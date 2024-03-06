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

# Informações de conexão acessadas no arquivo .env
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
agenda = []
agenda_erros = []

# telefone adm
telefone_admin = os.getenv("ADM_TELL")

# Estabelecer conexão e tratar os dados
def tratamento_de_dados_para_agenda_adm():
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        print("Conexao bem-sucedida!")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Schedulings;")
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            print("No momento nao foi encontrado nenhum agendamento")
        else:
            agendamentos_encontrados = False
            for linha in linhas:
                data_do_agendamento = linha[1]
                data_do_agendamento_formatada = data_do_agendamento.strftime("%d-%m-%Y")
                if data_do_agendamento_formatada == data_atual_formatada:
                    hora = linha[2]
                    pet = linha[3]
                    userId = linha[6]
                    cursor.execute("SELECT * FROM Users WHERE id=%s", (userId,))
                    linha_usuario = cursor.fetchone()
                    nome_usuario = linha_usuario[1]
                    telefone_usuario = linha_usuario[2]

                    # Criando um objeto com as informações e adicionando à lista
                    objeto_agendamento = {
                        'data': data_do_agendamento_formatada,
                        'hora': hora,
                        'pet': pet,
                        'nome': nome_usuario,
                        'telefone': telefone_usuario
                    }
                    agenda.append(objeto_agendamento)
                    agendamentos_encontrados = True
            conn.close()
            if not agendamentos_encontrados:
                print('Nao possui agendamentos')

    except mysql.connector.Error as e:
        print("Erro ao tratar os dados:", e)

def automacao_whats(agenda):
    global mensagens
    mensagens = []
    if len(agenda) == 0:
        mensagens.append('Não possui agendamento para o dia de hoje')
    else:
        # Concatenando as informações de todos os objetos da agenda em uma única mensagem
        mensagem = ''
        for objeto in agenda:
            mensagem += f' {objeto["hora"]} - {objeto["pet"]} do usuário {objeto["nome"]}\n'
        try:
            linkConfirmationWhats = f'https://web.whatsapp.com/send?phone=55{telefone_admin}&text={quote(mensagem)}'
            webbrowser.open(linkConfirmationWhats)
            sleep(20)
            seta = pyautogui.locateCenterOnScreen('seta.png')
            sleep(10)
            pyautogui.click(seta[0], seta[1])
            sleep(10)
            pyautogui.hotkey('ctrl', 'w')
            sleep(5)
            mensagens.append('Mensagem com a agenda do dia enviada com sucesso.')
        except Exception as e:
            mensagens.append('Não foi possível enviar a mensagem com a agenda do dia.')
        
        # Após o envio da mensagem, limpa o array agenda
        agenda.clear()

def agendaAdm():
    tratamento_de_dados_para_agenda_adm()
    automacao_whats(agenda)
    return mensagens

def resulucao_de_erros_agendaAdm():
    automacao_whats(agenda_erros)
    agenda_erros.clear()
    return mensagens