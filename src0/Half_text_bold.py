import os
import re
import textract
import pdfkit
import math

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
input_txt_file = 'lecture0.txt'
output_html_file = 'lecture0.html'
output_pdf_file = 'lecture0.pdf'

# Processa o texto
text = read_txt_file(input_txt_file)
if text:  # só prossegue se conseguiu ler o arquivo
    bold_text = bold_half_words(text)

    # Cria o arquivo HTML
    create_html_file(output_html_file, bold_text)

    # Converte o arquivo HTML para PDF
    convert_html_to_pdf(output_html_file, output_pdf_file)
