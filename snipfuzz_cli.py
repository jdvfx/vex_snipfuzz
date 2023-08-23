from pynput.keyboard import Key, Listener
from typing import List,Tuple
import subprocess
from enum import Enum

class SearchMode(Enum):
    fuzzy = 0
    hashtag = 1

class SnipFuzz:

    def __init__(self,file:str) -> None:
        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()
        self.search_mode = SearchMode.fuzzy

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

        if(matches<len(s)):
            return 0
        else:
            return(matches)

    def copy_to_clipboard(self, text:str):
        subprocess.run(['echo', '-n', text], stdout=subprocess.PIPE)
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))

    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string,search_mode) -> List[Tuple[float,str]]:
        search_results = []
        for snippet in self.snippets:

            score_sum = 0
            score = 0
            for line in snippet.split("\n"):
                if search_mode is SearchMode.hashtag:
                    if "#" in line:
                        score = self.fuzzy_search(search_string,line)
                    else:
                        pass
                elif search_mode is SearchMode.fuzzy:
                    score = self.fuzzy_search(search_string,line)
                else: # would use match/case if Python 3.10
                    pass

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
            elif key == Key.space:
                self.input_char_list.append(" ")
            elif key == Key.alt_l:
                if self.search_mode is SearchMode.fuzzy:
                    self.search_mode = SearchMode.hashtag
                else:
                    self.search_mode = SearchMode.fuzzy
            else:
                pass
        else:
            self.input_char_list.append(keystr)

        # clear terminal
        std_out = chr(27) + "[2J\n"
        std_out += ".............................."
        # create the search string text from char array
        search_string = "".join(self.input_char_list)

        results:List[Tuple[float,str]] = self.search(search_string,self.search_mode)

        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            self.current_snippet = results[self.snippet_index]

            tt = self.display_snippet(self.current_snippet)
            std_out += tt
            ratio:str = f"{float(results[self.snippet_index][0]):.2f}"

            std_out += "..............................\n"
            search_mode_char = "-"
            if self.search_mode is SearchMode.hashtag:
                search_mode_char = "#"

            std_out += f"{search_mode_char} {self.snippet_index+1} of {len(results)} : match_ratio: {ratio}"

        std_out += "\n"+search_string
        print(std_out)

        # copy snippet to clipboard and exit
        if key == Key.ctrl:
            text = self.current_snippet[1]
            self.copy_to_clipboard(text)
            return False  # Stop the listener and exit

ts = SnipFuzz("vex.c")
with Listener(
        on_press=ts.on_press,
        ) as listener:
    listener.join()

