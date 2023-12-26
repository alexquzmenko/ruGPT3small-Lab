import numpy as np
import torch
np.random.seed(42)
torch.manual_seed(42)
from transformers import GPT2LMHeadModel, GPT2Tokenizer
def load_tokenizer_and_model(model_name_or_path):
  return GPT2Tokenizer.from_pretrained(model_name_or_path), GPT2LMHeadModel.from_pretrained(model_name_or_path).cuda()


def generate(
    model, tok, text,
    do_sample=True, max_length=50, repetition_penalty=5.0,
    top_k=5, top_p=0.95, temperature=1,
    num_beams=None,
    no_repeat_ngram_size=3
    ):
  input_ids = tok.encode(text, return_tensors="pt").cuda()
  out = model.generate(
      input_ids.cuda(),
      max_length=max_length,
      repetition_penalty=repetition_penalty,
      do_sample=do_sample,
      top_k=top_k, top_p=top_p, temperature=temperature,
      num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
      )
  return list(map(tok.decode, out))
def generate_model_response(text, num_beams=5, max_length=240):
    tokenizer, model = load_tokenizer_and_model("sberbank-ai/rugpt3small_based_on_gpt2")
    return generate(model, tokenizer, text, max_length=max_length, num_beams=num_beams)[0]


def generate_response(text):
    texts = [generate_model_response(f"{text}. Актуальность:\n "),
             generate_model_response(f"Курсовая работа по теме: {text.lower()}. Аннотация работы: ", max_length=120)]
    for i in range(len(texts)):
        for symbol in ["\n", "&nbsp;"]:
            texts[i] = texts[i].replace(symbol, "")
        texts[i] = texts[i][:texts[i].rfind(".") + 1]
    return texts[0] + "\n\n" + texts[1]