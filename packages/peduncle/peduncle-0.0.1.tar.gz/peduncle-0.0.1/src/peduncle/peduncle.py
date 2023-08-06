'''
user API
'''
from bs4.element import Tag

from .grader import Grader

def extract_text(html:str, alpha:float=0.25) -> str:
    '''
    html: raw html string contains content waiting to be extracted
    alpha: float between 0 and 1, larger the alpha, the extractor
    '''
    G = Grader(html,alpha)
    return G.main_node.text

def extract_node(html:str, alpha:float=0.25) -> Tag:
    '''
    html: raw html string contains content waiting to be extracted
    alpha: float between 0 and 1, larger the alpha, the extractor
    '''
    G = Grader(html,alpha)
    return G.main_node