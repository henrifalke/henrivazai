import requests
import json

class OnlineSpellChecker:
    def __init__(self):
        self.base_url = "https://api.languagetool.org/v2/check"

    def check_text(self, text):
        params = {
            'text': text,
            'language': 'pt-BR',
            'enabledOnly': 'false'
        }

        response = requests.post(self.base_url, data=params)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result['matches']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

def analyze_text(text, checker):
    results = checker.check_text(text)
    misspelled = []
    for error in results:
        if error['rule']['category']['id'] == 'TYPOS':
            misspelled.append(error['context']['text'][error['offset']:error['offset']+error['length']])
    return misspelled

# Criar o verificador ortográfico online
checker = OnlineSpellChecker()

# Exemplo de uso
texto_para_analisar = "Este é um exmplo de textu com algun erros de ortografia e palavras como Organizasão."
erros = analyze_text(texto_para_analisar, checker)

print("\nTexto analisado:", texto_para_analisar)
print("Palavras possivelmente incorretas:", erros)

# Verificar palavras específicas
palavras_teste = ["exmplo", "textu", "algun", "erros", "ortografia", "Organizasão", "texto-base", "língua", "palavra"]
for palavra in palavras_teste:
    print(f"\nVerificando '{palavra}':")
    resultado = analyze_text(palavra, checker)
    esta_correto = len(resultado) == 0
    print(f"Resultado: {'Correto' if esta_correto else 'Incorreto'}")
