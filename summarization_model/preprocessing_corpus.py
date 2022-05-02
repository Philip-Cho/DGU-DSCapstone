import os
import jsonlines
import json
import re
import string
import nltk
from nltk.data import load

nltk.download('punkt')
tokenizer = load('tokenizers/punkt/english.pickle')   # nltk.sent_tokenizer가 불러오는 파일
extra_abbreviation = [    
    'RE', 're', 'pat', 'no', 'nos', 'vol', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'eng', 'ser', 'ind', 'ed', 'pp', 'e.g', 'al', 'T.E.N.S', 'E.M.S', 'F.E', 'U.H.T.S.T', 'degree', '/g', 'm',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
tokenizer._params.abbrev_types.update(extra_abbreviation)   # _params로 파라미터에 직접 접근, 업데이트


start_file = 2000   # s2-corpus-000 등 파일 번호
end_file = 2999
data_dir = '/home/irteam/2017111707-dcloud-dir/data'

nums=[]
whole_lst=[]
# paperAbstract 데이터만 추출
print('appending...')
for i in range(start_file, end_file+1):
    if i<10:
        idx = '00{}'.format(i)
    elif i<100:
        idx = '0{}'.format(i)
    else:
        idx = '{}'.format(i)
        
    with jsonlines.open(data_dir+'/s2-corpus-{}'.format(idx), 'r') as file:
        data_lst = [line['paperAbstract'] for line in file if line['paperAbstract']!='']
        whole_lst = whole_lst + data_lst
    nums.append(i)
    print('>'+str(i), end='')
print('\nlines:', len(whole_lst))

# 모든 코퍼스 파일의 paperAbstract 문장으로 분리하여 txt 파일에 저장(계속 이어씀)
# whole_lst에 모든 데이터 저장 후 한번에 생성하기
sent_file = open(data_dir+'/separate_sents(2000~2999).txt', 'a', encoding='utf-8')
no_blank = False
print('writing...')
for i, line in enumerate(whole_lst):
    if i%10000==0:
        print('>'+str(i), end='')

    if line=='':
        break
    if line.strip()=='':
        if no_blank:
            continue
        sent_file.write(f'{line}')
    else:
        result_ = nltk.sent_tokenize(line)   # 문장 구조 학습한 모델 -> 약어에 쓰이는 마침표 등 학습됨
        result = [f'{cul_line}\n' for cul_line in result_]
        for save_line in result:
            sent_file.write(save_line)
print()  
sent_file.close()