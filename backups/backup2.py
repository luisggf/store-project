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
        def __init__(self, name, address, phone):
            self.name = name
            self.address = address
            self.phone = phone

    class Order:
        def __init__(self, order_number, products, total_value, customer):
            self.order_number = order_number
            self.products = products
            self.total_value = total_value
            self.customer = customer

    def __init__(self):
        self.products_list = []
        self.balance = 0
        self.orders = []

    # ram
    def add_product(self, product):
        if any(prod.name == product.name for prod in self.products_list):
            print(f"Product '{product.name}' already exists in the store.")
        else:
            self.products_list.append(product)
            print(f"Product '{product.name}' added to the store.")

    # ram
    def remove_product(self, name):
        for product in self.products_list:
            if product.name == name:
                self.products_list.remove(product)
                print(f"Product '{name}' removed from the store.")
                return
        print(f"Product '{name}' does not exist in the store.")

    # ram
    def print_products(self):
        print("Products in the store:")
        for product in self.products_list:
            print(f"Name: {product.name}, Code: {product.code}, Quantity: {product.quantity}, Price: {product.price}")


    # rom
    def save_product_to_file(self, product, filename):
        with open(filename, 'a') as file:
            file.write(f"Product Name: {product.name}\n")
            file.write(f"Product Code: {product.code}\n")
            file.write(f"Quantity: {product.quantity}\n")
            file.write(f"Price: {product.price}\n")
            file.write("------------\n")
        print(f"Product '{product.name}' saved to '{filename}' successfully.")

    # remoção rom
    def remove_product_from_file(self, filename, code):
        found = False  # Variável para indicar se o produto foi encontrado

        # Criar um arquivo temporário para armazenar as linhas atualizadas
        temp_filename = "temp_file.txt"

        # Abrir o arquivo original para leitura
        with open(filename, 'r') as file:
            # Abrir o arquivo temporário para escrita
            with open(temp_filename, 'w') as temp_file:
                # Ler linha por linha do arquivo original
                line = file.readline()
                while line:
                    if line.strip() == f"Product Code: {code}":
                        # Encontrou o registro a ser removido
                        found = True
                        # Ignorar as linhas do registro atual
                        for _ in range(5):
                            line = file.readline()
                        continue
                    
                    # Escrever a linha no arquivo temporário
                    temp_file.write(line)

                    # Ler a próxima linha do arquivo original
                    line = file.readline()

        if found:
            # Substituir o arquivo original pelo arquivo temporário
            os.replace(temp_filename, filename)
            print(f"Product '{code}' removed from '{filename}' successfully.")
        else:
            # Remover o arquivo temporário
            os.remove(temp_filename)
            print(f"Product '{code}' does not exist in '{filename}'.")

    # uso de ram
    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    #busca sequencial por uso de ram
    def sequential_search_ram(self, filename, code):
        comp = 0
        start_time = time.time()

        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("Product Code:"):
                    comp += 1
                    product_code = int(line.split(':')[1].strip())
                    if code == product_code:
                        elapsed_time = time.time() - start_time
                        print("Product found in", comp, "comparisons and", elapsed_time, "seconds:")
                        print(line)
                        return

        elapsed_time = time.time() - start_time
        print("Product not found in the store.")
        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")



    # busca rom
    def sequential_search_rom(self, filename, code):
        comp = 0
        start_time = time.time()
        found = False  # Variável para indicar se o produto foi encontrado
        record_lines = []  # Variável auxiliar para armazenar as linhas do registro atual

        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                record_lines.append(line)
                if line.startswith("Product Code:"):
                    comp += 1
                    product_code = int(line.split(':')[1].strip())
                    if code == product_code:
                        found = True
                        elapsed_time = time.time() - start_time
                        print("Product found in", comp, "comparisons and", elapsed_time, "seconds:")
                        # Imprimir o registro completo, incluindo as duas linhas adicionais
                        print(''.join(record_lines[:2]))  
                        break
                if line.startswith("------------"):
                    record_lines = []
                line = file.readline()

        if not found:
            elapsed_time = time.time() - start_time
            print("Product not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")



    def get_product_code(self, register):
        for line in register.split('\n'):
            if line.startswith("Product Code:"):
                product_code = int(line.split(":")[1].strip())
                return product_code
        return 0  # Return a default value in case no product code is found


    ##############################  
    def sort_products_by_code(self, filename):
        start_time = time.time()
        comparisons = 0
        with open(filename, 'r') as file:
            content = file.read()

        registers = content.split('------------\n')

        sorted_registers = sorted(registers, key=self.get_product_code)

        for i in range(1, len(sorted_registers)):
            if sorted_registers[i - 1] != sorted_registers[i]:
                comparisons += 1

        sorted_content = '------------\n'.join(sorted_registers)

        with open('sorted_output.txt', 'w') as file:
            file.write(sorted_content)
        elapsed_time = time.time() - start_time
        print("File successfully sorted with", comparisons, "comparisons in", elapsed_time, "s! Sorted file: sorted_output.txt")

    def shuffle_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read()

        registers = content.split('------------\n')

        random.shuffle(registers)

        shuffled_content = '------------\n'.join(registers)

        with open('shuffled_output.txt', 'w') as file:
            file.write(shuffled_content)
        print("Products shuffled successfully! Shuffled file: shuffled_output.txt")

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
            self.save_product_to_file(var_product, "products_test.txt")

    def sorted_partition_creation(self, filename, chunk_size):
        partitions = []
        with open(filename, 'r') as file:
            content = file.read()

        registers = content.split('------------\n')

        sorted_registers = sorted(registers, key=self.get_product_code)

        for i in range(0, len(sorted_registers), chunk_size):
            partition = sorted_registers[i:i+chunk_size]
            partitions.append(partition)

            partition_filename = f'./partitions/sorted-partition-{len(partitions)}.txt'
            with open(partition_filename, 'w') as partition_file:
                partition_file.write('\n'.join(partition))
        return partitions
    

    def sorted_partition_creation_ROM(self, filename, chunk_size):
        partitions = []
        partition_counter = 1

        with open(filename, 'r') as file:
            partition = []
            for line in file:
                if line.strip() == '------------':
                    sorted_partition = sorted(partition, key=self.get_product_code)
                    partitions.append(sorted_partition)

                    if len(partitions[-1]) >= chunk_size:
                        partition_filename = f'./partitions2/sorted-partition-{partition_counter}.txt'
                        with open(partition_filename, 'w') as partition_file:
                            partition_file.write('\n'.join(sorted_partition))
                        partition_counter += 1

                    partition = []
                else:
                    partition.append(line.strip())

        if partition:
            sorted_partition = sorted(partition, key=self.get_product_code)
            partitions.append(sorted_partition)

            partition_filename = f'./partitions2/sorted-partition-{partition_counter}.txt'
            with open(partition_filename, 'w') as partition_file:
                partition_file.write('\n'.join(sorted_partition))

        return partitions

    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Customer '{customer.name}' added to the store.")

    def place_order(self):
        customer_name = input("Enter the customer name: ")
        customer_exists = False
        for customer in self.customers:
            if customer.name == customer_name:
                customer_exists = True
                break

        if not customer_exists:
            customer_phone = input("Enter the customer phone: ")
            customer_address = input("Enter the customer address: ")
            customer = self.Customer(customer_name, customer_address, customer_phone)
            self.add_customer(customer)

        product_name = input("Enter the name of the product: ")
        quantity_requested = int(input("Enter the quantity required: "))

        for product in self.products_list:
            if product.name == product_name:
                if quantity_requested <= product.quantity:
                    product.quantity -= quantity_requested
                    order_total = product.price * quantity_requested
                    order_number = random.randint(1000, 9999)
                    order = self.Order(order_number, product, quantity_requested, order_total, customer)
                    self.orders.append(order)
                    print(f"Order placed successfully for '{product_name}'.")
                    return
                else:
                    print("Insufficient quantity in stock for the requested product.")
                    return

        print(f"Product '{product_name}' does not exist in the store.")

    def list_orders(self):
        print("Orders in the store:")
        for order in self.orders:
            print(f"Order Number: {order.order_number}")
            print(f"Product: {order.product.name}")
            print(f"Quantity: {order.quantity}")
            print(f"Total Value: {order.total_value}")
            print(f"Customer: {order.customer.name}")
            print("--------------")

    def calculate_total_value(self, order):
        total_value = order.product.price * order.quantity
        return total_value
