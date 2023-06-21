import time
import random

class Store:
    class Product:
        def __init__(self, code, name, price, quantity):
            self.code = code
            self.name = name
            self.price = price
            self.quantity = quantity

    def __init__(self):
        self.products_list = []
        self.balance = 0
        self.orders = []

    # adiciona produto na lista de produtos da loja
    def add_product(self, product):
        if any(prod.name == product.name for prod in self.products_list):
            print(f"Product '{product.name}' already exists in the store.")
            return
        else:
            self.products_list.append(product)

    # remove produto pelo nome da lista de produtos da loja
    def remove_product(self, name):
        for product in self.products_list:
            if product.name == name:
                self.products_list.remove(product)
                return
        print(f"Product '{name}' does not exist in the store.")

    # imprime todos produtos da loja
    def print_products(self):
        print("Products in the store:")
        for product in self.products_list:
            print(f"Name: {product.name}, Code: {product.code}, Quantity: {product.quantity}, Price: {product.price}")

    # salva produto no arquivo filename
    def save_product_to_file(self, product, filename):
        with open(filename, 'a') as file:
            file.write(f"Product Name: {product.name}\n")
            file.write(f"Product Code: {product.code}\n")
            file.write(f"Quantity: {product.quantity}\n")
            file.write(f"Price: {product.price}\n")
            file.write("------------\n")
        print(f"Product '{product.name}' saved to '{filename}' successfully.")

    # remove um produto do arquivo baseado no código
    def remove_product_from_file(filename, code):
        with open(filename, 'r') as file:
            lines = file.readlines()

        found = False
        with open(filename, 'w') as file:
            for line in lines:
                if line.strip() == f"Product Code: {code}":
                    found = True
                    continue
                if found:
                    if line.strip() == "------------":
                        found = False
                else:
                    file.write(line)

        if found:
            print(f"Product '{code}' removed from '{filename}' successfully.")
        else:
            print(f"Product '{code}' does not exist in '{filename}'.")

   # le produtos do arquivo filename 
    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    # realiza busca sequencial baseada em codigo de produto no arquivo
    def sequential_search(self, filename, code):
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

    # auxiliar para função sort_products_by_code
    def get_product_code(self, register):
        for line in register.split('\n'):
            if line.startswith("Product Code:"):
                product_code = int(line.split(":")[1].strip())
                return product_code
        return 0  # Return a default value in case no product code is found

    
    # ordena os produtos por codigo

    def sort_products_by_code(self, filename):
        # Read the contents of the file
        start_time = time.time()
        comparisons = 0
        with open(filename, 'r') as file:
            content = file.read()

        # Split the content into individual registers
        registers = content.split('------------\n')

        # Sort the registers based on the product code
        sorted_registers = sorted(registers, key=self.get_product_code)

        # Count the number of comparisons made during sorting
        for i in range(1, len(sorted_registers)):
            if sorted_registers[i - 1] != sorted_registers[i]:
                comparisons += 1

        # Join the sorted registers back into a single string
        sorted_content = '------------\n'.join(sorted_registers)

        # Write the sorted content back to the file
        with open('sorted_output.txt', 'w') as file:
            file.write(sorted_content)
        elapsed_time = time.time() - start_time
        print("File successfully sorted with", comparisons, "comparisons in", elapsed_time, "s! Sorted file: sorted_output.txt")



    # embaralha registros do arquivo
    def shuffle_file(self, filename):
        # Read the contents of the file
        with open(filename, 'r') as file:
            content = file.read()

        # Split the content into individual registers
        registers = content.split('------------\n')

        # Shuffle the registers
        random.shuffle(registers)

        # Join the shuffled registers back into a single string
        shuffled_content = '------------\n'.join(registers)

        # Write the shuffled content back to the file
        with open('shuffled_output.txt', 'w') as file:
            file.write(shuffled_content)
        print("Products shuffled successfully! Shuffled file: shuffled_output.txt")

    # gera instrumentos aleatorios baseado em lista de nomes e numeros aleatorios
    def gen_random_instruments(self):
        code = 0
        with open('names.txt', 'r') as file:
            content = file.readlines()
        random.shuffle(content)
        for line in content:
            cleaned_line = line.rstrip()  # Remove the newline character
            random_float = round(random.uniform(20, 1000), 2)
            random_integer = random.randint(0, 20)
            var_product = self.Product(code, cleaned_line, random_float, random_integer)
            self.add_product(var_product)
            code += 1
            self.save_product_to_file(var_product, "products_test.txt")

    # cria partições ordenadas do arquivo maior em disco
    def sorted_partition_creation(self, filename, chunk_size):
        partitions = []
        with open(filename, 'r') as file:
            content = file.read()

        # Split the content into individual registers
        registers = content.split('------------\n')

        # Sort the registers based on the product code
        sorted_registers = sorted(registers, key=self.get_product_code)

        # Create partitions with sorted registers
        for i in range(0, len(sorted_registers), chunk_size):
            partition = sorted_registers[i:i+chunk_size]
            partitions.append(partition)

            # Save the partition to a separate file
            partition_filename = f'./partitions/sorted-partition-{len(partitions)}.txt'
            with open(partition_filename, 'w') as partition_file:
                partition_file.write('\n'.join(partition))
        return partitions
    

    ####################################################
    class Costumer:
        def __init__(self, name, adresss, phone) -> None:
            self.name = name
            self.adress = adresss
            self.phone = phone

        def get_custumer_info(self):
            self.name = str(input("Enter the client name: "))
            self.phone = str(input("Enter the client phone: "))
            self.adress = str(input("Enter the client adress: "))
            return self


            
            
    #######################################################
    # criação de classe e funções para ser possivel realizar pedidos em cima dos produtos
    class Order:
        def __init__(self, order_number, products, total_value, customer):
            self.order_number = order_number
            self.products = products
            product_quantity = 0
            self.total_value = total_value
            self.customer = customer

    # fazer requisição de produto na loja
    def place_order(self, custumer):
        product_name = input("Enter the name of the product: ")
        quantity_requested = int(input("Enter the quantity required: "))
        try:
            
            pass
        except:
            pass
        for product in self.products_list:
            if product.name == product_name:
                if quantity_requested <= product.quantity:
                    # Update the product quantity in the store
                    product.quantity -= quantity_requested

                    # Calculate the order total
                    order_total = product.price * quantity_requested

                    
                    
                    # Add the order to the list of orders
                    self.orders.append((product.name, quantity_requested, order_total, custumer))

                    print(f"Order placed successfully for '{product_name}'.")
                    return
                else:
                    print("Insufficient quantity in stock for the requested product.")
                    return

        print(f"Product '{product_name}' does not exist in the store.")

    def save_order_in_file(self, order, filename):
        with open(filename, 'w') as file:
            file.write(order)


    
    # class Store:
    #     def __init__(self, orders, order_quantity):
    #         self.orders = orders
    #         self.order_quantity = order_quantity

    
   
        
    
    def add_customer(self, store, customer):
        pass 
        # Logic to add a customer to the store
    
    def place_order(self, store, order):
        pass
        # Logic to place an order in the store
    
    def list_orders(self, store):
        pass
        # Logic to list the orders in the store
    
    def calculate_total_value(self, order):
        pass
        # Logic to calculate the total value of an order
