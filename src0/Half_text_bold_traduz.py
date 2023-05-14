'''
Programa utilizado para 
'''


import os
import re
import textract
import pdfkit
import math

import openai
import os
import textwrap
import nltk

nltk.download('punkt')  # baixa os dados necessários para dividir o texto em frases

# Define a chave da API do OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define o tamanho máximo de cada chunk de texto (em número de caracteres)
MAX_CHUNK_SIZE = 4096

def split_text_into_chunks(text):
    sentences = nltk.tokenize.sent_tokenize(text)  # divide o texto em frases
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= MAX_CHUNK_SIZE:
            # Se a frase couber no chunk atual, adicione-a
            current_chunk += sentence + ' '
        else:
            # Se a frase não couber no chunk atual, comece um novo chunk
            chunks.append(current_chunk)
            current_chunk = sentence + ' '
    # Adicione o último chunk, se não estiver vazio
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def translate_text(text, source_lang, target_lang):
    chunks = split_text_into_chunks(text)
    translated_chunks = []
    for chunk in chunks:
        print('Texto enviado:',chunk)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Atue como um tradutor de livros. Quero que traduza todo o texto abaixo para português brasileiro, sem dizer mais nada:\n\n"+chunk,
            temperature=0.2,
            max_tokens=2500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print('A resposta foi: ',response )
        print("=========================================================")
        translated_chunks.append(response['choices'][0]['text'])
    return ''.join(translated_chunks)

def main():
    input_filename = 'lecture0.txt'
    output_filename = 'lecture0_ptbr.txt'

    # Lê o arquivo de entrada
    with open(input_filename, 'r') as f:
        text = f.read()

    # Traduz o texto
    translated_text = translate_text(text, 'en', 'pt-BR')

    # Escreve o texto traduzido no arquivo de saída
    with open(output_filename, 'w') as f:
        f.write(translated_text)

if __name__ == '__main__':
    main()





# Lê o arquivo .txt
def read_txt_file(filename):
    if os.path.isfile(filename):  # verifica se o arquivo existe
        text = textract.process(filename)
        return text.decode('utf-8')  # decodifica o objeto bytes para obter uma string
    else:
        print(f'O arquivo {filename} não foi encontrado.')
        return ''

# Altera a primeira metade das palavras para negrito
def bold_half_words(text):
    words = re.split('(\W)', text)  # divide o texto por palavras, preservando a pontuação
    new_words = []
    for word in words:
        if word.isalpha():  # se a 'palavra' é realmente uma palavra e não pontuação ou espaço
            split_index = math.ceil(len(word) / 2)  # calcula o índice onde a palavra deve ser dividida, arredondado para cima
            first_half = word[:split_index]
            second_half = word[split_index:]
            new_word = f'<b>{first_half}</b>{second_half}'  # coloca a primeira metade da palavra em negrito
        else:
            new_word = word
        new_words.append(new_word)
    return ''.join(new_words)

# Cria um arquivo HTML
def create_html_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)

# Converte o arquivo HTML para PDF
# Cria um arquivo HTML
def create_html_file(filename, text):
    lines = text.split('\n')  # divide o texto em linhas
    lines = [line + '<br>' for line in lines]  # adiciona a tag <br> ao final de cada linha
    text = '\n'.join(lines)  # junta as linhas novamente
    html = f'''
    <html>
    <head>
    <style>
    body {{ 
        font-family: "Tahoma"; 
        font-size: 12pt; 
        line-height: 2; 
        text-align: left;
    }}
    </style>
    </head>
    <body>
    {text}
    </body>
    </html>
    '''
    with open(filename, 'w') as f:
        f.write(html)


def convert_html_to_pdf(input_html, output_pdf):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file(input_html, output_pdf, configuration=config)

# Nomes dos arquivos
input_txt_file = 'lecture0_ptbr.txt'
output_html_file = 'lecture0_ptbr.html'
output_pdf_file = 'lecture0_ptbr.pdf'

# Processa o texto
text = read_txt_file(input_txt_file)
if text:  # só prossegue se conseguiu ler o arquivo
    bold_text = bold_half_words(text)

    # Cria o arquivo HTML
    create_html_file(output_html_file, bold_text)

    # Converte o arquivo HTML para PDF
    convert_html_to_pdf(output_html_file, output_pdf_file)
