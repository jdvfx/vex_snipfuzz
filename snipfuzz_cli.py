from pynput.keyboard import Key, Listener
import string 
import re
import difflib
from typing import List,Tuple

class TextSearch:
    def __init__(self,file:str) -> None:
        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()

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
    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string) -> List[Tuple[float,str]]:
        search_results = []
        for snippet in self.snippets:
            alpha = re.sub('[^a-za-z]+', ' ', snippet) # alpha only
            words_ = alpha.split(' ')
            words_ = [x for x in words_ if x != ''] # remove empty elements
            words = list(set(words_)) # remove duplicates

            for word in words:
                ratio:float = difflib.SequenceMatcher(None,search_string,word).ratio()
                if ratio>0.5:
                    result:Tuple[float,str] = (ratio,snippet)
                    search_results.append(result)
                    break
        #
        search_results.sort(reverse=True)
        return search_results
    # ----------------------------------------------------------
    def display_snippet(self,snippet) -> None:
        lines = snippet[1].split("\n")
        for line in lines:
            print(line)
    # ----------------------------------------------------------
    def on_press(self,key) -> None:
        # convert keycode to string
        keystr ="{0}".format(key)[1:-1]

        if keystr in string.ascii_letters:
            self.input_char_list.append(keystr)
        elif key == Key.backspace:
            if len(self.input_char_list)>0:
                if len(self.input_char_list)>0:
                    self.input_char_list.pop()
        elif key == Key.up:
            self.snippet_index-=1
        elif key == Key.down:
            self.snippet_index+=1
        else:
            pass

        # clear terminal
        print(chr(27) + "[2J")
        search_string = "".join(self.input_char_list)
        results:List[Tuple[float,str]] = self.search(search_string)

        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            self.display_snippet(results[self.snippet_index])
            ratio:float = int(float(results[self.snippet_index][0])*100)/100
            print(f"{self.snippet_index} of {len(results)-1} : match_ratio: {ratio}")
        print(search_string)

# ----------------------------------------------------------

      


ts = TextSearch("vex.c")
with Listener(
        on_press=ts.on_press,
        ) as listener:
    listener.join()

