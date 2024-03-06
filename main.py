from kivy.lang import Builder
from kivy.app import App
from confirmacao_de_consulta import confirmarConsultas, resulucao_de_erros_confirmacao_de_consultas
from vencimento_vacina import vencimentoVacina, resulucao_de_erros_vencimentoVacina
from agenda_diaria_adm import agendaAdm, resulucao_de_erros_agendaAdm
from conexao_whatsAppWeb import conexaoWhatsAppWeb

GUI = Builder.load_file('tela.kv')

class Automacao(App):
    def build(self):
        return GUI
    
    def conexao_whatsAppWeb(self):
        conexaoWhatsAppWeb()
    
    def confirmar_consulta(self):
        mensagem = confirmarConsultas()
        mensagem_completa = "\n".join(mensagem)
        self.root.ids.lbl_mensagem_consulta.text = mensagem_completa
    
    def vencimento_vacina(self):
        mensagem2 = vencimentoVacina()
        mensagem_completa2 = "\n".join(mensagem2)
        self.root.ids.lbl_mensagem_vacina.text = mensagem_completa2

    def agenda_adm(self):
        mensagem3 = agendaAdm()
        mensagem_completa3 = "\n".join(mensagem3)
        self.root.ids.lbl_agenda_adm.text = mensagem_completa3

    def resolucao_erros(self):
        mensagem4 = resulucao_de_erros_confirmacao_de_consultas()
        mensagem_completa4 = "\n".join(mensagem4)
        self.root.ids.lbl_mensagem_erros.text = mensagem_completa4

    def resolucao_erros_vacina(self):
        mensagem5 = resulucao_de_erros_vencimentoVacina()
        mensagem_completa5 = "\n".join(mensagem5)
        self.root.ids.lbl_mensagem_erros_vacina.text = mensagem_completa5

    def resolucao_erros_agenda(self):
        mensagem6 = resulucao_de_erros_agendaAdm()
        mensagem_completa6 = "\n".join(mensagem6)
        self.root.ids.lbl_mensagem_erros_agenda.text = mensagem_completa6

Automacao().run()

