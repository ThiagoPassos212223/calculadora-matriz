import os
import sys
from fractions import Fraction

def limparTela():
    comando = "cls" if "win" in sys.platform else "clear"
    input("Pressione Enter para continuar...")
    os.system(comando)

def receberNumero(mensagem, fracao=False):
    while True:
        numero = input(mensagem)
        if numero.lower() == "sair":
            print("Operação cancelada.")
            exit()
        try:
            if fracao:
                return Fraction(numero)
            else:
                return int(numero)
        except:
            if fracao:
                print("Erro! Digite um número inteiro ou fração como 3/4")
            else: 
                print("Erro! Insira um número inteiro!")
                
def mostrarMatriz(matriz, titulo=""):
    if titulo:
        print(titulo)
    for linha in matriz:
        print("[", end=" ")
        for coluna in linha:
            print(f"{str(coluna):>7}", end=" ")
        print("]")
    print("-" * 30)

class MatrizComum:
    def __init__(self):
        self.matriz = []

    def adicionarElementos(self):
        self.numero_linhas = receberNumero("Insira o número de linhas: ")
        self.numero_colunas = receberNumero("Insira o número de colunas: ")

        for numero_linha in range(self.numero_linhas):
            elemento = []
            for numero_coluna in range(self.numero_colunas):
                elemento.append(receberNumero(f"Insira o elemento ({numero_linha},{numero_coluna}): ", True))
            self.matriz.append(elemento)

    def encontrarDeterminante(self):
        determinante = 1
        for n in range(self.numero_linhas):
            determinante *= self.matriz[n][n]
        
        # Aplica o efeito das trocas de linha
        determinante *= (-1) ** self.trocas_linha

        if self.valores_usados != 0:
            self.determinante = determinante / self.valores_usados
        else:
            self.determinante = 0

    def escalonar(self):
        self.valores_usados = 1
        self.trocas_linha = 0  # Conta quantas trocas de linha ocorreram
        mostrarMatriz(self.matriz, "Matriz original:")

        for posicao_pivo in range(self.numero_linhas - 1):
            pivo = self.matriz[posicao_pivo][posicao_pivo]
            
            # Se o pivô for zero, tenta trocar com uma linha abaixo
            if pivo == 0:
                for i in range(posicao_pivo + 1, self.numero_linhas):
                    if self.matriz[i][posicao_pivo] != 0:
                        print(f"Trocando linha {posicao_pivo + 1} com linha {i + 1}")
                        self.matriz[posicao_pivo], self.matriz[i] = self.matriz[i], self.matriz[posicao_pivo]
                        self.trocas_linha += 1
                        pivo = self.matriz[posicao_pivo][posicao_pivo]
                        break
                else:
                    print("Pivô zero detectado, não foi possível trocar linhas.")
                    continue

            for numero_linha in range(posicao_pivo + 1, self.numero_linhas):
                fator_eliminacao = -self.matriz[numero_linha][posicao_pivo]
                self.valores_usados *= pivo

                linha_pivo = self.matriz[posicao_pivo]
                linha_alvo = self.matriz[numero_linha]

                print(f"Operação: L{posicao_pivo + 1} * ({fator_eliminacao}) + L{numero_linha + 1} * ({pivo})")

                for numero_coluna in range(self.numero_colunas):
                    resultado = (linha_pivo[numero_coluna] * fator_eliminacao) + (linha_alvo[numero_coluna] * pivo)
                    self.matriz[numero_linha][numero_coluna] = resultado

            mostrarMatriz(self.matriz, f"Matriz (passo {posicao_pivo + 1}):")

    def resolverSistema(self):
        self.resultado = [0 for _ in range(self.numero_linhas)]

        for i in range(self.numero_linhas - 1, -1, -1):
            soma = 0
            for j in range(i + 1, self.numero_colunas - 1):
                soma += self.matriz[i][j] * self.resultado[j]
            coef = self.matriz[i][i]
            termo_independente = self.matriz[i][-1]

            if coef == 0:
                if termo_independente - soma != 0:
                    print("Sistema impossível!")
                    return
                else:
                    print(f"Infinitas soluções para a variável x{i}")
                    self.resultado[i] = 0
            else:
                self.resultado[i] = (termo_independente - soma) / coef

    def mostrarSolucao(self):
        mostrarMatriz(self.matriz, "Matriz resolvida:")
        
        self.encontrarDeterminante()
        print(f"Determinante = {self.determinante}")
        print("\nSoluções:")
        for i, valor in enumerate(self.resultado):
            print(f"x{i+1} = {valor}")

class MatrizInversa:
    def __init__(self):
        self.elementos = []

    def adicionarElementos(self):
        while True:
            print("Propriedades da matriz")
            self.numero_linhas = receberNumero("Número de linhas: ")
            self.numero_colunas = receberNumero("Número de colunas: ")

            if self.numero_linhas != self.numero_colunas:
                print("Erro: matriz não quadrada não pode ter inversa!")
            else:
                break

        print("Elementos da matriz:")
        for i in range(self.numero_linhas):
            linha = []
            for j in range(self.numero_colunas):
                valor = receberNumero(f"Elemento ({i},{j}): ")
                linha.append(Fraction(valor))
            self.elementos.append(linha)

        identidade = self.matrizIdentidade()
        for i in range(self.numero_linhas):
            self.elementos[i].extend(identidade[i])

    def matrizIdentidade(self):
        identidade = []
        for i in range(self.numero_linhas):
            linha = [Fraction(int(i == j)) for j in range(self.numero_colunas)]
            identidade.append(linha)
        return identidade

    def escalonar(self):
        numero_linhas = self.numero_linhas
        m = len(self.elementos[0])
        mostrarMatriz([linha[:self.numero_colunas] for linha in self.elementos], "Matriz original:")

        for i in range(numero_linhas):
            print(f"----- Passo {i + 1}")
            pivo = self.elementos[i][i]
            if pivo == 0:
                for k in range(i + 1, numero_linhas):
                    if self.elementos[k][i] != 0:
                        print(f"Trocando linha {i + 1} por linha {k + 1}")
                        self.elementos[i], self.elementos[k] = self.elementos[k], self.elementos[i]
                        pivo = self.elementos[i][i]
                        break
                else:
                    print("Erro: a matriz não é invertível")
                    return

            print(f"Normalizando a linha {i + 1} com pivô = {pivo}")
            self.elementos[i] = [x / pivo for x in self.elementos[i]]

            for j in range(numero_linhas):
                if j != i:
                    fator = self.elementos[j][i]
                    print(f"Zerando elemento na linha {j + 1}, coluna {i + 1} com fator {fator}")
                    self.elementos[j] = [
                        self.elementos[j][k] - fator * self.elementos[i][k]
                        for k in range(m)
                    ]
            mostrarMatriz(self.elementos, f"Matriz (passo {i + 1}):")

    def exibirResultado(self):
        mostrarMatriz(self.elementos, "Resultado:")

    def extrairInversa(self):
        numero_linhas = self.numero_linhas
        mostrarMatriz(
            [linha[numero_linhas:] for linha in self.elementos],
            "Matriz inversa:"
        )

class Main:
    def __init__(self):
        while True:
            modo = input("a) Matriz comum    b) Matriz inversa    c) Sair \nEscolha o modo: ")
            if modo.lower() == "a":
                matriz = MatrizComum()
                matriz.adicionarElementos()
                matriz.escalonar()
                matriz.encontrarDeterminante()
                matriz.resolverSistema()
                matriz.mostrarSolucao()
            elif modo.lower() == 'b':
                matriz = MatrizInversa()
                matriz.adicionarElementos()
                matriz.escalonar()
                matriz.exibirResultado()
                matriz.extrairInversa()
            elif modo.lower() == 'c':
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Tente novamente.")
            limparTela()

Main()
