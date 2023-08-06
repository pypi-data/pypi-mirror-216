import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from collections import defaultdict
import glob
import re
import random
random.seed(3)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tqdm import tqdm

from src.peduncle.peduncle import *

class DataLoader(object):
    def __init__(self, limit=None) -> None:
        raw_data_pattern = "../data/dragnet_data-master/HTML/*.html"
        eval_data_pattern = "../data/dragnet_data-master/Corrected/*.html.corrected.txt"

        def get_base_filename(file_path):
            base_name = os.path.basename(file_path)
            return base_name.replace('.html', '').replace('.corrected.txt','')

        def create_dict(file_paths):
            file_dict = defaultdict(list)
            for file in file_paths:
                file_dict[get_base_filename(file)].append(file)
            return file_dict

        rawfilenames = glob.glob(raw_data_pattern)
        evalfilenames = glob.glob(eval_data_pattern)

        raw_dict = create_dict(rawfilenames)
        eval_dict = create_dict(evalfilenames)

        # merge two dicts and filter out keys (filenames) that don't have both raw and eval filepaths
        merged_dict = {k: (raw_dict[k], eval_dict[k]) for k in raw_dict.keys() & eval_dict.keys()}

        self.values = sorted(list(merged_dict.values()))
        random.shuffle(self.values)
        
        if limit is not None:
            self.values = self.values[:limit]
        
        self.index = 0
        
    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self,items):
        return self.values[items][0][0],self.values[items][1][0]
    
    def __next__(self):
        if self.index < len(self.values):
            result = self.values[self.index]
            self.index += 1
            return result[0][0],result[1][0]
        else:
            raise StopIteration

class Evaluator(object):
    def __init__(self) -> None:
        self.answer_corpus=[]
        self.eval_corpus=[]
        self.scores=-1
    
    def push(self,eval_doc:str,answer_doc:str):
        self.eval_corpus.append(eval_doc)
        self.answer_corpus.append(answer_doc)
    
    def run(self):
        corpus=np.concatenate([self.answer_corpus,self.eval_corpus],axis=0)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)
        answer_mat = X[:int(X.shape[0]/2),:]
        eval_mat = X[int(X.shape[0]/2):,:]
        self.scores = np.array([
            cosine_similarity(answer_mat[i], eval_mat[i]
            )[0][0] for i in range(answer_mat.shape[0])
        ])
        
    def get_final_score(self):
        self.run()
        return self.scores.mean()
    
    def get_acc_rate(self,threshold):
        c = 0
        for i in self.scores:
            if i > threshold:
                c+=1
        return c/len(self.scores)
    
    def clean(self, text):
        text: str = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return re.sub(r'\s+', ' ', text)
        
if __name__=="__main__":
    
    data = DataLoader()
    evaluator = Evaluator()
    
    diffs = []
    
    with tqdm(total=len(data)) as bar:
        for raw_fname,eval_fname in data:
            raw_file = open(raw_fname,'r',encoding='utf8',errors='ignore')
            eval_file = open(eval_fname,'r',encoding='utf8',errors='ignore')
            raw_str = raw_file.read()
            eval_str = eval_file.read()
            raw_file.close()
            eval_file.close()
            
            # extracted_content = evaluator.clean(Grader(raw_str).main_node.text)
            extracted_content = evaluator.clean(extract_text(raw_str,0.21))

            eval_str = evaluator.clean(eval_str)
            evaluator.push(extracted_content,eval_str)
            
            diffs.append(len(extracted_content)-len(eval_str))
            
            bar.update()
    
    print(f"similarty: {evaluator.get_final_score()}")
    print(f"acc: {evaluator.get_acc_rate(0.95)}")
    print(f"len_diff: {np.mean(diffs)}")
    print(f"diff std: {np.std(diffs)}")