from nltk.tokenize import RegexpTokenizer, word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from sklearn.preprocessing import normalize
import os
    
# 1-1) Load the stopwords
def get_stopwords(stopwords_path):
    stop_words_1 = stopwords.words('english')   # stopwords 179개
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stop_words = f.readlines()
        stop_words = [word.strip() for word in stop_words]   # stopwords 854개
    return stop_words
        
# 1-2) Load the script  
def get_script(script_path):
    with open(script_path) as f:
        text = f.read()
    sentences = sent_tokenize(text)
    sentences = [sent.replace('\n', ' ') for sent in sentences] 
    return sentences

# 3-1) Build the sentence graph
def build_sent_graph(sents, tfidf):  # 문장 리스트 -> tf-idf matrix -> sentence graph
    graph_sentence = []
    tfidf_mat = tfidf.fit_transform(sents).toarray()
    graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
    return graph_sentence

# 3-2) Build the word graph
def build_word_graph(sent, cnt_vec):
    cnt_vec_mat = normalize(cnt_vec.fit_transform(sent).toarray().astype(float), axis=0)
    vocab = cnt_vec.vocabulary_
    graph_word = np.dot(cnt_vec_mat.T, cnt_vec_mat)
    idx2word = {vocab[word] : word for word in vocab}
    return graph_word, idx2word

# 4) Calculate the ranks of each sentence or word
def get_ranks(graph, d=0.85):
    A = graph
    matrix_size = A.shape[0]
    for id in range(matrix_size):
        A[id, id] = 0   # diagonal 부분 -> 0으로 바꿔줌(diagonal matrix)
        link_sum = np.sum(A[:, id])
        if link_sum != 0:
            A[:, id] /= link_sum
        A[:, id] *= -d
        A[id, id] = 1
        
    B = (1-d) * np.ones((matrix_size, 1))
    ranks = np.linalg.solve(A, B)
    
    return {idx: r[0] for idx, r in enumerate(ranks)}

# 5-1) Get the list of keywords
def get_keywords(sorted_word_idx, idx2word, word_num=5):
    keywords = []
    index = []
    for idx in sorted_word_idx[:word_num]:
        index.append(idx)      
    for idx in index:
        keywords.append(idx2word[idx])
        
    return keywords

# 5-2) Get the list of keysentences
def get_keysents(sorted_sent_idx, sentences, sent_num=2):
    keysents=[]
    index=[]
    for idx in sorted_sent_idx[:sent_num]:
        index.append(idx)
    for idx in index:
        keysents.append(sentences[idx])

    return keysents

# 6) Final: Get the sentence with blank, answer sentence, answer word
def keysents_blank(keywords:list, keysents:list):
    keysent=''   # blank 만들 keysent
    keysent_blank=''   # blank 만든 keysent
    keyword_keysent=''   # keysent의 blank에 들어갈 keyword
    lowest_weight=23   # 가장 작은 weight(초기값: 최대 weight+1)
    
    for sent in keysents:
        sent_weight = keysents.index(sent) + 1 
        
        keyword=''
        for word in keywords:
            if word in sent:
                keyword = word
                break   # keywords 리스트는 앞의 index일수록 순위가 높은 키워드 -> 문장에 존재하면 break    
        if keyword!='':
            word_weight = keywords.index(keyword) + 1
        else:
            word_weight = 23
            
        weight = sent_weight + word_weight
        if weight<lowest_weight:
            lowest_weight = weight
            keysent = sent
            keyword_keysent = keyword
    
    keysent_blank = keysent.replace(keyword_keysent, '__________')
    
    return {'sentence_blank':keysent_blank, 'sentence':keysent, 'answer':keyword_keysent}

def preprocess_sents(sentences, stop_words):
    # 2) Preprocess the sentences
    sents_after=[]   # stop_words 제거, lower()한 list of sentences
    for sent in sentences:
        words = word_tokenize(sent)
        sents_after.append(' '.join([word.lower() for word in words if word.lower() not in stop_words and len(word)>1]))
        sents_after = [s for s in sents_after if s!=''] 
    return sents_after


def run():
    # 1-3) Set the algorithm
    sent_ngram = 1
    word_ngram = 3    
    tfidf = TfidfVectorizer(ngram_range=(1, sent_ngram))
    cnt_vec = CountVectorizer(ngram_range=(1, word_ngram))
    
    stopwords_path = 'stop_words_english.txt'
    script_path = 'sample_script.txt'
    stop_words = get_stopwords(stopwords_path)
    sentences = get_script(script_path)
    sents_after = preprocess_sents(sentences, stop_words)
    
    sent_graph = build_sent_graph(sents_after, tfidf)
    word_graph, idx2word = build_word_graph(sents_after, cnt_vec)
    
    sent_rank_idx = get_ranks(sent_graph)  # 문장 가중치 그래프
    sorted_sent_idx = sorted(sent_rank_idx,   # 문장 가중치 그래프-가중치 작은 차순 정렬
                             key=lambda k: sent_rank_idx[k], reverse=True)
    word_rank_idx = get_ranks(word_graph)  # 단어 가중치 그래프
    sorted_word_idx = sorted(word_rank_idx, 
                             key=lambda k: word_rank_idx[k], reverse=True)

    keywords = get_keywords(sorted_word_idx, idx2word, word_num=10)
    keysents = get_keysents(sorted_sent_idx, sentences, sent_num=10)

    print(keysents_blank(keywords, keysents))

    return keysents_blank(keywords, keysents)



if __name__ == '__main__':
    run()