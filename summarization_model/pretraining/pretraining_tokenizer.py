from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
from transformers import BartTokenizer
from tokenizers.processors import BertProcessing

tokenizer = ByteLevelBPETokenizer()

tokenizer.train(files='data/separate_sents(0~999).txt',
               vocab_size=32000,
               min_frequency=2,
               special_tokens=['<pad>', '<unk>', '<s>', '</s>', '<mask>'],
               )

tokenizer.save_model('output')
tokenizer = BartTokenizer(vocab_file='output/vocab.json', merges_file='output/merges.txt', do_lower_case=True)
tokenizer.save_pretrained('output/tokenizer_ord')


trained_tokenizer = BartTokenizer.from_pretrained('output/tokenizer_ord')
enc = trained_tokenizer.encode('This is a newly-pretrained tokenizer!')
print(trained_tokenizer.decode(enc))