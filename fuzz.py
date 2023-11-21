# basic "FZF like" cli fuzzy search

from pynput.keyboard import Key, Listener
from termcolor import colored

class SnipFuzz:

    def __init__(self,lines) -> None:
            self.input_char_list = []
            self.lines = lines
    # ----------------------------------------------------------
    def on_press(self,key) -> None:
        # convert keycode to string
        keystr ="{0}".format(key)[1:-1]

        if str(key).startswith("Key"):
            if key == Key.backspace:
                if len(self.input_char_list)>0:
                    if len(self.input_char_list)>0:
                        self.input_char_list.pop()
            elif key == Key.space:
                self.input_char_list.append(" ")
            else:
                pass
        else:
            self.input_char_list.append(keystr)

        # clear terminal
        std_out = chr(27) + "[2J\n"

        search_string = "".join(self.input_char_list)
        if len(search_string)>0:
            results = self.search(search_string)
            std_out += results

        std_out += "\n"
        std_out += colored(search_string,"green")
        print(std_out)

    def fuzzy_search(self,search,string):

        s = search
        l = string
        li = 0
        si = 0

        matches = 0

        while li<len(l) and si<len(s):
            s_ = s[si]
            l_ = l[li]

            if s_==l_:
                matches += 1
                si += 1
                li+=1
            else:
                li+=1

        if(matches<len(s) and matches>0):
            return 0
        else:
            return(matches)

    def search(self,search_string):

        newlines = ""
        for line in self.lines:
            newline = ""
            a = self.fuzzy_search(search_string,line)
            if a>0:
                j = 0
                for i in line:
                    if j<len(search_string):
                        if i == search_string[j]:
                            newline += colored(i,"red")
                            j+=1
                        else:
                            newline += colored(i,"white")
                    else:
                        newline += colored(i,"white")

            if len(newline)>0:
                newlines+="\n"+newline
        return newlines





lines = None

with open("vex.c","r") as f:
    lines = f.read().splitlines()

if lines is not None:
    ts = SnipFuzz(lines)
    with Listener(
            on_press=ts.on_press,
            ) as listener:
        listener.join()



