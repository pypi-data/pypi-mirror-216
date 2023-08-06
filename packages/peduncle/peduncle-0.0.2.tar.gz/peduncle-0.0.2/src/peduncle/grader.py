import re
import bs4
from bs4 import BeautifulSoup

class SAG:
    def __init__(self,alpha):
        self.nodelist = []
        self.alpha=alpha
        if self.alpha<=0 or self.alpha>=1:
            raise Warning("alpha must be float between 0 and 1")

    def __get_text_length(self, node):
        text: str = node.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        text = re.sub(r'\s+', ' ', text)
        return len(text)

    def __score_text_children_ratio(self, child_count, text_length):
        c_factor = self.alpha*100
        c = child_count / c_factor
        c_score = c + 1 / c
        return text_length / c_score

    def __score_tag_name(self, node):
        if node.name in ["article", "content", "tbody", "main", "body"]:
            return 3
        if node.name in ["center"]:
            return 1.5
        if node.name in [ "script", "style", "noscript", "applet", "meta", 
              "link", "a", "base", "img", "button", "header", "footer",
              "aside", "tfoot", "menu", "nav", "frame", "iframe", 
              "form", "title", "h1", "h2", "html","head"]:
            return 0
        return 1

    def _score(self, node, child_count):
        text_length = self.__get_text_length(node)
        child_score = self.__score_text_children_ratio(child_count, text_length)
        tag_score = self.__score_tag_name(node)
        return child_score * (tag_score ** 0.3)

    def score(self, node, child_count):
        self.nodelist.append([node, self._score(node, child_count)])

    def get_content(self):
        self.nodelist = sorted(self.nodelist, key=lambda x: x[1], reverse=True)
        return self.nodelist[0][0]
 
class Grader(object):
    
    content_child_tags=["td","th","tr","li","p"]
    
    def __init__(self, htmlstr, alpha=0.25):
        self.htmlstr = htmlstr
        self.soup = BeautifulSoup(htmlstr, features="lxml")
        self.sag = SAG(alpha)
        self.nodelist = []
        self.__run_sag()
        self.main_node:bs4.element.Tag = self.sag.get_content()
    
    def __run_sag(self):
        self.gotree(self.soup)

    def gotree(self, node, depth=1):
        if node.name in self.content_child_tags:
            ct = 0.2
        else:
            ct = 1
        for i in node:
            if i.name is None:
                continue
            ct += self.gotree(i, depth + 1)
            self.sag.score(i, ct)
        return ct