from flask import Flask, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from classes import Product, CustomisableProduct, ProductOption, User
import copy

app = Flask(__name__)
app.secret_key = "SIR"
login_manager = LoginManager()
login_manager.init_app(app)

products = {
    "Classics Range": [
        Product("Pepperoni Pizza", 21, "Our signature base topped with fresh Italian tomato sauce, spicy cured pork salami and mozzarella cheese.", "https://www.dominos.com.au/ManagedAssets/AU/product/P480/AU_P480_en_hero_12569.jpg?v370349117"),
        Product("Chicken Supreme Pizza", 23.50, "Our signature base topped with fresh Italian tomato sauce, 100% Aussie chicken breast, sliced red onion, capsicum, mushrooms, pineapple, mozzarella and oregano.", "https://www.dominos.com.au/ManagedAssets/AU/product/P422/AU_P422_en_hero_8129.jpg?v807560171"),
        Product("BBQ Meatlovers Pizza", 25.50, "Our signature base topped with Hickory BBQ sauce, 100% Aussie beef, pepperoni, rasher bacon, Italian sausage, sliced red onion, mozzarella and oregano.", "https://www.dominos.com.au/ManagedAssets/AU/product/P019/AU_P019_en_hero_4055.jpg?v1694200044"),
        Product("Veg Supreme Pizza", 22.5, "Our signature base topped with fresh Italian tomato sauce, sliced red onion, capsicum, mushrooms, pineapple, baby spinach, kalamata olives, mozzarella and oregano.", "https://www.dominos.com.au/ManagedAssets/AU/product/P456/AU_P456_en_hero_10451.png?v1150158411"),
        Product("Hawaiian Pizza", 19, "Our signature base topped with fresh Italian tomato sauce, 100% Aussie ham, sweet juicy pineapple and mozzarella cheese.", "https://www.dominos.com.au/ManagedAssets/AU/product/P005/AU_P005_en_hero_4055.jpg?v692091788"),
        Product("Margherita Pizza", 18.5, "Our signature base topped with fresh Italian tomato sauce, mozzarella cheese and oregano.", "https://www.dominos.com.au/ManagedAssets/AU/product/P301/AU_P301_en_hero_4055.jpg?v-1013096145"),
        Product("Spicy Special", 20, "Our signature base topped with fresh Italian tomato sauce, 100% Aussie beef, pepperoni, sliced red onion, jalapeños, chilli flakes, mozzarella and oregano.", "https://www.dominos.com.au/ManagedAssets/AU/product/P502/AU_P502_en_hero_12276.jpg?v1552340311"),
        CustomisableProduct("Build Your Own Pizza", 15, "Papa's signature base, topped with sauces and toppings of your choice!", "static/BYOP.png", [
            ProductOption("Sauce", {
                "Tomato": [0.5, False],
                "BBQ": [0.5, False], 
                "Pesto": [1.5, False],
            }),
            ProductOption("Cheese", {
                "Mozzarella": [0.5, False],
                "Cheddar": [0.5, False],
                "Parmesan": [1.5, False],
            }),
            ProductOption("Meat", {
                "Pepperoni": [1, False],
                "Ham": [1, False],
                "Beef": [1.5, False],
                "Chicken": [1.5, False],
                "Bacon": [1.5, False],
                "Sausage": [1.5, False],
                "Salami": [1.5, False],
                "Pork": [1.5, False],
            }),
            ProductOption("Vegetables", {
                "Pineapple": [0.5, False],
                "Mushroom": [0.5, False],
                "Onion": [0.5, False],
                "Capsicum": [0.5, False],
                "Olives": [0.5, False],
                "Jalapenos": [0.5, False],
                "Spinach": [0.5, False],
                "Tomato": [0.5, False],
                "Chilli": [0.5, False],
                "Garlic": [0.5, False],
                "Mystery": [1.5, False],
            })
        ])
    ],
    "Sides": [
        Product("Garlic Bread", 8, "Oven baked bread, topped with garlic and herb butter.", "https://order.dominos.com.au/ManagedAssets/AU/product/S00001/AU_S00001_en_hero_3970.jpg?v914720366"),
        Product("Cheesy Garlic Bread", 10, "Oven baked bread, topped with garlic and herb butter, infused with aromatic mozzarella cheese.", "https://www.dominos.com.au/ManagedAssets/AU/product/S00335/AU_S00335_en_hero_3970.jpg?v1445520942"),
        Product("Straight-Cut Chips", 10, "Oven baked chips, seasoned with salt and pepper.", "https://www.dominos.com.au/ManagedAssets/AU/product/S00016/AU_S00016_en_hero_12301.jpg?v1581437728"),
        Product("Spicy Loaded Chips", 14, "Oven baked chips, topped with spicy beef, pepperoni, sliced red onion, jalapeños, chilli flakes, and Papa's signature cheese sauce.", "https://www.dominos.com.au/ManagedAssets/AU/product/S00568/AU_S00568_en_hero_12569.jpg?v2043401138"),
    ],
    "Drinks": [
        CustomisableProduct("Pepsi", 2, "1.25L/600mL. Coca-Cola is the most popular soft drink in history, as well as the best-known brand in the world.", "https://www.dominos.com.au/ManagedAssets/AU/variety/Variety.Pepsi/AU_Variety.Pepsi_en_menu_12324.jpg?v-1367151555", [
            ProductOption("Size", {
                "1.25L": [1, False],
                "600mL": [0, False]
            }, False)
        ]),
        CustomisableProduct("Solo", 2, "1.25L/600mL. Solo is the world's leading lemon-lime flavoured soft drink.", "https://www.dominos.com.au/ManagedAssets/AU/variety/Variety.Solo/AU_Variety.Solo_en_menu_12324.jpg?v229998257", [
            ProductOption("Size", {
                "1.25L": [1, False],
                "600mL": [0, False]
            }, False)
        ]),
        CustomisableProduct("Sunkist", 2.5, "1.25L/600mL. Sunkist is a bubbly, fruit-flavoured soft drink that has a great, fruity taste.", "https://www.dominos.com.au/ManagedAssets/AU/variety/Variety.Sunkist/AU_Variety.Sunkist_en_menu_12324.jpg?v545627267", [
            ProductOption("Size", {
                "1.25L": [1, False],
                "600mL": [0, False]
            }, False)
        ]),
        CustomisableProduct("Mountain Dew", 2.5, "1.25L/600mL. For the gamers.", "https://www.dominos.com.au/ManagedAssets/AU/variety/Variety.MountainDew/AU_Variety.MountainDew_en_menu_12324.jpg?v2083099670", [
            ProductOption("Size", {
                "1.25L": [1, False],
                "600mL": [0, False]
            }, False)
        ]),
        CustomisableProduct("Build Your Own Milkshake", 8, "Choose from a variety of flavours and toppings to create your own milkshake!", "https://www.dominos.com.au/ManagedAssets/AU/variety/Variety.Milkshake/AU_Variety.Milkshake_en_menu_12324.jpg?v-1367151555", [
            ProductOption("Flavour", {
                "Chocolate": [1.5, False],
                "Strawberry": [1.5, False],
                "Vanilla": [1.5, False],
                "Mint": [2, False],
            }),
            ProductOption("Topping", {
                "Chocolate Syrup": [0.5, False],
                "Strawberry Syrup": [0.5, False],
                "Caramel Syrup": [0.5, False],
                "Mystery": [1.5, False],
            })
        ])
    ],
}

cart = []

@login_manager.user_loader
def load_user(user_id: str):
    with open('users.txt', 'r') as f:
        for line in f:
            user = User.parse_from_text(line.strip())
            if user.cust_id == user_id:
                return user
    return None

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        #print (request.form)
        product_name = request.form['name']
        #loop through products, find the product with the same name and deep copy it
        new_product = None
        for category in products:
            for product in products[category]:
                if product.name == product_name:
                    new_product = copy.deepcopy(product)
                    break
        if new_product is None:
            raise ValueError("Invalid product name")
        # loop through options if it is a customisable product, and set the options
        if new_product.is_customisable():
            options_chosen = dict((key, request.form.getlist(key)) for key in request.form.keys())
            for option_name in options_chosen:
                for option_value in options_chosen[option_name]:
                    new_product.set_option(option_name, option_value)

        # add the product to the cart
        cart.append(new_product)
        print(cart)
    return render_template('menu.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    error = ""
    if request.method == 'POST' and 'adminpassword' in request.form: #a POST request from the form
        if request.form['adminpassword'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('admin.html')
        return render_template('login.html', error=error)
    elif request.method == 'POST' and 'login' in request.form:
        id = request.form['custid']
        password = request.form['password']
        user = load_user(id)
        if user is None:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        print(user.parse_to_text())
        login_user(user)
        if user is not None and user.check_password(password):
            return render_template('login.html', error=error)
        
    elif request.method == 'POST' and 'signup' in request.form:
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        cust_id = int(request.form['custid'])
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        loyalty = False
        if 'loyaltymember' in request.form:
            loyalty = True if request.form["loyaltymember"] == "on" else False

        if User.check_if_user_exists(cust_id):
            error = "ID is taken. Please try again."
            return render_template('login.html', error=error)
        
        user = User(first_name, last_name, cust_id, address, email, password, loyalty)
        with open('users.txt', 'a') as f:
            f.write(user.parse_to_text())
        return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    delivery = False
    if request.method == 'POST':
        if 'delivery' in request.form:
            delivery = True
    subtotal = sum([product.price for product in cart]) #product.price IMPLEMENTS POLYMORPHISM!!!
    total = subtotal
    over_one_hundred = False
    loyalty = False
    discount_amount = 0
    if delivery:
        total += 8
    if subtotal > 100:
        over_one_hundred = True
        discount_amount = 0.05 * total
        total -= discount_amount
    elif current_user.loyalty_member:
        loyalty = True
        discount_amount = 0.05 * total
        total -= discount_amount
    gst = total / 11
    return render_template('cart.html', items=cart, subtotal=subtotal, gst=gst, total=total, delivery=delivery, loyalty=loyalty, discount=discount_amount, over_one_hundred=over_one_hundred)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')