import gradio as gr
import spacy
from textstat import textstat
import torch
from transformers import BertForMaskedLM, BertTokenizer

# Carregar modelos
nlp = spacy.load("pt_core_news_sm")
model = BertForMaskedLM.from_pretrained("neuralmind/bert-base-portuguese-cased")
tokenizer = BertTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")

def analyze_grammar(text):
    # Implementação básica - você pode expandir isso
    doc = nlp(text)
    return "Análise gramatical: Implementação básica"

def check_spelling(text):
    # Implementação básica - você pode expandir isso
    return "Verificação ortográfica: Implementação básica"

def analyze_style(text):
    diversity = textstat.lexicon_count(text, removepunct=True) / len(text.split())
    avg_sentence_length = textstat.avg_sentence_length(text)
    return f"Diversidade lexical: {diversity:.2f}, Comprimento médio de frase: {avg_sentence_length:.2f}"

def generate_text(prompt, max_length=100):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def analyze_and_generate(text, is_premium):
    grammar_analysis = analyze_grammar(text)
    spelling_check = check_spelling(text)
    style_analysis = analyze_style(text)
    
    if is_premium:
        generated_text = generate_text(text[:100], max_length=200)
    else:
        generated_text = generate_text(text[:50], max_length=100)
    
    return f"{grammar_analysis}\n\n{spelling_check}\n\n{style_analysis}\n\nTexto Gerado: {generated_text}"

iface = gr.Interface(
    fn=analyze_and_generate,
    inputs=[
        gr.Textbox(label="Insira seu texto aqui"),
        gr.Checkbox(label="Versão Premium")
    ],
    outputs="text",
    title="Analisador de Texto e Gerador BERT",
    description="Analisa gramática, ortografia, estilo e gera texto baseado no prompt fornecido."
)

if __name__ == "__main__":
    iface.launch(share=True)
