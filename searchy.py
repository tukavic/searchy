print('starting')
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from collections import defaultdict, Counter

class bible_class:
    def __init__(self, bible_v):
        self.id2ref = {}
        self.ref2text = {}
        for id in range(len(bible_v)):
            ref,verse = bible_v[id].split('\t', 1)
            self.id2ref[id] = ref
            self.ref2text[ref] = verse.rstrip()

    def __getitem__(self, getter):
        try:
            getter = int(getter) #try to cast to int if id is str
        except:
            pass

        if isinstance(getter, int):
            ref = self.id2ref[getter]
            return self.ref2text[ref]
        else:
            return self.ref2text[getter]    

    def __setitem__(self, na):
        pass

model = SentenceTransformer('all-MiniLM-L6-v2')

#Our sentences we like to encode
with open('searchy/bsb2.txt', 'r') as file:
    bible_v = file.readlines()
    print(len(bible_v), 'lines in bsb2')
try:
    embeddings = np.load('searchy/bsb_embeddings.npy')
except:
    #Sentences are encoded by calling model.encode()
    embeddings = model.encode(bible_v)
    np.save('searchy/bsb_embeddings.npy', embeddings)

bible = bible_class(bible_v)
d = embeddings.shape[1]
print('embeddings shape', d)
index = faiss.IndexFlatL2(d)
index.add(embeddings)

if __name__ == "__main__":
    print('in main')
    print(bible is not None)
    print(bible[0])
    print(bible[30000])
    print(list(bible.id2ref.items())[:4])
    ngrams = defaultdict(int)
    for i in range(len(bible_v)):
        list_of_words = bible[i].lower().split(' ')
        for a,b,c,d,e in zip(list_of_words, list_of_words[1:], list_of_words[2:], list_of_words[3:], list_of_words[4:]):
            # print(a,b,c)
            ngrams[a+' '+b+' '+c+' '+d+' '+e]+=1
        # break
        if i%1000 == 0:
            print('.', end= '')
    # print(trigrams)
    ngrams = Counter(ngrams)
    print(len(ngrams))
    count = sum(1 for count in ngrams.values() if count > 1)
    print(ngrams.most_common(10))
    # create new embedding structure that is zipped to reference
    # find original references of each occurance in the ngram > 1

def return_results(str_inp):
    k = 20
    xq = model.encode([str_inp])
    D, I = index.search(xq, k)
    dict_list = [] 
    for v in sorted(I[0]):
    # for v in I[0]:
        ref,verse = bible_v[v].split('\t', 1)
        d = {"id": int(v), "ref": ref, "verse": verse}
        dict_list.append(d)
    return dict_list
    # out = ''
    # for v in sorted(I[0]):
    #     out += bible_v[v] + "\n"
    # return out

# while True:
#     k = 20
#     s = input('Enter search')#"jesus does a healing"
#     xq = model.encode([s])
#     D, I = index.search(xq, k)
#     #Print the embeddings
#     print(I)
#     print(D)
#     for v in sorted(I[0]):
#         print(bible_v[v], end = '')

# i = 0
# for sentence, embedding in zip(bible_v, embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", len(embedding))
#     print("")
#     i+=1
#     if i>10:
#         break