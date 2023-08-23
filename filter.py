
def fzf(search,string) -> (int,str):

    s = search
    l = string
    li = 0
    si = 0

    found_chars = ""

    matches = 0

    while li<len(l) and si<len(s):
        s_ = s[si]
        l_ = l[li]

        if s_==l_:
            matches += 1
            found_chars += s_
            si += 1
            li+=1
        else:
            li+=1

    if(matches<len(s)):
        return((0,""))
    else:
        return((matches,found_chars))

# ----------------------------------------

def get_snippet_list():
    with open("vex.c","r") as file:
        lines = file.read().splitlines()
    snippets:list[str] = []
    snip_lines:str = ""

    for line in lines:
        if "-----" not in line:
            snip_lines += f"{line}\n"
        else:
            if len(snip_lines)>0:
                snippets.append(snip_lines)
                snip_lines = ""
    return snippets

# ----------------------------------------
snippets = get_snippet_list()
current_snippet:str = snippets[0]
print("-- --")
print(current_snippet)

a = fzf("vec",current_snippet)
print(">>", a)

