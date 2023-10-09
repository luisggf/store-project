# Readme do Projeto

## Visão Geral
Este projeto é uma aplicação de linha de comando para gerenciar produtos, clientes e pedidos de uma loja. Ele oferece várias funcionalidades para manutenção e interação com esses conjuntos de dados. A aplicação é escrita em Python e depende algumas bibliotecas para sua funcionalidade.

## Dependências
Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- pandas
- faker
- random
- os
- io
- heapq
- shutil
- csv

Você pode instalar essas dependências usando o `pip` executando o seguinte comando:

```bash
pip install pandas faker
```

## Funcionalidades

### Gerenciamento de Produtos
O menu de produtos (`menu_product`) oferece as seguintes funcionalidades:

1. **Adicionar Produto**: Adicionar um novo produto à lista de produtos da loja.
2. **Remover Produto**: Remover um produto da lista de produtos pelo seu código.
3. **Ler Arquivo**: Exibir o conteúdo do arquivo de produtos.
4. **Busca Sequencial**: Procurar um produto usando busca sequencial pelo seu código.
5. **Busca Binária**: Procurar um produto usando busca binária pelo seu código.
6. **Ordenar Produtos**: Ordenar a lista de produtos pelo código do produto.
7. **Embaralhar Arquivo**: Embaralhar a ordem dos produtos no arquivo de produtos.
8. **Gerar Instrumentos Aleatórios**: Gerar instrumentos aleatórios e adicioná-los à lista de produtos.
9. **Criação de Partições Ordenadas**: Criar partições ordenadas a partir do arquivo de produtos.
10. **Ordenação por Intercalação**: Realizar ordenação por intercalação nas partições de produtos.

### Gerenciamento de Pedidos
O menu de pedidos (`menu_order`) oferece as seguintes funcionalidades:

1. **Adicionar Pedido**: Realizar um pedido de um produto especificando o nome do produto, CPF do cliente e quantidade.
2. **Remover Pedido**: Remover um pedido da lista de pedidos pelo seu código.
3. **Imprimir Lista de Pedidos**: Exibir o conteúdo do arquivo de pedidos.
4. **Busca Sequencial**: Procurar um pedido usando busca sequencial pelo seu código.
5. **Busca Binária**: Procurar um pedido usando busca binária pelo seu código.
6. **Ordenar por Código de Pedido**: Ordenar a lista de pedidos pelo código do pedido.
7. **Embaralhar**: Embaralhar a ordem dos pedidos no arquivo de pedidos.

### Gerenciamento de Clientes
O menu de clientes (`menu_customer`) oferece as seguintes funcionalidades:

1. **Adicionar Cliente**: Adicionar um novo cliente à lista de clientes.
2. **Remover Cliente**: Remover um cliente da lista de clientes pelo seu CPF.
3. **Ler Lista de Clientes**: Exibir o conteúdo do arquivo de clientes.
4. **Gerar Clientes Aleatórios**: Gerar dados de clientes aleatórios e adicioná-los à lista de clientes.
5. **Busca Sequencial**: Procurar um cliente usando busca sequencial pelo seu CPF.
6. **Busca Binária**: Procurar um cliente usando busca binária pelo seu CPF.
7. **Ordenar por Ordem Alfabética**: Ordenar a lista de clientes por nomes de clientes.
8. **Embaralhar**: Embaralhar a ordem dos clientes no arquivo de clientes.

### Menu Principal
O menu principal (`main_menu`) serve como ponto de entrada para a aplicação e permite navegar pelos menus de produtos, clientes e pedidos, além de verificar o saldo atual da loja.

## Como Executar
Para executar a aplicação, siga estas etapas:

1. Certifique-se de ter o Python e as dependências necessárias instaladas.
2. Salve este código em um arquivo Python, por exemplo, `gerenciamento_loja.py`.
3. Crie arquivos CSV vazios com os nomes `produtos.csv`, `clientes.csv` e `pedidos.csv` para armazenar os dados.
4. Execute o arquivo Python usando o seguinte comando:

```bash
python main.py
```

5. Siga as instruções na tela para navegar pelos menus e realizar várias ações.

## Armazenamento de Dados
A aplicação armazena dados de produtos, clientes e pedidos em arquivos CSV. Certifique-se de que esses arquivos existam no mesmo diretório que o script Python. Os nomes dos arquivos são os seguintes:

- `produtos.csv` para dados de produtos.
- `clientes.csv` para dados de clientes.
- `pedidos.csv` para dados de pedidos.
