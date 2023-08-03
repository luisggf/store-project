import time
import random
import os
import io
import heapq
import shutil
import csv
import pandas as pd
from faker import Faker
#pip install faker

class Store:
    class Product:
        def __init__(self, code, name, price, quantity):
            self.code = code
            self.name = name
            self.price = price
            self.quantity = quantity

    class Customer:
        def __init__(self, name, Adress, phone, cpf):
            self.name = name
            self.Adress = Adress
            self.phone = phone
            self.cpf = cpf

    # possibilidade de execução em ram e contagem de saldo da loja
    def __init__(self):
        self.balance = 0.0


    # facilitação para criar clientes (uso em place_order)
    def create_customer(self):
        while True:
            name = input("Enter customer name: ")
            if not name:
                print("Name cannot be empty. Please try again.")
                continue
            name = name.capitalize()

            Adress = input("Enter customer Adress: ")

            phone = input("Enter customer phone: ")
            if not phone.isdigit():
                print("Phone must be a numeric value. Please try again.")
                continue

            cpf = input("Enter customer CPF: ")
            if not cpf.isdigit():
                print("CPF must be a numeric value. Please try again.")
                continue

            # Input validation successful
            return Store.Customer(name, Adress, int(phone), int(cpf))


    #@override   
    def create_customer_with_cpf(self, cpf):
        while True:
            name = input("Enter customer name: ")
            if not name:
                print("Name cannot be empty. Please try again.")
                continue
            name.capitalize()
            Adress = input("Enter customer Adress: ")
            
            phone = input("Enter customer phone: ")
            if not phone.isdigit():
                print("Phone must be a numeric value. Please try again.")
                continue
            
            # Input validation successful
            return Store.Customer(name, Adress, int(phone), cpf)
        
    # facilitação para criar clientes (uso em place_order)
    def create_product(self):
        while True:
            name = input("Enter customer name: ")
            if not name:
                print("Name cannot be empty. Please try again.")
                continue
            name.capitalize()

            code = input("Input the product code: ")
            if not code.isdigit():
                print("Code must be a numeric value. Please try again.")
                continue

            price = float(input("Input the product price: "))
            if type(price) != float:
                print("Price must be a numeric value. Please try again.")
                continue

            quantity = input("Input the product quantity avaliable: ")
            if not quantity.isdigit():
                print("CPF must be a numeric value. Please try again.")
                continue

            # Input validation successful
            return Store.Product(int(code),name, float(price), int(quantity))

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

    # acha produtos por codigo
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

    def binary_search_product(self, filename, code):
        self.sort_products_by_code(filename)
        comp = 0
        start_time = time.time()

        df = pd.read_csv(filename)
        df = df.sort_values(by=['Product Code'])

        left = 0
        right = len(df) - 1
        found = False

        while left <= right:
            mid = (left + right) // 2
            comp += 1

            if df.loc[mid, 'Product Code'] == code:
                found = True
                break
            elif df.loc[mid, 'Product Code'] < code:
                left = mid + 1
            else:
                right = mid - 1

        elapsed_time = time.time() - start_time

        if found:
            print()
            print(df.loc[mid])
        else:
            print("Product not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

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

        if not found:
            elapsed_time = time.time() - start_time
            print("Product not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

    def sequential_search_rom_clean(self, filename, code):
        found = False
        # prod_aux = self.Product()
        for chunk in pd.read_csv(filename, chunksize=15):
            result = chunk[chunk['Product Code'] == code]
            if not result.empty:
                found = True
                return result

        if not found:
            print("Product not found in the store.")

    def sequential_search_rom_clean_by_name(self, filename, name):
        found = False
        # prod_aux = self.Product()
        for chunk in pd.read_csv(filename, chunksize=15):
            result = chunk[chunk['Product Name'] == name]
            if not result.empty:
                found = True
                return result

        if not found:
            print("Product not found in the store.")


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
            print("5. Binary Search")
            print("6. Sort Products")
            print("7. Shuffle File")
            print("8. Generate Random Instruments")
            print("9. Sorted Partition Creation")
            print("10. Intercalation Sort")
            print("0. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                product = self.create_product()
                self.save_product_to_file(product, filename)

            elif choice == "2":
                product_code = int(input("Enter product code: "))
                self.remove_product_from_file(filename, product_code)

            elif choice == "3":
                self.read_file(filename)

            elif choice == "4":
                product_code = int(input("Enter product code to search: "))
                self.sequential_search_rom(filename, product_code)

            elif choice =="5":
                product_code = int(input("Enter product code to search: "))
                self.binary_search_product(filename,product_code)

            elif choice == "6":
                self.sort_products_by_code(filename)

            elif choice == "7":
                self.shuffle_file(filename)

            elif choice == "8":
                self.gen_random_instruments()

            elif choice == "9":
                chunk_size = int(input("Enter chunk size for partition creation: "))
                self.generate_ordered_partitions(filename, "partition", chunk_size)
            elif choice == "10":
                self.merge_partitions("./partitions/", "merge.csv")
            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

    # menu interativo para realizar pedidos
    def menu_order(self, filename_order):
        while True:
            print("\n=== ORDER MENU ===")
            print("1. Add Order")
            print("2. Remove Order")
            print("3. Print Order's List")
            print("4. Sequential Search")
            print("5. Binary Search")
            print("6. Sort Order Code")
            print("7. Shuffle")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                product_name = str(input("Input the product name you wish to buy: "))
                aux = self.sequential_search_rom_clean_by_name("products.csv", product_name)
                if aux is None:
                    return
                print("The product you searched: \n", aux, "\nif you wanna buy it please proceed.")
                costumer_cpf = int(input("Input the costumer CPF (if you don't wanna but it input -1): "))
                if costumer_cpf == -1:
                    print("Purchased cancelled!")
                    break
                quantity = int(input("Input the quantity you wish to buy: "))
                self.place_order(filename_order,aux.iloc[0]["Product Code"],costumer_cpf,quantity)

            elif choice == "2":
                order_code = int(input("Enter Order Code: "))
                self.remove_order_from_file(filename_order, order_code)

            elif choice == "3":
                print("Reading Order's file!")
                self.read_file(filename_order)
                print("Reading complete!")

            elif choice == "4":
                code = int(input("Input Order Code: "))
                self.sequential_search_rom_order(filename_order,code)

            elif choice == "5":
                code = int(input("Input Order Code: "))
                self.binary_search_order(filename_order,code)

            elif choice == "6":
                self.sort_order_by_code(filename_order)

            elif choice == "7":
                self.shuffle_file(filename_order)

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
            print("3. Read Customers List")
            print("4. Gen Random Custumers")
            print("5. Sequential Search")
            print("6. Binary Search")
            print("7. Sort by Alphabetical Order")
            print("8. Shuffle")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                customer = self.create_customer()
                self.save_costumer_to_file(customer, filename_costumer)

            elif choice == "2":
                customer_cpf = int(input("Costumer CPF: "))
                self.remove_costumer_from_file(filename_costumer, customer_cpf)

            elif choice == "3":
                self.read_file_costumer(filename_costumer)

            elif choice == "4":
                self.gen_random_costumers()

            elif choice == "5":
                cpf = int(input("Input your CPF: "))
                self.sequential_search_rom_costumer(filename_costumer,cpf)

            elif choice =="6":
                cpf = int(input("Input your CPF: "))
                self.binary_search_costumer_csv(filename_costumer,cpf)
            
            elif choice == "7":
                self.sort_customers_by_name(filename_costumer)

            elif choice == "8":
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

    #ordenação por cpf para busca binaria
    def sort_customers_by_cpf(self,filename):
        df = pd.read_csv(filename)
        df = df.sort_values(by=['Costumer CPF'])
        df.to_csv(filename, mode='w', index=False)

    #busca binaria por CPF
    def binary_search_costumer_csv(self, filename, cpf):
        self.sort_customers_by_cpf(filename)
        comp = 0
        start_time = time.time()

        df = pd.read_csv(filename)
        df = df.sort_values(by=['Costumer CPF'])

        left = 0
        right = len(df) - 1
        found = False

        while left <= right:
            mid = (left + right) // 2
            comp += 1

            if df.loc[mid, 'Costumer CPF'] == cpf:
                found = True
                break
            elif df.loc[mid, 'Costumer CPF'] < cpf:
                left = mid + 1
            else:
                right = mid - 1

        elapsed_time = time.time() - start_time

        if found:
            print()
            print(df.loc[mid])
        else:
            print("Customer not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

    # salva cliente no arquivo de clientes
    def save_costumer_to_file(self, costumer, filename_costumer):
        data = {
            "Costumer Name": [costumer.name],
            "Costumer CPF": [costumer.cpf],
            "Adress": [costumer.Adress],
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
    def remove_costumer_from_file(self, filename, cpf):
        try:
            df = pd.read_csv(filename)
            df = df[df['Costumer CPF'] != cpf]
            df.to_csv(filename, index=False)
            print(f"Customer '{cpf}' removed from '{filename}' successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    # encontra clientes por CPF
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
                    Adress=customer_row['Adress'],
                    phone=customer_row['Number']
                )
        # Se nenhum cliente for encontrado em todos os chunks
        return None

    # gera um numero 'len(costumer_names.txt)' de clientes para a loja [criação de dados]
    def gen_random_costumers(self):
        fake = Faker()
        for line in range(80):
            address = fake.address()
            truncated_address = address[:12]
            area_code = fake.random_element(["11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "24", "27", "28", "31", "32", "33", "34",
                "35", "37", "38", "41"]) 
            number = fake.random_int(min=1000000, max=9999999) 
            formatted_phone_number = f"({area_code}){9}{number}"

            var_clientes = self.Customer(fake.name(), truncated_address.replace(', ', '- '), formatted_phone_number, fake.unique.random_number(digits=11, fix_len=True))
            self.save_costumer_to_file(var_clientes, "costumer.csv")

    # retorna o cliente procurado por código por busca sequencial
    def sequential_search_rom_costumer(self, filename_costumer, code):
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

        if not found:
            elapsed_time = time.time() - start_time
            print("Costumer CPF not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

    
    # ordena clientes por nome
    def sort_customers_by_name(self, filename_costumer):
        df = pd.read_csv(filename_costumer)
        df = df.sort_values(by=['Costumer Name'])
        df.to_csv(filename_costumer, mode='w', index=False)


    ################################################# Funções relacionadas ao objeto Order

    # realiza Order de dado cliente
    def place_order(self, orders_file, product_code, costumer_cpf, quantity):
        rand = random.randint(1, 1000)

        product_aux = self.find_product_by_code("products.csv", product_code)
        costumer_aux = self.find_customer_by_cpf("costumer.csv", costumer_cpf)

        if product_aux.quantity == 0 or product_aux.quantity < quantity:
            print("All Products Sold Out!")
            return

        if costumer_aux is None:
            customer = self.create_customer()
            self.save_costumer_to_file(customer, "costumer.csv")
            costumer_aux = self.find_customer_by_cpf("costumer.csv", costumer_cpf)

        if product_aux is None:
            print("Couldn't find product!")
            return

        expense = float(product_aux.price * quantity)
        self.balance += expense

        if product_aux.quantity == 0 or product_aux.quantity < quantity:
            print("All Products Sold Out!")
            return

        product_aux.quantity -= quantity

        df = pd.read_csv("products.csv")
        df.loc[df["Product Code"] == product_code, "Quantity"] = product_aux.quantity
        df.to_csv("products.csv", index=False)

        data = {
            "Product Name": [product_aux.name],
            "Bought Quantity:": [quantity],
            "Customer Name": [costumer_aux.name],
            "Order Code": [rand],
            "Final Value": [expense]
        }
        df_order = pd.DataFrame(data)
        if os.path.isfile(orders_file):
            df_order.to_csv(orders_file, mode="a", index=False, header=False)
        else:
            df_order.to_csv(orders_file, mode="a", index=False)

        print(f"Order '{product_code}' saved to '{orders_file}' successfully.")
    

    # calcula o saldo da loja baseado na pilha de pedidos feitos 
    def calculate_total_final_value(self, filename):
        try:
            df = pd.read_csv(filename)
            total_final_value = float(df['Final Value'].sum())
            return float(total_final_value)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None
        
    def remove_order_from_file(self, filename, code):
        df = pd.read_csv(filename)
        df = df[df['Order Code'] != code]
        df.to_csv(filename, index=False)
        print(f"Order '{code}' removed from '{filename}' successfully.")

    def sequential_search_rom_order(self, filename_order, code):
        comp = 0
        start_time = time.time()
        found = False

        for chunk in pd.read_csv(filename_order, chunksize=15):
            comp += chunk.shape[0]
            result = chunk[chunk['Order Code'] == code]
            if not result.empty:
                found = True
                elapsed_time = time.time() - start_time
                print("Order Code in", comp, "comparisons and", elapsed_time, "seconds:")
                print()
                print(result)
                return result

        if not found:
            elapsed_time = time.time() - start_time
            print("Order Code not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")
    
    def binary_search_order(self, filename, code):
        self.sort_order_by_code(filename)
        comp = 0
        start_time = time.time()

        df = pd.read_csv(filename)
        df = df.sort_values(by=['Order Code'])

        left = 0
        right = len(df) - 1
        found = False

        while left <= right:
            mid = (left + right) // 2
            comp += 1

            if df.loc[mid, 'Order Code'] == code:
                found = True
                break
            elif df.loc[mid, 'Order Code'] < code:
                left = mid + 1
            else:
                right = mid - 1

        elapsed_time = time.time() - start_time

        if found:
            print()
            print(df.loc[mid])
        else:
            print("Order Code not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

    def sort_order_by_code(self, filename):
        df = pd.read_csv(filename)
        df = df.sort_values(by=['Order Code'])
        df.to_csv(filename, mode='w', index=False)

    def generate_ordered_partitions(self, input_filename, output_filename, M):
        # Leitura do arquivo CSV
        df = pd.read_csv(input_filename)

        # Variáveis de controle
        partition_number = 1
        reservatorio = []
        array = []
        A = 0
        ultimo_indice = len(df) - 1
        
        for index, line in df.iterrows():
        
            new_line = line['Product Code']

            if A < M:
                    #AQUI VAI LER M REGISTRO
                    array.append(new_line) 
                    A += 1
            else:

                #Caso a memoria não está toda preenchida.
                if len(array) != M: 
                     
                     # verifica se o valor gravado na partição é maior que a proxima linha
                     if new_line < min_product_code:
                        reservatorio.append(new_line)
                        
                        #Caso o reservatorio esteja cheio, vai colocar tudo na partição
                        if len(reservatorio) == M:  
                            #ORDENA RESERVATORIO
                            array.sort()
                            for a in array:
                                #escreve no arquivo o reservatorio ordenado
                                output_file.write(f"{a}\n")
                            output_file.close()
                            #transfere o reservatorio para a memoria
                            array = reservatorio
                            # zera o reservatorio
                            reservatorio = []
                            partition_number += 1 
                     else:
                        array.append(new_line)


                else:
                    # Pega o valor minimo
                    min_product_code = min(array) 
                    #Cria um novo arquivo
                    output_filename = f"./partitions/{partition_number}.csv" 
                    output_file = open(output_filename, "a")
                    output_file.write(f"{min_product_code}\n")
                    # Remove o valor minimo da memoria
                    array.remove(min_product_code)

                    # verifica se o valor gravado na partição é maior que a proxima linha
                    if new_line < min_product_code:
                        reservatorio.append(new_line)
                    else:
                        array.append(new_line)

                    # VEEFICIANDO se o reservatório está cheio
                    if len(reservatorio) == M:  
                        #ORDENA RESERVATORIO
                        array.sort()
                        for a in array:
                            #escreve no arquivo o reservatorio ordenado
                            output_file.write(f"{a}\n")
                        #transfere o reservatorio para a memoria
                        array = reservatorio
                        # zera o reservatorio
                        reservatorio = []
                        partition_number += 1

        #Caso o arquivo acabe e tenha conteudo no reservatorio ou na memoria
        if ultimo_indice == index:
            # Caso tenha conteudo na memoria ---------------# 
            array.sort()                                    #
            for a in array:                                 #
                output_file.write(f"{a}\n")                 #
            #-----------------------------------------------#

            #Caso tenha no reservatorio-------------------------------------------------#
            if len(reservatorio) != 0:                                                  #  
                reservatorio.sort()                                                     #
                partition_number += 1                                                   #
                # é preciso criar um novo arquivo, pois o reservatorio pode conter numeros menores que na partição#
                output_filename = f"./partitions/{partition_number}.csv"   #
                output_file = open(output_filename, "a")                                #
                for b in reservatorio:                                                  #
                    output_file.write(f"{b}\n")                                         #
            #---------------------------------------------------------------------------#
            output_file.close()


    def merge_partitions(self, input_prefix, output_filename):
        partition_number = 1
        merged_records = []

        while True:
            try:
                # Load the next partition
                partition_file = f"{input_prefix}partition{partition_number}.csv"
                with open(partition_file, "r") as file:
                    partition_records = [int(line.strip()) for line in file.readlines()]
                    merged_records.extend(partition_records)

                partition_number += 1
            except FileNotFoundError:
                # No more partitions to merge, break the loop
                break

        # Sort the merged records
        merged_records.sort()


        # Save the merged records to the output file
        with open(output_filename, "w") as output_file:
            for record in merged_records:
                output_file.write(str(record) + "\n")

        print(f"Partições unidas e ordenadas no arquivo '{output_filename}'.")

   
    def intercalation_sort(self, input_folder, output_file):
        input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith(".csv")]
        F = len(input_files)

        if F < 2:
            print("At least two partition files are required.")
            return

        output_partition = os.path.join(input_folder, "output_partition.csv")

        while len(input_files) > 1:
            partitions_to_merge = input_files[:F - 1]
            remaining_files = input_files[F - 1:]

            # Perform intercalation for F-1 partitions
            with open(output_partition, 'w') as output:
                heap = []

                # Open F-1 input partitions and initialize the heap with the first integer from each
                for file in partitions_to_merge:
                    with open(file, 'r') as f:
                        record = f.readline().strip()
                        if record:
                            heapq.heappush(heap, (int(record), f))

                # Merge the integers and write to the output partition
                while heap:
                    try:
                        record, file = heapq.heappop(heap)
                        output.write(str(record) + '\n')

                        next_record = file.readline().strip()
                        if next_record is not None:
                            heapq.heappush(heap, (int(next_record), file))
                    except ValueError:
                        # Ignore the ValueError when reaching the end of the file
                        pass

                # Remove merged partitions and add the newly created partition to the list
                for file in partitions_to_merge:
                    os.remove(file)

                shutil.move(output_partition, input_files[-1])

                # Update the list of input files for the next iteration
                input_files = remaining_files + [input_files[-1]]

            # Rename the final partition to the output file
            shutil.move(input_files[0], output_file)

        # Function to read a line from each input file
    def read_line(self, files, i):
        # Try to read a line from file i
        try:
            # Read the line and convert it to an integer
            value = int(files[i].readline())
            # Return the value and the index of the file
            return (value, i)
        # If an exception occurs (e.g., end of file)
        except:
            # Return None
            return None

    # Function to write a line to the output file
    def write_line(self, file, value, i):
        # Write the value and the index of the file separated by a comma
        file.write(f"{value},{i}\n")

    # Function to merge the sorted partitions
    def merge_partitions(self, input_folder, output_name):
        file_names = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith(".csv")]
        num_files = len(file_names)
        # Open the input files in read mode
        files = [open(name, "r") for name in file_names]
        # Open the output file in write mode
        output_file = open(output_name, "w")
        # Read the first line from each input file
        lines = [self.read_line(files, i) for i in range(num_files)]
        # Remove the None values from the list
        lines = [x for x in lines if x is not None]
        # While the list is not empty
        while lines:
            # Find the smallest value in the list and its corresponding file index
            smallest = min(lines)
            value, i = smallest
            # Write the smallest value to the output file
            self.write_line(output_file, value, i)
            # Read the next line from the file corresponding to the smallest value
            next_line = self.read_line(files, i)
            # If the next value is not None
            if next_line is not None:
                # Update the list with the new value and index
                lines[lines.index(smallest)] = next_line
            # Otherwise
            else:
                # Remove the value and index from the list
                lines.remove(smallest)
        # Close the input and output files
        for file in files:
            file.close()
        output_file.close()
        print("Sorted file has been saved as: ", output_name)
