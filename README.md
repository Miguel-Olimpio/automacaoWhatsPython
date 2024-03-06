#  Automação whatsPython

[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Miguel-Olimpio/automacaoWhatsPython/blob/main/LICENSE)

## IDEALIZAÇÃO DO PROJETO

O projeto se originou com o pedido de um cliente que necessitava enviar mensagens de forma automatica para seus clientes, no entanto a alternativa de criar um bot de whatsApp demonstrou ser pouco viável, logo foi feito um arquivo executavel em python que era capaz de ler os dados de um banco de dados e enviar as mensagens de forma automatica.

## Layout e modo de usar
Primeiramente é necessário inserir as configurações para seu banco de dados e mensagens que deseja enviar, posteriormente basta gerar o executável com o comando pyinstaller main.py -w.
Ao gerar o execútavel com o comando pyinstaller main.py -w, será criada uma pasta dist, a mesma deve conter os seguintes arquivos:

![imagePython1](https://github.com/Miguel-Olimpio/automacaoWhatsPython/assets/107503116/d77cbaad-002a-48fb-b500-13c8e5cbf542)

Após isto basta clicar no executável criado e utilizar.

![imagePython2](https://github.com/Miguel-Olimpio/automacaoWhatsPython/assets/107503116/6a155bc3-4052-4195-abc1-0a82056d76e5)

# Tecnologias utilizadas

## Back end
- Python

## Front end
- kivy

# Como executar o projeto

## Back end
Pré-requisitos: python 3.12.1

```bash
# clonar repositório
git clone https://github.com/Miguel-Olimpio/automacaoWhatsPython.git

# entrar na pasta do projeto back end
cd automacaoWhatsPython

# instalar dependências
pip install -r requirements.txt

# executar o projeto basta rodar 
python main.py
```

# Autor

Miguel Olimpio de Paula Netto

https://www.linkedin.com/in/miguel-olimpio-ba3220200/
