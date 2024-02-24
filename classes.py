import datetime
from flask_login import UserMixin

class Product:
    def __init__(self, name: str, price: float, description: str, image_url: str):
        self.name = name
        self.price = price
        self.description = description
        self.image = image_url

    def calculate_gst(self):
        return self.price / 11

    def is_customisable(self):
        return isinstance(self, CustomisableProduct)
    
    def __str__(self):
        return f"{self.name} - ${self.price} - {self.description}"
    

class ProductOption:
    def __init__(self, name: str, option_price_dict: dict, multiple_allowed: bool = True):
        self.name = name
        self.dict = option_price_dict #this price dict is including GST
        self.multiple_allowed = multiple_allowed

    def __str__(self):
        return f"{self.name} - {self.dict}"

class CustomisableProduct(Product):
    def __init__(self, name: str, base_price: float, description: str, image_url: str, options: list):
        super().__init__(name, base_price, description, image_url)
        self.options = options

    def set_option(self, option_name: str, option_value: str):
        for option in self.options:
            if option.name == option_name:
                if option.multiple_allowed:
                    option.dict[option_value][1] = True
                    self.price += option.dict[option_value][0]
                else:
                    for value in option.dict:
                        option.dict[value][1] = False
                    option.dict[option_value][1] = True
                    self.price += option.dict[option_value][0]
                break

    def __str__(self):
        string = "Actual Price: " + str(self.price) + "\n"
        for option in self.options:
            string += f"{option.name}: {option.dict}\n"
        return f"{super().__str__()}\n{string}"
    
class User(UserMixin):
    def __init__(self, first_name: str, last_name: str, cust_id, address: str, email: str, password: str, loyalty_member: bool = False):
        self.cust_id = cust_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.password = password
        self.loyalty_member = loyalty_member

    def parse_to_text(self):
        return f"{self.first_name}$%${self.last_name}$%${self.cust_id}$%${self.address}$%${self.email}$%${self.password}$%${self.loyalty_member}\n"
    
    def check_password(self, password: str):
        return self.password == password
    
    def get_id(self):
        return self.cust_id
    
    @staticmethod
    def check_if_user_exists(id: str, get_user: bool = False):
        with open("users.txt", "r") as file:
            for line in file:
                if line.split("$%$")[2] == id:
                    return User.parse_from_text(line) if get_user else True
        return None if get_user else False
    
    @staticmethod
    def parse_from_text(string: str):
        first_name, last_name, cust_id, address, email, password, loyalty_member = string.split("$%$")
        parsed_loyalty_member = True if loyalty_member == "True\n" else False
        return User(first_name, last_name, cust_id, address, email, password, parsed_loyalty_member)
    
    
class Order:
    def __init__(self, customer: User, products: list, delivery: bool, date: datetime.date, total: float = 0.0):
        self.customer = customer
        self.products = products
        self.total = total
        self.delivery = delivery
        self.date = date

    def parse_to_text(self):
        string = "==========\n"
        string += f"{self.customer.cust_id}$%${self.total}$%${self.delivery}$%${self.date.strftime('%Y-%m-%d')}\n"
        for product in self.products:
            string += f"{product.name}$%${product.price}$%${product.description}$%${product.image}\n"
        return string

    def __str__(self):
        string = f"Customer: {self.customer.cust_id} - {self.customer.email}\n"
        for product in self.products:
            string += f"{product}\n"
        return string
    
    @staticmethod
    def parse_from_text(string: str):
        #string will be in the format of:
        #customer_id$%$total$%$delivery\n
        #product_name$%$product_price$%$product_description$%$product_image\n
        #product_name$%$product_price$%$product_description$%$product_image\n
        #etc.
        lines = string.split("\n")
        customer_id, total, delivery, date = lines[0].split("$%$")
        parsed_delivery = True if delivery == "True" else False
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        products = []
        for line in lines[1:]:
            if line:
                name, price, description, image = line.split("$%$")
                products.append(Product(name, float(price), description, image))
        return Order(User.check_if_user_exists(customer_id, True), products, parsed_delivery, parsed_date, float(total))
    
    
