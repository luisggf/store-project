from functools import partial
from heapq import merge
import time
import random
import os
import pandas as pd

class Store:
    class Product:
        def __init__(self, code, name, price, quantity):
            self.code = code
            self.name = name
            self.price = price
            self.quantity = quantity

    class Customer:
        def __init__(self, name, cep, phone, cpf):
            self.name = name
            self.cep = cep
            self.phone = phone
            self.cpf = cpf

    @staticmethod
    def create_customer(self):
        name = input("Enter customer name: ")
        cep = input("Enter customer CEP: ")
        phone = input("Enter customer phone: ")
        cpf = input("Enter customer CPF: ")
        return Store.Customer(name, cep, phone, cpf)


    def __init__(self):
        self.products_list = []
        self.customers = []
        self.orders = []
        self.balance = 0.0

    # adiciona produto no dicionario products_list, uso de ram
    def add_product(self, product):
        if any(prod.name == product.name for prod in self.products_list):
            print(f"Product '{product.name}' already exists in the store.")
        else:
            self.products_list.append(product)
            print(f"Product '{product.name}' added to the store.")

    # remove produto no dicionario products_list, uso de ram
    def remove_product(self, name):
        for product in self.products_list:
            if product.name == name:
                self.products_list.remove(product)
                print(f"Product '{name}' removed from the store.")
                return
        print(f"Product '{name}' does not exist in the store.")

    # imprime todos produtos da lista, uso de ram
    def print_products(self):
        print("Products in the store:")
        for product in self.products_list:
            print(f"Name: {product.name}, Code: {product.code}, Quantity: {product.quantity}, Price: {product.price}")

    # le o arquivo filename passado por parametro em chunks (pedaços de 30), uso de rom
    def read_file(self, filename):
        try:
            chunk_size = 30  # Define o tamanho do chunk desejado
            reader = pd.read_csv(filename, chunksize=chunk_size)
            for chunk in reader:
                # Realiza as operações desejadas com cada chunk
                print(chunk)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    # salva um produto passado como parametro no arquivo
    def save_product_to_file(self, product, filename):
        data = {
            "Product Name": [product.name],
            "Product Code": [product.code],
            "Quantity": [product.quantity],
            "Price": [product.price]
        }
        df = pd.DataFrame(data)
        if os.path.isfile(filename):
            df.to_csv(filename, mode='a', index=False, header=False)
        else:
            df.to_csv(filename, mode='a', index=False)
        print(f"Product '{product.name}' saved to '{filename}' successfully.")

    # remove um produto passado por parametro baseado em código de produto, no arquivo
    def remove_product_from_file(self, filename, code):
        df = pd.read_csv(filename)
        df = df[df['Product Code'] != code]
        df.to_csv(filename, index=False)
        print(f"Product '{code}' removed from '{filename}' successfully.")

    # realiza a busca sequencial de um codigo de produto no arquivo, retornando tempo gasto 
    # numero de comparações
    def sequential_search_rom(self, filename, code):
        comp = 0
        start_time = time.time()
        found = False
        # prod_aux = self.Product()
        for chunk in pd.read_csv(filename, chunksize=15):
            comp += chunk.shape[0]
            result = chunk[chunk['Product Code'] == code]
            if not result.empty:
                found = True
                elapsed_time = time.time() - start_time
                print("Product found in", comp, "comparisons and", elapsed_time, "seconds:")
                print(result)
                return result
                break

        if not found:
            elapsed_time = time.time() - start_time
            print("Product not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")


    # ordena produtos de arquivo por codigo de produto
    def sort_products_by_code(self, filename):
        df = pd.read_csv(filename)
        df = df.sort_values(by=['Product Code'])
        df.to_csv(filename, mode='w', index=False)

    def shuffle_file(self, filename):
        with pd.read_csv(filename, chunksize=6) as reader:
            chunks = []
            for chunk in reader:
                chunks.append(chunk)
            df = pd.concat(chunks)
        df = df.sample(frac=1).reset_index(drop=True)
        df.to_csv(filename, mode='w', index=False)

    # gera len(names.txt) instrumentos (produtos) [geração de dados]
    def gen_random_instruments(self):
        code = 0
        with open('names.txt', 'r') as file:
            content = file.readlines()
        random.shuffle(content)
        for line in content:
            cleaned_line = line.rstrip()
            random_float = round(random.uniform(20, 1000), 2)
            random_integer = random.randint(0, 20)
            var_product = self.Product(code, cleaned_line, random_float, random_integer)
            self.add_product(var_product)
            code += 1
            self.save_product_to_file(var_product, "products.csv")

    # particiona o arquivo maior em arquivos menores de forma ordenada
    def sorted_partition_creation_ROM(self, filename, chunk_size):
        partition_counter = 1
        partitions = []
        chunk = []
        self.sort_products_by_code(filename)
        for _, row in pd.read_csv(filename).iterrows():
            chunk.append(row)
            if len(chunk) >= chunk_size:
                chunk = sorted(chunk, key=lambda x: x['Product Code'])
                partitions.append(chunk)
                partition_filename = f'./partitions/sorted-partition-{partition_counter}.csv'
                pd.DataFrame(chunk).to_csv(partition_filename, index=False)
                partition_counter += 1
                chunk = []
        if chunk:
            chunk = sorted(chunk, key=lambda x: x['Product Code'])
            partitions.append(chunk)
            partition_filename = f'./partitions/sorted-partition-{partition_counter}.csv'
            pd.DataFrame(chunk).to_csv(partition_filename, index=False)
        return partitions

    # menu de manutenção dos produtos para maior acessibilidade para o usuario
    def menu_product(self, filename):
        while True:
            print("\n=== PRODUCT MENU ===")
            print("1. Add Product")
            print("2. Remove Product")
            print("3. Read File")
            print("4. Sequential Search")
            print("5. Sort Products")
            print("6. Shuffle File")
            print("7. Generate Random Instruments")
            print("8. Sorted Partition Creation")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                product_name = input("Enter product name: ")
                product_code = int(input("Enter product code: "))
                product_quantity = int(input("Enter product quantity: "))
                product_price = float(input("Enter product price: "))
                product = self.Product(product_code, product_name, product_price, product_quantity)
                self.add_product(product)
                self.save_product_to_file(product, filename)

            elif choice == "2":
                product_code = int(input("Enter product code: "))
                self.remove_product_from_file(filename, product_code)

            elif choice == "3":
                self.read_file(filename)

            elif choice == "4":
                product_code = int(input("Enter product code to search: "))
                self.sequential_search_rom(filename, product_code)

            elif choice == "5":
                self.sort_products_by_code(filename)

            elif choice == "6":
                self.shuffle_file(filename)

            elif choice == "7":
                self.gen_random_instruments()

            elif choice == "8":
                chunk_size = int(input("Enter chunk size for partition creation: "))
                self.sorted_partition_creation_ROM(filename, chunk_size)

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

    def menu_order(self, filename_order):
        while True:
            print("\n=== CUSTOMER MENU ===")
            print("1. Add Order")
            print("2. Print Order's List")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                codigo_prod = int(input("Digite o codigo do produto: "))
                cliente_CPF = int(input("Digite o CPF do cliente: "))
                quantity = int(input("Digite a quantidade: "))
                self.place_order(filename_order,codigo_prod,cliente_CPF,quantity)

            elif choice == "2":
                print("Reading Order's file!")
                self.read_file(filename_order)
                print("Reading complete!")

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")
    # menu de manutenção dos clientes para maior acessibilidade para o usuario
    def menu_customer(self, filename_costumer):
        while True:
            print("\n=== CUSTOMER MENU ===")
            print("1. Add Customer")
            print("2. Remove Customer")
            print("3. List Customer's")
            print("4. Gen Random Custumers")
            print("5. Sequential Search")
            print("6. Ordem Alfabética")
            print("7. Shuffle")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                customer_name = input("Enter customer name: ")
                customer_address = input("Enter customer CEP: ")
                customer_phone = input("Enter customer phone: ")
                customer_cpf = input("Enter customer CPF: ")
                customer = self.Customer(customer_name, customer_address, customer_phone, customer_cpf)
                self.save_costumer_to_file(customer, filename_costumer)

            elif choice == "2":
                customer_cpf = int(input("Costumer CPF: "))
                self.remove_costumer_from_file(filename_costumer, customer_cpf)

            elif choice == "3":
                self.read_file_costumer(filename_costumer)

            elif choice == "4":
                self.gen_random_costumers()

            elif choice == "5":
                cpf = int(input("INPUT CPF: "))
                self.sequential_search_rom_cliente(filename_costumer,cpf)
            
            elif choice == "6":
                self.sort_customers_by_name(filename_costumer)

            elif choice == "7":
                self.shuffle_file(filename_costumer)

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

    # menu geral que engloba menus de pedidos, produtos e clientes, além de informações da loja
    def main_menu(self):
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Product Menu")
            print("2. Customer Menu")
            print("3. Order Menu")
            print("4. Current Store Balance")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.menu_product("products.csv")

            elif choice == "2":
                self.menu_customer("costumer.csv")

            elif choice == "3":
                self.menu_order("order.csv")

            elif choice == "4":     
                print("Current store balance: ", self.calculate_total_final_value("order.csv"))
            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")


################################### funções relacionadas ao objeto cliente

    # salva cliente no arquivo de clientes
    def save_costumer_to_file(self, costumer, filename_costumer):
        data = {
            "Costumer Name": [costumer.name],
            "Costumer CPF": [costumer.cpf],
            "CEP": [costumer.cep],
            "Number": [costumer.phone]
        }
        df = pd.DataFrame(data)
        if os.path.isfile(filename_costumer):
            df.to_csv(filename_costumer, mode='a', index=False, header=False)
        else:
            df.to_csv(filename_costumer, mode='a', index=False)
        print(f"Product '{costumer.name}' saved to '{filename_costumer}' successfully.")

    # le arquivo de clientes, os imprimindo na tela
    def read_file_costumer(self, filename_costumer):
        try:
            chunk_size = 30  # Define o tamanho do chunk desejado
            reader = pd.read_csv(filename_costumer, chunksize=chunk_size)
            for chunk in reader:
                # Realiza as operações desejadas com cada chunk
                print(chunk)
        except FileNotFoundError:
            print(f"File '{filename_costumer}' not found.")

    # remove cliente do arquivo baseado em cpf
    def remove_costumer_from_file(self, filename_costumer, cpf):
        df = pd.read_csv(filename_costumer)
        df = df[df['Costumer CPF'] != cpf]
        df.to_csv(filename_costumer, index=False)
        print(f"Costumer '{cpf}' removed from '{filename_costumer}' successfully.")



    # gera um numero 'len(costumer_names.txt)' de clientes para a loja [criação de dados]
    def gen_random_costumers(self):
        with open('custumer_names.txt', 'r', encoding="utf-8") as file:
            content = file.readlines()
        random.shuffle(content)
        for line in content:
            cleaned_line = line.rstrip()
            cleaned_end = random.randint(10000, 99999) + random.randint(100, 999)
            random_number = random.randint(10, 55) + random.randint(100000000, 999999999)
            random_cpf = random.randint(100, 999) + random.randint(100, 999) + random.randint(100, 999) + random.randint(10, 99)
            var_clientes = self.Customer(cleaned_line, cleaned_end, random_number, random_cpf)
            # self.add_product(var_clientes)
            self.save_costumer_to_file(var_clientes, "costumer.csv")

    def sequential_search_rom_cliente(self, filename_costumer, code):
        comp = 0
        start_time = time.time()
        found = False

        for chunk in pd.read_csv(filename_costumer, chunksize=15):
            comp += chunk.shape[0]
            result = chunk[chunk['Costumer CPF'] == code]
            if not result.empty:
                found = True
                elapsed_time = time.time() - start_time
                print("Costumer CPF in", comp, "comparisons and", elapsed_time, "seconds:")
                print()
                print(result)
                return result
                break

        if not found:
            elapsed_time = time.time() - start_time
            print("Costumer CPF not found in the store.")

        print()
        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

    def sort_customers_by_name(self, filename_costumer):
        df = pd.read_csv(filename_costumer)
        df = df.sort_values(by=['Costumer Name'])
        df.to_csv(filename_costumer, mode='w', index=False)


    ################################################# Funções relacionadas ao objeto Order

    # realiza Order de dado cliente
    def place_order(self, filename_pedidos, codigo_prod, cliente_CPF, quantity):
        rand = random.randint(1, 1000)

        P = self.find_product_by_code("products.csv", codigo_prod)
        C = self.find_customer_by_cpf("costumer.csv", cliente_CPF)

        if C is None:
            print("Couldn't find customer!")
            C = self.create_customer()
        if P is None:
            print("Couldn't find product!")
            return

        expense = P.price * quantity
        self.balance += expense

        if P.quantity == 0 or P.quantity < quantity:
            print("All Products Sold Out!")
            return

        P.quantity -= quantity
        # self.save_product_to_file(P, "products.csv")

        # Update quantity in the file
        df = pd.read_csv("products.csv")
        df.loc[df["Product Code"] == codigo_prod, "Quantity"] = P.quantity
        df.to_csv("products.csv", index=False)

        data = {
            "Product Name": [P.name],
            "Bought Quantity:": [quantity],
            "Customer Name": [C.name],
            "Order Code": [rand],
        }

        df_order = pd.DataFrame(data)
        if os.path.isfile(filename_pedidos):
            df_order.to_csv(filename_pedidos, mode="a", index=False, header=False)
        else:
            df_order.to_csv(filename_pedidos, mode="a", index=False)

        print(f"Order '{codigo_prod}' saved to '{filename_pedidos}' successfully.")



    #achar cliente por CPF
    def find_customer_by_cpf(self, filename, cpf, chunksize=1000):
        # Abrir o arquivo CSV em partes menores (chunks)
        for chunk in pd.read_csv(filename, chunksize=chunksize):
            # Filtrar o chunk atual pelo CPF do cliente
            customer_chunk = chunk[chunk['Costumer CPF'] == cpf]
            
            # Verificar se há clientes encontrados no chunk
            if not customer_chunk.empty:
                # Retornar o primeiro cliente encontrado
                customer_row = customer_chunk.iloc[0]
                return self.Customer(
                    name=customer_row['Costumer Name'],
                    cpf=customer_row['Costumer CPF'],
                    cep=customer_row['Adress'],
                    phone=customer_row['Number']
                )
        
        # Se nenhum cliente for encontrado em todos os chunks
        return None
    
    #achar produto por codigo
    def find_product_by_code(self, filename, cod, chunksize=1000):
        # Abrir o arquivo CSV em partes menores (chunks)
        for chunk in pd.read_csv(filename, chunksize=chunksize):
            # Filtrar o chunk atual pelo CPF do cliente
            product_chunk = chunk[chunk['Product Code'] == cod]
            # Verificar se há clientes encontrados no chunk
            if not product_chunk.empty:
                # Retornar o primeiro cliente encontrado
                product_row = product_chunk.iloc[0]
                return self.Product(
                    name=product_row['Product Name'],
                    code=product_row['Product Code'],
                    quantity=product_row['Quantity'],
                    price=product_row['Price']
                )
        
        # Se nenhum cliente for encontrado em todos os chunks
        return None
    
    def calculate_total_final_value(self, filename):
        try:
            df = pd.read_csv(filename)
            total_final_value = df['Final Value'].sum()
            return float(total_final_value)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None