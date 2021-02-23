import PyPDF2
import os
import spacy
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
nlp = spacy.load("en_core_web_sm")
from spacy import displacy
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher
import sys
import pandas as pd
import seaborn as sns

#Add your resume path
mypath='./Vamil_Gandhi_Resume(CMU).pdf'




def pdfextract(file):
    fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    countpage = fileReader.getNumPages()
    count = 0
    text = []
    while count < countpage:    
        pageObj = fileReader.getPage(count)
        count +=1
        t = pageObj.extractText()

        text.append(t)
    return text

def read_skill():
    return open("./job_skill").read().splitlines()

def job_desc_profile():
    job_skill = read_skill()
    job_desc = sys.stdin.read()
    job_desc.lower()
    job_skill = [nlp.make_doc(text.lower()) for text in job_skill]
    matcher = PhraseMatcher(nlp.vocab)
    
    matcher.add('Job skill dict',job_skill)


    doc = nlp(job_desc)
    matches = matcher(doc)
    match_words_dic = {}
    for match_id, start, end in matches:
        span = Span(doc, start, end, label=match_id)
        #doc.ents = list(doc.ents) + [span]
        if span.text not in match_words_dic:
            match_words_dic[span.text.lower()] = 0
    
    return match_words_dic

def create_job_profile(file):
    match_words = job_desc_profile()
    text = pdfextract(file) 
    text = str(text)
    text = text.replace("\\n", "")
    text = text.lower()

    job_skill = [nlp.make_doc(text.lower()) for text in match_words ]
    matcher = PhraseMatcher(nlp.vocab)
    
    matcher.add('Jobs found in desc',job_skill)


    doc = nlp(text)
    matches = matcher(doc)
    match_words_dic = match_words
    count = 0
    for match_id, start, end in matches:
        span = Span(doc, start, end, label=match_id)
        #doc.ents = list(doc.ents) + [span]
        if span.text in match_words_dic:
            match_words_dic[span.text] += 1
            count += 1
    df = pd.DataFrame(match_words_dic.items(), columns = ['skills','Frequency'])
    print(df)
    print('\n')
    print("Percentage Match:",((count * 100)/len(match_words_dic)))
    return df

df = create_job_profile(mypath)

