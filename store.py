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
        def create_customer():
            name = input("Enter customer name: ")
            cep = input("Enter customer cep: ")
            phone = input("Enter customer phone: ")
            cpf = input("Enter customer CPF: ")
            return Store.Customer(name, cep, phone, cpf)

    class Order:
        def __init__(self, order_number, product, quantity, total_value, customer):
            self.order_number = order_number
            self.product = product
            self.quantity = quantity
            self.total_value = total_value
            self.customer = customer

    def __init__(self):
        self.products_list = []
        self.customers = []
        self.orders = []

    def add_product(self, product):
        if any(prod.name == product.name for prod in self.products_list):
            print(f"Product '{product.name}' already exists in the store.")
        else:
            self.products_list.append(product)
            print(f"Product '{product.name}' added to the store.")

    def remove_product(self, name):
        for product in self.products_list:
            if product.name == name:
                self.products_list.remove(product)
                print(f"Product '{name}' removed from the store.")
                return
        print(f"Product '{name}' does not exist in the store.")

    def print_products(self):
        print("Products in the store:")
        for product in self.products_list:
            print(f"Name: {product.name}, Code: {product.code}, Quantity: {product.quantity}, Price: {product.price}")

    def read_file(self, filename):
        try:
            chunk_size = 30  # Define o tamanho do chunk desejado
            reader = pd.read_csv(filename, chunksize=chunk_size)
            for chunk in reader:
                # Realiza as operações desejadas com cada chunk
                print(chunk)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def get_product_code(self, register):
        for line in register.split('\n'):
            if line.startswith("Product Code:"):
                product_code = int(line.split(":")[1].strip())
                return product_code
        return 0

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

    def remove_product_from_file(self, filename, code):
        df = pd.read_csv(filename)
        df = df[df['Product Code'] != code]
        df.to_csv(filename, index=False)
        print(f"Product '{code}' removed from '{filename}' successfully.")

    def sequential_search_rom(self, filename, code):
        comp = 0
        start_time = time.time()
        found = False

        for chunk in pd.read_csv(filename, chunksize=15):
            comp += chunk.shape[0]
            result = chunk[chunk['Product Code'] == code]
            if not result.empty:
                found = True
                elapsed_time = time.time() - start_time
                print("Product found in", comp, "comparisons and", elapsed_time, "seconds:")
                print(result)
                break

        if not found:
            elapsed_time = time.time() - start_time
            print("Product not found in the store.")

        print("Total comparisons:", comp)
        print("Elapsed time:", elapsed_time, "seconds")

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

    def menu_customer(self, filename_costumer):
        while True:
            print("\n=== CUSTOMER MENU ===")
            print("1. Add Customer")
            print("2. Remove Customer")
            print("3. List Customer's")
            print("4. Gen Random Custumers")
            # print("3. Place Order (NOT WORKING)")
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

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")

    def main_menu(self):
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Product Menu")
            print("2. Customer Menu")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.menu_product("products.csv")

            elif choice == "2":
                self.menu_customer("costumer.csv")

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")


###################################

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


    def read_file_costumer(self, filename_costumer):
        try:
            chunk_size = 30  # Define o tamanho do chunk desejado
            reader = pd.read_csv(filename_costumer, chunksize=chunk_size)
            for chunk in reader:
                # Realiza as operações desejadas com cada chunk
                print(chunk)
        except FileNotFoundError:
            print(f"File '{filename_costumer}' not found.")

    def remove_costumer_from_file(self, filename_costumer, cpf):
        df = pd.read_csv(filename_costumer)
        df = df[df['Costumer CPF'] != cpf]
        df.to_csv(filename_costumer, index=False)
        print(f"Costumer '{cpf}' removed from '{filename_costumer}' successfully.")

    def place_order(self, customer_cpf):
        customer = self.find_customer_by_cpf(customer_cpf)
        if customer:
            order = self.Order(customer)
            while True:
                customer_cpf = int(input("Enter costumer code to add to order (or 0 to finish): "))
                if customer_cpf == 0:
                    break
                costumer = self.find_costumer_by_cpf(customer_cpf)
                if costumer:
                    quantity = int(input("Enter costumer quantity: "))
                    order.add_product(costumer, quantity)
                    print("Product added to order successfully.")
                else:
                    print("Product not found.")
            self.orders.append(order)
            print("Order placed successfully.")
        else:
            print("Customer not found.")

    def teste():
        pass

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

    
