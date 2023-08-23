from termcolor import colored
from typing import Tuple


# with open("vex.c","r") as file:
#
#     x = 0
#     s = ""
#
#     lines = file.read().splitlines()
#     for i in lines:
#         if "rotate" in i:
#             s += colored(i,"cyan")
#         else:
#             s += colored(i,"white")
#         s += "\n"
#         x+=1
#         if x>10:
#             break
#
#     print(s)


def fuzzy_search(search,string) -> Tuple[int,str]:
    s = search
    l = string
    li = 0
    si = 0

    matches = 0

    newstr =""

    while li<len(l) and si<len(s):
        s_ = s[si]
        l_ = l[li]

        if s_==l_:
            newstr += colored(l_,"red")
            matches += 1
            si += 1
            li+=1
        else:
            newstr += colored(l_,"white")
            li+=1

    if(matches<len(s)):
        return (0, string)
    else:
        l_ = l[li:]
        newstr += colored(l_,"white")
        return (matches, newstr)

string = "v@v = qrotate(quaternion(angle, axis),v@v);"
search = "quat"

(score,string2) = fuzzy_search(search,string)

print(score,string2)


