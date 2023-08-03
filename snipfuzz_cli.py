from pynput.keyboard import Key, Listener
from typing import List,Tuple

class TextSearch:
    def __init__(self,file:str) -> None:
        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()
        self.search_mode = 0

    # ----------------------------------------------------------
    """ split file by separators containing dashes """
    def get_snippet_list(self) -> List[str]:
        with open(self.file,"r") as file:
            lines = file.read().splitlines()
        snippets:list[str] = []
        snip_lines:str = ""
        for line in lines:
            if "-----" not in line:
                snip_lines += f"{line}\n"
            else:
                snippets.append(snip_lines)
                snip_lines = ""
        return snippets
    # ----------------------------------------------------------
    def fzf(self,search,string):
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

        if(matches<len(s)):
            return 0
        else:
            return(matches)

    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string,search_mode) -> List[Tuple[float,str]]:
        search_results = []
        for snippet in self.snippets:

            score_sum = 0
            score = 0
            for line in snippet.split("\n"):
                if search_mode == 1:
                    if "#" in line:
                        score = self.fzf(search_string,line)
                    else:
                        pass
                else:
                    score = self.fzf(search_string,line)

                score_sum += score

            if score_sum>0:
                result:Tuple[float,str] = (float(score_sum),snippet)
                search_results.append(result)
        #
        search_results.sort(reverse=True)
        return search_results
    # ----------------------------------------------------------
    def display_snippet(self,snippet) -> str:
        std_out = ""
        lines = snippet[1].split("\n")
        for line in lines:
            std_out += f"\n{line}"
        return std_out
    # ----------------------------------------------------------
    def on_press(self,key) -> None:
        # convert keycode to string
        keystr ="{0}".format(key)[1:-1]

        if str(key).startswith("Key"):
            if key == Key.backspace:
                if len(self.input_char_list)>0:
                    if len(self.input_char_list)>0:
                        self.input_char_list.pop()
            elif key == Key.up:
                self.snippet_index-=1
            elif key == Key.down:
                self.snippet_index+=1
            elif key == Key.left:
                self.search_mode = 0
            elif key == Key.right:
                self.search_mode = 1
            elif key == Key.space:
                self.input_char_list.append(" ")
            elif key == Key.alt_l:
                if self.search_mode == 0:
                    self.search_mode = 1
                else:
                    self.search_mode = 0
            else:
                pass
        else:
            self.input_char_list.append(keystr)

        # clear terminal
        std_out = ""
        std_out+=chr(27) + "[2J\n"
        search_string = "".join(self.input_char_list)
        results:List[Tuple[float,str]] = self.search(search_string,self.search_mode)
        std_out+=".............................."

        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            tt =self.display_snippet(results[self.snippet_index])
            std_out += tt
            ratio:float = int(float(results[self.snippet_index][0])*100)/100

            std_out+="..............................\n"
            search_mode_char = "-"
            if self.search_mode == 1:
                search_mode_char = "#"

            std_out+=f"{search_mode_char} {self.snippet_index+1} of {len(results)} : match_ratio: {ratio}"

        std_out+="\n"+search_string
        print(std_out)

# ----------------------------------------------------------

      


ts = TextSearch("vex.c")
with Listener(
        on_press=ts.on_press,
        ) as listener:
    listener.join()

