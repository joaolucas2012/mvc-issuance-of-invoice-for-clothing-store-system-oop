import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os.path
import pickle

#Exceptions de tratamento

# Caso o usuário não preencha todos os campos
class PreenchaTudo(Exception):
    pass

# Caso o número seja inválido
class NroInvalido(Exception):
    pass

# Caso o nome seja inválido
class NomeInvalido(Exception):
    pass

# Caso seja digitado um número ao invés de um nome
class NomeIsNumero(Exception):
    pass

# Caso o item seja repetido
class ItemRepetido(Exception):
    pass

# Caso tenha sido criada uma nota anteriormente que possua o mesmo código
class NotaComCodeRepetido(Exception):
    pass

# Caso a nota seja inexistente
class NotaInexistente(Exception):
    pass

# Criando a classe Nota Fiscal com seus métodos getters
class NotaFiscal:
    def __init__(self, numeroNF, nomeCliente):
        self.__numeroNF = numeroNF
        self.__nomeCliente = nomeCliente

        # A nota fiscal possui uma lista de produtos
        # Isto se torna uma agregação
        self.__itensNota = []

    def getNroNF(self):
        return self.__numeroNF
    
    def getNomeCliente(self):
        return self.__nomeCliente
    
    def getItens(self):
        return self.__itensNota
    
    # Método que adiciona um novo produto a lista de produtos da Nota fiscal
    def addItens(self, produto):
        self.__itensNota.append(produto)

# Criando a classe da janela de Criação de Notas Fiscais
class LimiteCriarNota(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('300x200')
        self.title('Criar Nota Fiscal')
        self.controle = controle

        # Frame para a nota
        self.frameNroNota = tk.Frame(self)
        self.frameNroNota.pack()
        self.labelNroNota = tk.Label(self.frameNroNota, text = 'Informe o número da nota: ')
        self.labelNroNota.pack()
        self.inputNroNota = tk.Entry(self.frameNroNota, width = 20)
        self.inputNroNota.pack()

        # Frame para o nome do cliente 
        self.frameNomeCli = tk.Frame(self)
        self.frameNomeCli.pack()
        self.labelNomeCli = tk.Label(self.frameNomeCli, text = 'Informe o nome do cliente: ')
        self.labelNomeCli.pack()
        self.inputNomeCli = tk.Entry(self.frameNomeCli, width = 20)
        self.inputNomeCli.pack()

        # Frame para a escolha dos produtos
        self.frameEscolhaProduto = tk.Frame(self)
        self.frameEscolhaProduto.pack()
        self.labelEscolha = tk.Label(self.frameEscolhaProduto, text = 'Escolha os produtos desejados:')
        self.labelEscolha.pack()
        self.escolhaProduto = tk.StringVar()
        self.comboProd = ttk.Combobox(self.frameEscolhaProduto, width = 20, textvariable = self.escolhaProduto)
        listaCodigos = controle.PegaListaCodes()

        # Combobox que contém os códigos de todos os produtos
        self.comboProd['values'] = listaCodigos
        self.comboProd.pack()

        # Frame para o botão Inserir Produto
        self.frameButton1 = tk.Frame(self)
        self.frameButton1.pack()

        # Frame para os demais botões
        self.frameButton2 = tk.Frame(self)
        self.frameButton2.pack()

        # Botão Inserir Produto
        self.ButtonInserir = tk.Button(self.frameButton1, text = 'Inserir Produto', font = ('Negrito', 9))
        self.ButtonInserir.pack()
        self.ButtonInserir.bind("<Button>", controle.insereProdutoHandler)

        # Botão que cria a Nota Fiscal
        self.ButtonCriar = tk.Button(self.frameButton2, text = 'Criar nota', font = ('Negrito', 9))
        self.ButtonCriar.pack(side = 'left')
        self.ButtonCriar.bind("<Button>", controle.criarHandler)

        # Botão que cancela a criação da Nota Fiscal (fecha a janela)
        self.ButtonCancelar = tk.Button(self.frameButton2, text = 'Cancelar', font = ('Negrito', 9))
        self.ButtonCancelar.pack(side = 'left')
        self.ButtonCancelar.bind("<Button>", controle.cancelaHandler)

# Criando a classe da janela de consultar notas fiscais
class LimiteConsultaNotaFiscal(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('300x120')
        self.title('Consultar Produto')
        self.controle = controle

        # Frame para o número da Nota Fiscal
        self.frameNroNota = tk.Frame(self)
        self.frameNroNota.pack()
        self.labelNroNota = tk.Label(self.frameNroNota, text = 'Informe o número da nota: \n')
        self.labelNroNota.pack()
        self.inputNroNota = tk.Entry(self.frameNroNota, width = 20)
        self.inputNroNota.pack()
        self.labelSpace = tk.Label(self.frameNroNota, text = '\n')
        self.labelSpace.pack()

        # Frame para os botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # Botão que consulta a Nota Fiscal
        self.ButtonConsultar = tk.Button(self.frameButton, text = 'Consultar nota', font = ('Negrito', 9))
        self.ButtonConsultar.pack(side = 'left')
        self.ButtonConsultar.bind("<Button>", controle.consultaHandler)

        # Botão que cancela a consulta
        self.ButtonCancelarConsulta = tk.Button(self.frameButton, text = 'Cancelar', font = ('Negrito', 9))
        self.ButtonCancelarConsulta.pack(side = 'left')
        self.ButtonCancelarConsulta.bind("<Button>", controle.cancelaConsultaHandler)

# Classe cotrole da NotaFiscal.py
class CtrlNotaFiscal():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal

        # Lista que recebe os itens inseridos na Nota Fiscal e as armazena temporariamente
        self.listaItensNota = []

        # Garantindo a persistência de arquivos
        if not os.path.isfile("notasFiscais.pickle"):
            self.listaNotasFiscais = []
        else:
            with open("notasFiscais.pickle", "rb") as f:
                self.listaNotasFiscais = pickle.load(f)

    # Método que salva todos os dados   
    def salvaNotasFiscais(self):
        if len(self.listaNotasFiscais) != 0:
            with open("notasFiscais.pickle", "wb") as f:
                pickle.dump(self.listaNotasFiscais, f) 
    
    # Método que cria messageboxes
    def mensagem(self, title, msg):
        messagebox.showinfo(title, msg)
    
    # Método que retorna uma lista com os códigos de todos os produtos para o combobox
    def PegaListaCodes(self):
        self.listaCodes = self.CtrlPrincipal.ctrlProduto.getListaCodeProdutos()
        return self.listaCodes

    # Método para averiguar se uma entrada é um valor numérico
    def isNumber(self, number):
        try:
            if number.isdigit() == True:
                return True
            float(number)
            return True
        except ValueError:
            return False
    
    # Método para averiguar se uma nota fiscal é duplicada
    def isNotaRepetida(self, number):
        for nota in self.listaNotasFiscais:
            if nota.getNroNF() == number:
                return True
            else:
                return False  

    # Método que cria a janela para Criar a Nota Fiscal
    def criaNotaFiscal(self):
        self.limiteCria = LimiteCriarNota(self)
    
    # Método que cria a janela para consultar a Nota Fiscal
    def consultaNotaFiscal(self):
        self.limiteConsult = LimiteConsultaNotaFiscal(self)
    
    # Função que insere os produtos na lista de itens da Nota Fiscal
    def insereProdutoHandler(self, event):
        try:
            # Verifica se os dados digitados pelo usuário são válidos
            nroNota = self.limiteCria.inputNroNota.get()
            nomeCli = self.limiteCria.inputNomeCli.get()
            escolhaProd = self.limiteCria.escolhaProduto.get()
            if len(nroNota) == 0 or len(nomeCli) == 0 or len(escolhaProd) == 0:
                raise PreenchaTudo()
            if self.isNumber(nroNota) == False or len(nroNota.split(' ')) >= 2:
                raise NroInvalido()
        # Tratamento das exceptions
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except NroInvalido:
            str = 'Número de nota fiscal inválido! O número deve ser inteiro e não deve haver espaços. '
            str += 'Números válidos: 1235, 45678, 59373, etc.'
            self.mensagem('Erro', str)
        else:
            # Se os dados inseridos forem válidos, estes dados são pegos
            produtoSel = escolhaProd
            produto = self.CtrlPrincipal.ctrlProduto.PegaProdutoPorCode(produtoSel)
            try:
                # Verifica se o mesmo produto já foi inserido anteriormente
                if produto in self.listaItensNota:
                    raise ItemRepetido()
            # Tratamento da exception
            except ItemRepetido:
                self.mensagem('Erro', 'Este produto já foi inserido nesta Nota Fiscal!')
            else:
                # Se não foi inserido ainda, este produto é inserido agora
                self.listaItensNota.append(produto)

                # O usuário é informado da inserção do produto realizada com sucesso
                self.mensagem('Inserção realizada', 'Item inserido na Nota Fiscal!')

    # Função que instancia o produto (cria)
    def criarHandler(self, event):
        try:
            # Verifica se os dados inseridos são válidos
            nroNota = self.limiteCria.inputNroNota.get()
            nomeCli = self.limiteCria.inputNomeCli.get()
            escolhaProd = self.limiteCria.escolhaProduto.get()
            if len(nroNota) == 0 or len(nomeCli) == 0 or len(escolhaProd) == 0:
                raise PreenchaTudo()
            if self.isNumber(nroNota) == False or len(nroNota.split(' ')) >= 2:
                raise NroInvalido()
            if self.isNumber(nomeCli) == True:
                raise NomeIsNumero()
            if len(nomeCli) < 2:
                raise NomeInvalido()
        # Tratamento das exceptions
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except NroInvalido:
            str = 'Número de nota fiscal inválido! O número deve ser inteiro e não deve haver espaços.'
            str += 'Números válidos: 1235, 45678, 59373, etc.'
            self.mensagem('Erro', str)
            self.limiteCria.inputNroNota.delete(0, len(self.limiteCria.inputNroNota.get()))
        except NomeIsNumero:
            str = "Nome inválido! Lembre-se: Um nome não pode ser um número."
            self.mensagem('Erro', str)
            self.limiteCria.inputNomeCli.delete(0, len(nomeCli))
        except NomeInvalido:
            str = "Nome inválido!"
            str += "\nUm nome não pode ser tão pequeno assim a ponto de ter só uma letra."
            self.mensagem('Erro', str)
            self.limiteCria.inputNomeCli.delete(0, len(nomeCli))
        else:
            # Se tudo estiver válido, os dados são pegos
            nroNota = nroNota
            nomeCli = nomeCli
            notaFisc = NotaFiscal(nroNota, nomeCli)
            try:
                # Verifica de esta nota não foi criada anteriormente
                if self.isNotaRepetida(notaFisc.getNroNF()) == True:
                    raise NotaComCodeRepetido()
            # Tratamento da exception
            except NotaComCodeRepetido:
                self.mensagem('Erro', 'Outra nota já criada possui este mesmo código!')
            else:
                # Se tudo estiver ok, a Nota Fiscal é finalmente criada

                # A Nota Fiscal adiciona os itens armazenados na lista de intens temporária
                # a sua lista de itens particular
                for item in self.listaItensNota:
                    notaFisc.addItens(item)
                self.listaNotasFiscais.append(notaFisc)

                # O usuário é notificado do sucesso na criação da Nota Fiscal
                self.mensagem('Sucesso', 'Nota Fiscal criada!')

                # A janela de criar Nota Fiscal é fechada
                self.cancelaHandler(event)
    
    # Método que retorna uma Nota Fiscal pelo número da mesma
    def PegaNotaPorNro(self, nro):
        NotaRet = None
        for nota in self.listaNotasFiscais:
            if nota.getNroNF() == nro:
                NotaRet = nota
        return NotaRet

    # Função que consulta a Nota Fiscal
    def consultaHandler(self, event):
        try:
            # Verifica se o usuário digitou um código válido
            NroNota = self.limiteConsult.inputNroNota.get()
            if len(NroNota) == 0:
                raise PreenchaTudo()
            if self.isNumber(NroNota) == False or len(NroNota.split(' ')) >= 2:
                raise NroInvalido()
            if self.PegaNotaPorNro(NroNota) == None:
                raise NotaInexistente()
        # Tratamento das exceptions
        except PreenchaTudo:
            self.mensagem('Erro', 'Digite um número primeiro!')
        except NroInvalido:
            str = 'Número de nota fiscal inválido! O número deve ser inteiro e não deve haver espaços.'
            str += 'Números válidos: 1235, 45678, 59373, etc.'
            self.mensagem('Erro', str)
            self.limiteConsult.inputNroNota.delete(0, len(self.limiteConsult.inputNroNota.get()))
        except NotaInexistente:
            self.mensagem('Número inválido', 'Não há nenhuma nota fiscal cadastrada com este número!')
            self.limiteConsult.inputNroNota.delete(0, len(self.limiteConsult.inputNroNota.get()))
        else:
            # Se os dados forem válidos, a consulta é realizada

            # Pega-se a nota pelo código fornecido
            nota = self.PegaNotaPorNro(NroNota)

            # Cria uma variável para a contagem do valor unitário de todos os produtos da lista da Nota Fiscal
            valorTotal = 0

            # Começa a fornecer as informações necessárias
            titulo = 'Nota Fiscal número ' + nota.getNroNF() + ' encontrada'
            str = 'Cliente: ' + nota.getNomeCliente() + '\n'
            str += 'Produtos adquiridos:\n\n'

            # Fornece as informações dos produtos
            for item in nota.getItens():

                # Ao mesmo tempo, a variável valorTotal armazena o valor unitário de cada produto
                # Somando-os, para cada produto no for loop
                valorTotal += item.getValorUnit()

                str += 'Código: ' + item.getCodigo() + '\n'
                str += 'Descrição: ' + item.getDescricao() + '\n'
                str += ('Valor unitário: R${}0\n\n'.format(item.getValorUnit()))
            str += ('Valor unitário total: R${}0'.format(valorTotal))

            # A janela de consulta é destruída
            self.limiteConsult.destroy()

            # Todas as informações são exibidas ao usuário
            self.mensagem(titulo, str)

    # Função que fecha a janela de criar Nota Fiscal
    def cancelaHandler(self, event):
        self.limiteCria.destroy()
    
    # Função que fecha a janela de consultar Nota Fiscal
    def cancelaConsultaHandler(self, event):
        self.limiteConsult.destroy()