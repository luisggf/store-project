# Importar pandas
import pandas as pd
df = pd.read_csv("products.csv")

# Criar um nó


class BTreeNode:
    def __init__(self, folha=False):
        self.folha = folha
        self.chaves = []
        self.filho = []

# Árvore B


class BTree:
    def __init__(self, t):
        self.raiz = BTreeNode(True)
        self.t = t

    # Inserir nó
    def inserir(self, k):
        raiz = self.raiz
        if len(raiz.chaves) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.raiz = temp
            temp.filho.insert(0, raiz)
            self.dividir_filho(temp, 0)
            self.inserir_nao_cheio(temp, k)
        else:
            self.inserir_nao_cheio(raiz, k)

    # Inserir quando não está cheio
    def inserir_nao_cheio(self, x, k):
        i = len(x.chaves) - 1
        if x.folha:
            x.chaves.append((None, None))
            while i >= 0 and k[0] < x.chaves[i][0]:
                x.chaves[i + 1] = x.chaves[i]
                i -= 1
            x.chaves[i + 1] = k
        else:
            while i >= 0 and k[0] < x.chaves[i][0]:
                i -= 1
            i += 1

            # Verifique se o índice i está dentro dos limites válidos
            if i < len(x.filho):
                if len(x.filho[i].chaves) == (2 * self.t) - 1:
                    self.dividir_filho(x, i)
                    if k[0] > x.chaves[i][0]:
                        i += 1
                self.inserir_nao_cheio(x.filho[i], k)
            else:
                # Se o índice i estiver fora dos limites, insira no último filho
                self.inserir_nao_cheio(x.filho[-1], k)

    # Dividir o filho
    def dividir_filho(self, x, i):
        t = self.t
        y = x.filho[i]
        z = BTreeNode(y.folha)
        x.filho.insert(i + 1, z)
        x.chaves.insert(i, y.chaves[t - 1])
        z.chaves = y.chaves[t: (2 * t) - 1]
        y.chaves = y.chaves[0: t - 1]
        if not y.folha:
            z.filho = y.filho[t: 2 * t]
            y.filho = y.filho[0: t - 1]

    # Imprimir a árvore
    def imprimir_arvore(self, x, l=0):
        print("Nível", l, " ", len(x.chaves), end=":")
        for i in x.chaves:
            print(i, end=" ")
        print()
        l += 1
        if len(x.filho) > 0:
            for i in x.filho:
                self.imprimir_arvore(i, l)

    # Buscar chave na árvore
    def buscar_chave(self, k, x=None):
        if x is not None:
            i = 0
            # Converta k e x.chaves[i][0] para int
            while i < len(x.chaves) and int(k) > int(x.chaves[i][0]):
                i += 1
            # Converta k e x.chaves[i][0] para int
            if i < len(x.chaves) and int(k) == int(x.chaves[i][0]):
                return (x, i)
            elif x.folha:
                return None
            else:
                return self.buscar_chave(k, x.filho[i])
        else:
            return self.buscar_chave(k, self.raiz)

    def criar_arvore(self, B):
        df = pd.read_csv("products.csv")
        # Criar uma árvore B com grau t=3
        # Inserir os dados do arquivo CSV na árvore B usando o Product Code como chave e o Product Name como valor
        for index, row in df.iterrows():
            B.inserir((row["Product Code"], row["Product Name"]))
        return B

    def buscar_codigo_arvore(self, B):
        # Buscar um produto pelo seu código na árvore B e imprimir o seu nome se encontrado
        produto = input("Digite o código do produto que deseja buscar: ")
        resultado = B.buscar_chave(produto)
        if resultado is not None:
            print("Produto encontrado:", resultado[0].chaves[resultado[1]][1])
        else:
            print("Produto não encontrado")
