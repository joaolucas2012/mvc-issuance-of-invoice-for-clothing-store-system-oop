import tkinter as tk
from tkinter import messagebox
import Produto as prod
import NotaFiscal as NotFisc

# Criando a classe que constrói a janela principal
class LimitePrincipal():
    def __init__(self, raiz, controle):
        self.controle = controle
        self.raiz = raiz
        self.raiz.geometry("300x250")
        self.menubar = tk.Menu(self.raiz)
        self.produtoMenu = tk.Menu(self.menubar)
        self.NotaFiscalMenu = tk.Menu(self.menubar)
        self.sairMenu = tk.Menu(self.menubar)

        # Menu do produto
        self.produtoMenu.add_command(label = "Cadastrar", command = self.controle.cadastraProduto)
        self.produtoMenu.add_command(label = "Consultar", command = self.controle.consultaProduto)
        self.menubar.add_cascade(label = "Produto", menu = self.produtoMenu)

        # Menu da Nota Fiscal
        self.NotaFiscalMenu.add_command(label = "Criar", command = self.controle.criaNotaFiscal)
        self.NotaFiscalMenu.add_command(label = "Consultar", command = self.controle.consultaNotaFiscal)
        self.menubar.add_cascade(label = "Nota Fiscal", menu = self.NotaFiscalMenu)

        # Menu que salva as informações
        self.sairMenu.add_command(label = "Salvar tudo", command = self.controle.salvaDados)
        self.menubar.add_cascade(label = "Sair", menu = self.sairMenu)

        self.raiz.config(menu = self.menubar)

# Classe do controle principal que controla todas as operações do menu e da janela principal
class ControlePrincipal():       
    def __init__(self):
        self.raiz = tk.Tk()

        self.ctrlProduto = prod.CtrlProduto(self)
        self.ctrlNotaFiscal = NotFisc.CtrlNotaFiscal(self)
    
        self.limite = LimitePrincipal(self.raiz, self)

        self.raiz.title("Sistema para loja de confecções")
        self.raiz.geometry('500x200')

        self.raiz.mainloop()
    
    # Funções necessárias do Produto.py e da NotaFiscal.py
    def cadastraProduto(self):
        self.ctrlProduto.cadastraProduto()

    def consultaProduto(self):
        self.ctrlProduto.consultaProduto()
    
    def criaNotaFiscal(self):
        self.ctrlNotaFiscal.criaNotaFiscal()

    def consultaNotaFiscal(self):
        self.ctrlNotaFiscal.consultaNotaFiscal()
    
    # Função que salva todos os dados inseridos e fecha a janela principal
    def salvaDados(self):
        # Os produtos e notas fiscais são salvos
        self.ctrlProduto.salvaProdutos()
        self.ctrlNotaFiscal.salvaNotasFiscais()

        # O usuário é informado sobre o salvamento destas informações
        messagebox.showinfo('Sucesso', 'Informações salvas!\nSaindo...')

        # A janela principal é finalmente fechada
        self.raiz.destroy()

if __name__ == '__main__':
    c = ControlePrincipal()