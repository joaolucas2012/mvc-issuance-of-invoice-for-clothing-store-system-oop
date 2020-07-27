import tkinter as tk
from tkinter import messagebox
import os.path
import pickle

#Exceptions de tratamento#

# Caso o usuário não preencha todos os campos
class PreenchaTudo(Exception):
    pass

# Caso o código esteja repetido
class CodeRepetido(Exception):
    pass

# Caso o código seja inválido
class CodeInvalido(Exception):
    pass

# Caso a descrição seja repetida
class DescRepetida(Exception):
    pass

# Caso a descrição seja inválida
class DescricaoInvalida(Exception):
    pass

# Caso o valor seja inválido
class ValorInvalido(Exception):
    pass

# Caso o mesmo produto já tenha sido cadastrado
class ProdutoJaCadastrado(Exception):
    pass

# Caso o produto não exista
class ProdutoNaoExiste(Exception):
    pass

# Caso não haja produtos cadastrados
class NaoTemProdutos(Exception):
    pass

#Criando a classe Produto com seus métodos getters
class Produto:
    def __init__(self, codigo, descricao, valorUnitario):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__valorUnitario = valorUnitario

    def getCodigo(self):
        return self.__codigo
    
    def getDescricao(self):
        return self.__descricao

    def getValorUnit(self):
        return self.__valorUnitario

# Criando a classe janela para cadastro de produtos
class LimiteCadastraProduto(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('350x250')
        self.title('Cadastrar Produto')
        self.controle = controle

        # Frame para o código
        self.frameCode = tk.Frame(self)
        self.frameCode.pack()
        self.labelCode = tk.Label(self.frameCode, text = 'Informe o código:')
        self.labelCode.pack()
        self.inputCode = tk.Entry(self.frameCode, width = 20)
        self.inputCode.pack()

        # Frame para a descrição
        self.frameDesc = tk.Frame(self)
        self.frameDesc.pack()
        self.labelDesc = tk.Label(self.frameDesc, text = '\nInforme a descrição:')
        self.labelDesc.pack()
        self.inputDesc = tk.Entry(self.frameDesc, width = 30)
        self.inputDesc.pack()

        #Frame para o valor unitário
        self.frameValor = tk.Frame(self)
        self.frameValor.pack()
        self.labelValor = tk.Label(self.frameValor, text = '\nInforme o valor unitário:')
        self.labelValor.pack()
        self.inputValor = tk.Entry(self.frameValor, width = 20)
        self.inputValor.pack()
        self.labelSpace = tk.Label(self.frameValor, text = '\n')
        self.labelSpace.pack()

        # Frame para os botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # Botão cadastrar produto
        self.ButtonCadastrar = tk.Button(self.frameButton, text = 'Cadastrar', font = ('Negrito', 9))
        self.ButtonCadastrar.pack(side = 'left')
        self.ButtonCadastrar.bind("<Button>", controle.cadastraHandler)

        # Botão concluído (fecha a janela)
        self.ButtonConcluido = tk.Button(self.frameButton, text = 'Concluido', font = ('Negrito', 9))
        self.ButtonConcluido.pack(side = 'left')
        self.ButtonConcluido.bind("<Button>", controle.concluidoHandler)

# Criando a classe janela para consulta de produtos
class LimiteConsultaProduto(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('300x120')
        self.title('Consultar Produto')
        self.controle = controle

        # Frame para o código
        self.frameCode = tk.Frame(self)
        self.frameCode.pack()
        self.labelCode = tk.Label(self.frameCode, text = 'Informe o código: \n')
        self.labelCode.pack()
        self.inputCode = tk.Entry(self.frameCode, width = 20)
        self.inputCode.pack()
        self.labelSpace = tk.Label(self.frameCode, text = '\n')
        self.labelSpace.pack()

        # Frame para os botões
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        # Botão consultar produto
        self.ButtonConsultar = tk.Button(self.frameButton, text = 'Consultar', font = ('Negrito', 9))
        self.ButtonConsultar.pack(side = 'left')
        self.ButtonConsultar.bind("<Button>", controle.consultaHandler)

        # Botão cancelar consulta (fecha a janela)
        self.ButtonCancelar = tk.Button(self.frameButton, text = 'Concluido', font = ('Negrito', 9))
        self.ButtonCancelar.pack(side = 'left')
        self.ButtonCancelar.bind("<Button>", controle.cancelaHandler)

# Classe controle do Produto.py
class CtrlProduto():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal
        
        # Garantindo a persistência de arquivos
        if not os.path.isfile("produtos.pickle"):
            self.listaProdutos = []
        else:
            with open("produtos.pickle", "rb") as f:
                self.listaProdutos = pickle.load(f)

    # Método que salva todos os dados   
    def salvaProdutos(self):
        if len(self.listaProdutos) != 0:
            with open("produtos.pickle", "wb") as f:
                pickle.dump(self.listaProdutos, f) 
    
    # Método que cria messageboxes
    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
    
    # Método para averiguar se uma entrada é um valor numérico
    def isNumber(self, number):
        try:
            if number.isdigit() == True:
                return True
            float(number)
            return True
        except ValueError:
            return False
    
    # Método para pegar uma lista com os códigos de todos os produtos
    def getListaCodeProdutos(self):
        self.codigos = []
        for prod in self.listaProdutos:
            self.codigos.append(prod.getCodigo())
        return self.codigos
    
    # Método para pegar um produto pelo seu código
    def PegaProdutoPorCode(self, code):
        prodRet = None
        for prod in self.listaProdutos:
            if prod.getCodigo() == code:
                prodRet = prod
        return prodRet

    # Método que cria a janela Cadastro de Produto
    def cadastraProduto(self):
        self.limiteCad = LimiteCadastraProduto(self)
    
    # Método que cadastra um produto
    def cadastraHandler(self, event):
        try:
            # Antes de cadastrar, verifica se o código,
            # descrição e valor unitário são válidos
            code = self.limiteCad.inputCode.get()
            desc = self.limiteCad.inputDesc.get()
            value = self.limiteCad.inputValor.get()
            if len(code) == 0 or len(desc) == 0 or len(value) == 0:
                raise PreenchaTudo()
            if self.isNumber(code) == False or len(code.split(' ')) >= 2: 
                raise CodeInvalido()
            if len(desc) < 5 or self.isNumber(desc) == True:
                raise DescricaoInvalida()
            if len(value.split(' ')) >= 2 or self.isNumber(value) != True:
                raise ValorInvalido()
        # Tratamento das exceptions
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except CodeInvalido:
            str = 'Código inválido!\nO código deve ser um número inteiro e sem espaços.\nExemplos: 1001, 3456, ...'
            self.mensagem('Erro', str)
            self.limiteCad.inputCode.delete(0, len(self.limiteCad.inputCode.get()))
        except DescricaoInvalida:
            str = 'Descrição inválida!\nA descrição não deve conter números ou ter menos de 5 caracteres.'
            self.mensagem('Erro', str)
            self.limiteCad.inputDesc.delete(0, len(self.limiteCad.inputDesc.get()))
        except ValorInvalido:
            str = 'Valor inválido!\nO valor deve ser um número sem espaços entre um dígito e outro.\n'
            str += 'Exemplos válidos: 234, 700, 7685, ...'
            self.mensagem('Erro', str)
            self.limiteCad.inputValor.delete(0, len(self.limiteCad.inputValor.get()))      
        else:
            # Se tudo estiver correto, o cadastro é realizado

            # Pega-se os valores inseridos pelo usuário
            code = self.limiteCad.inputCode.get()
            desc = self.limiteCad.inputDesc.get()
            valor = float(self.limiteCad.inputValor.get())

            # Instancia-se uma classe com estes dados
            produto = Produto(code, desc, valor)

            try:
                # Verifica se o produto criado é igual a outro criado anteriormente
                for produt in self.listaProdutos:
                    if produt.getCodigo() == produto.getCodigo() and produt.getDescricao() == produto.getDescricao() and produt.getValorUnit() == produto.getValorUnit():
                        raise ProdutoJaCadastrado()
                    if produt.getCodigo() == produto.getCodigo():
                        raise CodeRepetido()
                    if produt.getDescricao() == produto.getDescricao():
                        raise DescRepetida()

            # Tratamento das exceptions
            except ProdutoJaCadastrado:
                self.mensagem('Erro', 'Produto já cadastrado!')
            except CodeRepetido:
                self.mensagem('Erro', 'Já existe outro produto com o mesmo código!')
            except DescRepetida:
                self.mensagem('Erro', 'Já existe outro produto com a mesma descrição!')
            
            else:
                # Se tudo estiver ok, a lista de produtos adiciona o novo produto
                self.listaProdutos.append(produto)

                # O usuário é notificado do sucesso no cadastro
                self.mensagem('Cadastro realizado', 'Produto cadastrado com sucesso!')

                # A janela é destruída
                self.limiteCad.destroy()
    
    # Função que fecha a janela de cadastro
    def concluidoHandler(self, event):
        self.limiteCad.destroy()
    
    # Função que cria a janela de consultar produtos
    def consultaProduto(self):
        try:
            # Verifica se a lista de produtos não está vazia
            if len(self.listaProdutos) != 0:

                # Se existir produtos cadastrados, a janela é criada
                self.limiteConsult = LimiteConsultaProduto(self)
            else:
                # Se não, o usuário é notificado sobre não haver produtos cadastrados
                raise NaoTemProdutos()

        # Tratamento da exception
        except NaoTemProdutos:
            self.mensagem('Erro', 'Não há produtos cadastrados!')       

    # Método que retorna um produto pelo seu código
    def getProdutoPorCodigo(self, code):
        prodRet = None
        for produto in self.listaProdutos:
            if produto.getCodigo() == code:
                prodRet = produto
        return prodRet 

    # Função que realiza a consulta de produtos
    def consultaHandler(self, event):
        try:
            # Verifica se o usuário digitou as informações
            if len(self.limiteConsult.inputCode.get()) == 0:
                raise PreenchaTudo()
        # Se não, é pedido para que ele as digite
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        else:
            # Se tudo estiver ok, pega-se as informações digitadas
            code = self.limiteConsult.inputCode.get()
            produto = self.getProdutoPorCodigo(code)
            try:
                # Verifica se o produto buscado existe
                if produto == None:
                    raise ProdutoNaoExiste()
            # Tratamento da exception
            except ProdutoNaoExiste:
                # Se o produto não existir, o usuário é notificado
                self.mensagem('Produto não encontrado', 'Não há nenhum produto cadastrado com este código!')  
                self.limiteConsult.inputCode.delete(0, len(self.limiteConsult.inputCode.get()))   
            else:
                # Se o produto existir, são exibidas suas respectivas informações
                str = 'Informações do produto consultado:\n'
                str += 'Descrição: ' + produto.getDescricao() + '\n'
                str += ('Valor unitário: R$ {}0\n'.format(produto.getValorUnit()))
                self.mensagem('Produto encontrado', str)

                # A janela de consulta é fechada
                self.cancelaHandler(event)
    
    # Função que fecha a janela de consulta
    def cancelaHandler(self, event):
        self.limiteConsult.destroy()              