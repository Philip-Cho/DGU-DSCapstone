from summarizer import Summarizer,TransformerSummarizer


def load_model():
    print("모델 로드 시작")
    GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
    print("모델 로드 완료")
    return GPT2_model

def summary_text(text, model):
    GPT2_model = model
    sum_text = ''.join(GPT2_model(text, min_length=60))
    return sum_text
