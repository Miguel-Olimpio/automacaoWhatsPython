from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

import mysql.connector
import datetime
import webbrowser
from time import sleep
import pyautogui
from urllib.parse import quote

# Informações de conexão
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

data_atual = datetime.datetime.now()
data_atual_formatada = data_atual.strftime("%d-%m-%Y")
# data_atual_formatada = '24-02-2024'

# mensagem para exibir na interface do kivy
mensagens = []

# array que será utizado para o envio de mensagens
vencimentos = []
vencimentos_erros = []

def tratamento_de_dados_vencimento_vacina():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        print("Conexao bem-sucedida!")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VeterinaryRecords;")
        linhas = cursor.fetchall()

        if len(linhas) == 0:
            print("No momento nao foi encontrado nenhuma ficha veterinaria")
        else:
            vacinas_vencidas = False
            for linha in linhas:
                data_do_vencimento = linha[5]
                data_do_vencimento_formatada = data_do_vencimento.strftime("%d-%m-%Y")
                print(f'data de vencimento: {data_do_vencimento_formatada}')
                if data_do_vencimento_formatada == data_atual_formatada:
                    petId = linha[8]
                    cursor.execute("SELECT * FROM Pets WHERE id=%s", (petId,))
                    linha_pet = cursor.fetchone()
                    nome_pet = linha_pet[1]
                    userId = linha_pet[6]
                    cursor.execute("SELECT * FROM Users WHERE id=%s", (userId,))
                    linha_usuario = cursor.fetchone()
                    nome_usuario = linha_usuario[1]
                    telefone_usuario = linha_usuario[2]

                    # Criando um objeto com as informações e adicionando à lista
                    objeto_agendamento = {
                        'data': data_do_vencimento_formatada,
                        'hora': '',
                        'pet': nome_pet,
                        'nome': nome_usuario,
                        'telefone': telefone_usuario
                    }
                    vencimentos.append(objeto_agendamento)
                    vacinas_vencidas = True
            conn.close()
            if not vacinas_vencidas:
                print('Não possui vacinas vencidas')

    except mysql.connector.Error as e:
        print("Erro ao tratar os dados:", e)

def automacao_whats(vencimentos):
    global mensagens
    mensagens = []
    if len(vencimentos) == 0:
        mensagens.append('Não possui agendamento para o dia de hoje')
    else:
        for objeto in vencimentos:
            try:
                mensagem = f'Ola {objeto["nome"]} na saúde e bem estar do seu pet {objeto["pet"]}, A Dr Fiama Reis toma a liberdade de lembra-los, que a vacina do seu melhor amigo venceu no dia de hoje, caso deseje agendar um horário favor clicar no AgroPetReis-1924190082.us-east-1.elb.amazonaws.com'
                linkConfirmationWhats = f'https://web.whatsapp.com/send?phone=55{objeto["telefone"]}&text={quote(mensagem)}'
                webbrowser.open(linkConfirmationWhats)
                sleep(20) 
                seta = pyautogui.locateCenterOnScreen('seta.png')
                sleep(10)
                pyautogui.click(seta[0],seta[1])
                sleep(10)
                pyautogui.hotkey('ctrl','w')
                sleep(5)
                mensagens.append(f'Mensagem referente a vencimento de vacina enviada para {objeto["nome"]} no telefone {objeto["telefone"]} foi entregue com sucesso.')
            except Exception as e:
                mensagens.append(f'Não foi possível enviar mensagem para {objeto["nome"]} que possui o telefone {objeto["telefone"]}. Verifique se o telefone está\n'
                                 f'correto no formato (ddd)9******** (por exemplo: 32984769673). Caso o formato esteja correto, favor verificar se este\n'
                                 f'telefone é um telefone válido. Caso tudo esteja correto clique no botão Reenviar vencimento de vacinas\n')
                vencimentos_erros.append(objeto)
                continue  # Continue para o próximo objeto mesmo se ocorrer um erro

        # Após o envio das mensagens, limpa o array vencimentos
        vencimentos.clear()

def vencimentoVacina():
    tratamento_de_dados_vencimento_vacina()
    automacao_whats(vencimentos)
    return mensagens

def resulucao_de_erros_vencimentoVacina():
    automacao_whats(vencimentos_erros)
    vencimentos_erros.clear()
    return mensagens