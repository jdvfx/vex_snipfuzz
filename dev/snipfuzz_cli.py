from pynput.keyboard import Key, Listener
from typing import List,Tuple
import subprocess
from enum import Enum
from termcolor import colored

class SearchMode(Enum):
    fuzzy = 0
    hashtag = 1

class CaseSensive(Enum):
    upperlower = 0
    lower = 1

class SnipFuzz:

    def __init__(self,file:str) -> None:
        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()
        self.search_mode = SearchMode.fuzzy
        self.case_sensitive = CaseSensive.upperlower

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
    def fuzzy_search(self,search,string) -> Tuple[int,str]:
        s = search
        l = string

        li = 0
        si = 0

        matches = 0
        newstr =""

        while li<len(l) and si<len(s):
            s_ = s[si]
            l_ = l[li]

            # stash original letter before case change
            l__ = l_
            if self.case_sensitive == CaseSensive.lower:
                s_ = s_.lower()
                l_ = l_.lower()

            if s_==l_:
                newstr += colored(l__,"red")
                matches += 1
                si += 1
                li+=1
            else:
                newstr += colored(l__,"white")
                li+=1

        if(matches<len(s)):
            return (0, string)
        else:
            l_ = l[li:]
            newstr += colored(l_,"white")
            return (matches, newstr)

    def copy_to_clipboard(self, text:str) -> None:
        subprocess.run(['echo', '-n', text], stdout=subprocess.PIPE)
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))

    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string,search_mode) -> List[Tuple[float,str,str]]:
        search_results = []
        for snippet in self.snippets:

            score_sum = 0
            score = 0
            result = (0,"",snippet)
            snippet_with_colors = ""

            for line in snippet.split("\n"):
                if search_mode is SearchMode.hashtag:
                    if "#" in line:
                        searchresult = self.fuzzy_search(search_string,line)
                        scolors = searchresult[1]
                        score = searchresult[0]
                        snippet_with_colors += scolors + "\n"
                    else:
                        pass
                elif search_mode is SearchMode.fuzzy:
                    searchresult = self.fuzzy_search(search_string,line)
                    scolors = searchresult[1]
                    score = searchresult[0]
                    snippet_with_colors += scolors + "\n"
                else: # would use match/case if Python 3.10
                    pass

                score_sum += score

            if score_sum>0:
                result:Tuple[float,str,str] = (float(score_sum),snippet_with_colors,snippet)
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
            elif key == Key.left:
                self.snippet_index=0
            elif key == Key.right:
                self.snippet_index=len(self.snippets)-1
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
            elif key == Key.shift:
                if self.case_sensitive is CaseSensive.upperlower:
                    self.case_sensitive = CaseSensive.lower
                else:
                    self.case_sensitive = CaseSensive.upperlower
            else:
                pass
        else:
            self.input_char_list.append(keystr)

        # clear terminal
        std_out = chr(27) + "[2J\n"
        # std_out = ""
        std_out += ".............................."
        # create the search string text from char array
        search_string = "".join(self.input_char_list)
        
        if self.case_sensitive is CaseSensive.lower:
            search_string = search_string.lower()

        results:List[Tuple[float,str,str]] = self.search(search_string,self.search_mode)

        ratio:str = ""

        self.snippet_index:int = min(max(0,self.snippet_index),len(results))
        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            self.current_snippet = results[self.snippet_index]

            tt = self.display_snippet(self.current_snippet)
            print(self.current_snippet)
            # exit()
            std_out += tt
            ratio:str = f"{float(results[self.snippet_index][0]):.2f}"

        # build cli output string and print
        std_out += "..............................\n"
        search_mode_char = "-"
        case_sensitive_char = "A"
        if self.search_mode is SearchMode.hashtag:
            search_mode_char = "#"
        if self.case_sensitive is CaseSensive.lower:
            case_sensitive_char = "a"
        std_out += f"{case_sensitive_char} {search_mode_char} {self.snippet_index} of {len(results)-1} : match_ratio: {ratio}"
        std_out += "\n"+search_string
        print(std_out)

        # copy snippet to clipboard and exit
        if key == Key.ctrl:
            text = self.current_snippet[2]
            self.copy_to_clipboard(text)
            return False  # Stop the listener and exit

ts = SnipFuzz("vex.c")
with Listener(
        on_press=ts.on_press,
        ) as listener:
    listener.join()

