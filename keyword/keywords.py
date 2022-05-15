from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.preprocessing import normalize

kw_model = KeyBERT('all-MiniLM-L12-v2')

# 2) Preprocess the sentences
def preprocess_sents(sentences, stop_words):
    sents_after=[]   # stop_words 제거, lower()한 list of sentences
    for sent in sentences:
        words = word_tokenize(sent)
        sents_after.append(' '.join([word.lower() for word in words if word.lower() not in stop_words and len(word)>1]))
        sents_after = [s for s in sents_after if s!=''] 
    return sents_after

# 3-1) Build the sentence graph
def build_sent_graph(sents, tfidf):  # 문장 리스트 -> tf-idf matrix -> sentence graph
    graph_sentence = []
    tfidf_mat = tfidf.fit_transform(sents).toarray()
    graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
    return graph_sentence

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
def get_keywords(text, kw_model=KeyBERT('all-MiniLM-L12-v2'), word_num=10, stopwords_list=None):
    stopwords_list = stopwords_list
    keywords = kw_model.extract_keywords(text, top_n=word_num, 
                                         keyphrase_ngram_range=(1,1), 
                                         stop_words=stopwords_list)
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
    
    
def key_question(script_path, weighted_keywords=False):
    sent_ngram = 2
    stopwords_path = 'stop_words_english.txt'
    script_path = script_path    

    with open(script_path) as f:
        text = f.read()
        sentences = sent_tokenize(text)
        sentences = [sent.replace('\n', ' ') for sent in sentences] 
    
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stop_words = f.readlines()
        stop_words = [word.strip() for word in stop_words]
        
        
    tfidf = TfidfVectorizer(ngram_range=(1, sent_ngram))
    stop_words = get_stopwords(stopwords_path)
    sentences = get_script(script_path)
    sents_after = preprocess_sents(sentences, stop_words)
    sent_graph = build_sent_graph(sents_after, tfidf)
    sent_rank_idx = get_ranks(sent_graph)  # 문장 가중치 그래프
    sorted_sent_idx = sorted(sent_rank_idx,   # 문장 가중치 그래프-가중치 작은 차순 정렬
                             key=lambda k: sent_rank_idx[k], reverse=True)
    keysents = get_keysents(sorted_sent_idx, sentences, sent_num=10)
    
    
    keywords_weight = get_keywords(text, kw_model, 10, stop_words)  
    keywords = [word_tup[0] for word_tup in keywords_weight]
    
    if weighted_keywords:
        return keywords_weight
    else:
        return keysents_blank(keywords, keysents)

key_question('scripts_for_stopwords/sample_script.txt')