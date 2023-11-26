# importing QT libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt

import re
from typing import List,Tuple
from enum import Enum

class SearchMode(Enum):
    fuzzy = 0
    hashtag = 1
    exactmatch = 2

class CaseSensive(Enum):
    upperlower = 0
    lower = 1


class Utils():

    def __init__(self):
        self.search_mode = SearchMode.fuzzy
        self.case_sensitive = CaseSensive.lower
        self.snippet_index = 0

        pass
    # ----------------------------------------------------------
    """ split file by separators containing dashes """
    def get_snippet_list(self,file:str) -> List[str]:
        # print(">",file)
        with open(file,"r") as f:
            lines = f.read().splitlines()

        snippets:list[str] = []
        snip_lines:str = ""
        for line in lines:
            if "-----" not in line:
                snip_lines += f"{line}\n"
            else:
                snippets.append(snip_lines)
                snip_lines = ""
        if len(snip_lines)>0:
            snippets.append(snip_lines)

        return snippets

    # ----------------------------------------------------------
    """
    search for letters in string and return number of matches
    basic 'FZF like' fuzzy search
    """
            
    def fuzzy_search(self, search, string) -> float:
    
        if self.search_mode == SearchMode.hashtag:
            string = self.keep_hashtags_only(string)
    
        s = search
        l = string
        li = 0
        si = 0

        match_score = 0.0
        last_match_index = 0
        letters_found = 0

        while li<len(l) and si<len(s):
            s_ = s[si]
            l_ = l[li]

            if s_==l_:
                letters_found += 1
                si += 1
                li+=1
                dist = abs(last_match_index-li)
                match_score += 1/float(dist)
                last_match_index = li
            else:
                li+=1
        if letters_found<len(search):
            return 0.0
        else:
            return match_score
            
    # ----------------------------------------------------------
    """ keep only hastags in the block of text """
    def keep_hashtags_only(self,text:str) -> str:
        hashtags = ""
        lines = text.split("\n")
        for line in lines:
            if line.startswith("//") and "#" in line:
                # don't lose the first tag is not space after //
                # eg: '//#firstag #secondtag
                line = re.sub("//","",line)
                filtered = list(filter(lambda b: b.startswith("#"), line.split(" ")))
                print("..",filtered)
                h = " ".join(filtered)
                h = re.sub("#","",h)
                hashtags = h
        return hashtags

    """ fuzzy search in snippet lines, return list of snippets """
    def search_snippets(self,search_string) -> List[Tuple[float,int]]:

        search_results = []
        
        if len(search_string)==0:
            return search_results

        for idx,snippet in enumerate(self.snippets):

            if self.case_sensitive == CaseSensive.lower:
                search_string = search_string.lower()
                
            match_score = self.fuzzy_search(search_string,snippet)

            if match_score>0:
                result:Tuple[float,int] = (match_score,idx)
                search_results.append(result)

        search_results.sort(reverse=True)


        return search_results        

    # ----------------------------------------------------------
    def update_text(self,text):
        print("snippet index :",self.snippet_index)

        results:List[Tuple[float,int]] = self.search_snippets(text)

        print(results)

    #     case = "A" if self.case_sensitive == CaseSensive.upperlower else "a"
    #     search_mode = "fuzzy" if self.search_mode == SearchMode.fuzzy else "#"
    #     s = f"{search_mode} {case}"
    #     
    #     if len(results)>0:
    #         self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
    #         current_snippet = self.snippets[results[self.snippet_index][1]]
    #         self.ui.text.setText(current_snippet)
    #         match = results[self.snippet_index][0]
    #
    #         s = f"{s}  {self.snippet_index+1}/{len(results)}    match:{match:.2f}"
    #
    #     self.ui.status.setText(s)
    #
    def textchanged(self,text):
        self.update_text(text)

