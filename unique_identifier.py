from nltk import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

import gensim
import spacy
import numpy as np
import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import TfidfTransformer

nlp = spacy.load("en_core_web_sm")

f1path = "file1.txt"
f2path = "file2.txt"

files_total = []
file_docs = []
documents_full_text = []
for file in [f1path, f2path]:
    document = ""
    with open(file) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            line = line.replace("\n", "")
            document = document + " " + line
            file_docs.append(line)
        documents_full_text.append(document)
        files_total.append(file_docs)
        file_docs = []
        f.close()

sentence_occurrences = pd.DataFrame(columns=["sentence", "doc_num"])
st = "[Çü?éâäàåêëèïîìæôöòûùÿ¢£¥Pƒáí¿¬½¼¡«»¦ßµ±°•·²€„…†‡ˆ‰Š‹Œ‘’“”–—˜™›¨©®¯³´¸¹¾ÃÐÓÕ×ØÚÝÞ÷+]"

for i in range(0, len(files_total)):
    for sentence in sorted(set(files_total[i])):
        sentence = sentence.lower()
        sentence = re.sub(st, "", sentence)
        sentence = re.sub("-", "", sentence)
        # sentence = re.sub('(', '', sentence)
        # sentence = re.sub(')', '', sentence)
        df = pd.DataFrame([[sentence, i]], columns=["sentence", "doc_num"])
        sentence_occurrences = sentence_occurrences.append(df, ignore_index=True)

doc1 = sentence_occurrences[sentence_occurrences["doc_num"] == 0]
doc1 = doc1.reset_index(drop=True)
doc2 = sentence_occurrences[sentence_occurrences["doc_num"] == 1]
doc2 = doc2.reset_index(drop=True)

left_joined = doc1.merge(doc2, how="left", left_on="sentence", right_on="sentence")
right_joined = doc1.merge(doc2, how="right", left_on="sentence", right_on="sentence")

left_for_txt = left_joined
left_for_txt['Document Number'] = 1
left_for_txt['Unique'] = np.where(left_for_txt['doc_num_y'] == 1, "No", "Yes")
left_for_txt = left_for_txt[["sentence", "Document Number", "Unique"]]
left_for_txt.reset_index(inplace=True)
print(left_for_txt)
left_for_txt.to_html('static/file1_processed.html')

right_for_txt = right_joined
right_for_txt['Document Number'] = 2
right_for_txt['Unique'] = np.where(right_for_txt['doc_num_x'] == 0, "No", "Yes")
right_for_txt = right_for_txt[["sentence", "Document Number", "Unique"]]
right_for_txt.reset_index(inplace=True)
print(right_for_txt)
right_for_txt.to_html('static/file2_processed.html')
