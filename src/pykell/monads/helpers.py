import re


def count_leading_space(s):
    return 0 if not (match := re.search(r"^\s*", s)) else match.end()


def proc(lines: list[str]):
    lead_ident = " " * count_leading_space(lines[0])
    lines = [l[len(lead_ident) :] for l in lines]
    buf = [lines[0]]
    lines = lines[1:]
    for i, line in enumerate(lines):
        buf.append(line)
        if not "__def__" in line:
            continue
        ident = " " * count_leading_space(line)
        idx, arg = line.split("__def__")[1].rstrip(")").split("(")
        body = lines[i + 1 :]
        new_def = [f"def __def__{idx}({arg}):", *[l for l in body]]
        ret = [*[b for b in buf[:-1]], *[ident + p for p in proc(new_def)], buf[-1]]
        return [lead_ident + r for r in ret]
    return [lead_ident + r for r in buf]
