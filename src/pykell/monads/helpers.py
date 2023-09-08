import inspect
import ast


def count_leading_whitespace(line):
    count = 0
    for char in line:
        if char in [" ", "\t"]:
            count += 1
        else:
            break
    return count


def deindent(src):
    lines = src.split("\n")
    base_identation = count_leading_whitespace(lines[0])
    return "\n".join(line[base_identation:] for line in lines)


def is_yield_assign(node):
    return isinstance(node, ast.Assign) and isinstance(node.value, ast.Yield)


class ReplaceMonadic(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef, idx=0):
        if idx == 0:  # remove decorator
            node.decorator_list = []

        # figure out the statement where the first yield assign occurs
        for i, b in enumerate(node.body):
            if is_yield_assign(b):
                break
        else:
            return node  # none were found, just return!

        # i position where it happensss
        assert len(b.targets) == 1  # type: ignore

        # used by the function definition
        left_name = b.targets[0].id  # type: ignore
        right = b.value.value  # type: ignore

        rest_of_body = node.body[i + 1 :]
        node.body = node.body[:i]

        funcdef = ast.FunctionDef(
            name=f"__def__{idx}",
            args=ast.arguments(
                args=[ast.arg(arg=left_name)],
                posonlyargs=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=rest_of_body,
            decorator_list=[],
        )

        binded = ast.Call(
            func=ast.Name(id="bind", ctx=ast.Load()),
            args=[right, ast.Name(id=f"__def__{idx}", ctx=ast.Load())],
            keywords=[],
        )
        returning = ast.Return(value=binded)

        # recursive call to eliminate all yields
        final_funcdef = self.visit_FunctionDef(funcdef, idx + 1)

        # adapting the node body
        node.body += [final_funcdef, returning]

        return node


class RelplaceReturns(ast.NodeTransformer):
    def visit_Return(self, node):
        return ast.Return(
            value=ast.Call(
                func=ast.Name("unit", ctx=ast.Load()), args=[node.value], keywords=[]
            )
        )


def convert(func, bind, unit):
    src = inspect.getsource(func)
    src = deindent(src)
    tree = ast.parse(src)
    new_tree = RelplaceReturns().visit(tree)
    new_tree = ReplaceMonadic().visit(new_tree)
    ast.fix_missing_locations(new_tree)
    namespace = {}
    global_namespace = {**func.__globals__, "bind": bind, "unit": unit}
    exec(compile(new_tree, filename="<ast>", mode="exec"), global_namespace, namespace)
    modified_func = namespace[func.__name__]
    return modified_func
