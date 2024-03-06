CLASS Product
    Attributes:
        name
        price
        description
        image
    
    Methods:
        FUNCTION Product(new_name, new_price, new_description, new_image)
            name = new_name
            price = new_price
            description = new_description
            image = new_image
        END Product

        FUNCTION calculate_gst()
            RETURN price / 11
        END calculate_gst

        FUNCTION is_customisable()
            RETURN isinstance(self, CustomisableProduct)
        END is_customisable

        FUNCTION __str__()
            RETURN name + " - $" + price + " - " + description
        END __str__

END Product

CLASS ProductOption
    Attributes:
        name
        dict
        multiple_allowed

    Methods:
        FUNCTION ProductOption(new_name, new_dict, new_multiple_allowed)
            name = new_name
            dict = new_dict
            multiple_allowed = new_multiple_allowed
        END ProductOption

        FUNCTION __str__()
            RETURN name + " - " + dict
        END __str__

END ProductOption

CLASS CustomisableProduct : Product
    Attributes:
        options

    Methods:
        FUNCTION set_option(option_name, option_value)
            FOR option_index = 0 TO options.length 
                option = options[option_index]
                IF option.name == option_name THEN
                    IF option.multiple_allowed THEN
                        option.dict[option_value][1] = True
                        price += option.dict[option_value][0]
                    ELSE
                        FOR index = 0 TO option.dict.length
                            key = option.dict[index]
                            option.dict[key][1] = False
                        END FOR
                        option.dict[option_value][1] = True
                        price += option.dict[option_value][0]
                    END IF
                    BREAK
                END IF
            END FOR
        END set_option

        FUNCTION __str__()
            string = "Actual Price: " + price + "\n"
            FOR option_index = 0 TO options.length
                option = options[option_index]
                string += option.name + ": " + option.dict + "\n"
            END FOR
        END __str__

END CustomisableProduct

CLASS User : UserMixin
    Attributes:
        cust_id
        first_name
        last_name
        address
        email
        password
        loyalty_member

    Methods:
        FUNCTION User(new_cust_id, new_first_name, new_last_name, new_address, new_email, new_password, new_loyalty_member)
            cust_id = new_cust_id
            first_name = new_first_name
            last_name = new_last_name
            address = new_address
            email = new_email
            password = new_password
            loyalty_member = new_loyalty_member
        END User

        FUNCTION parse_to_text()
            hashed_password = hash_password(password)
            RETURN first_name + "$%" + last_name + "$%" + cust_id + "$%" + address + "$%" + email + "$%" + hashed_password + "$%" + loyalty_member
        END parse_to_text

        FUNCTION check_password(password_to_check)
            IF password_to_check == password THEN
                RETURN True
            ELSE
                RETURN False
            END IF
        END check_password

        FUNCTION get_id():
            RETURN cust_id
        END get_id

        FUNCTION hash_password(password, to_hex)
            IF to_hex THEN
                RETURN password.encode("utf-8").hex()
            ELSE
                RETURN bytes.fromhex(password).decode("utf-8")
            END IF
        END hash_password

        FUNCTION check_if_user_exists(id, get_user)
            users = OPEN_READ("users.txt")
            lines = []
            WHILE NOT users.EOF
                line = users.READLINE()
                IF line.split("$%$")[2] == id THEN
                    IF get_user THEN
                        RETURN parse_from_text(line)
                    ELSE
                        RETURN True
                    END IF
                END IF
            END WHILE
            CLOSE(users)
            IF get_user THEN
                RETURN None
            ELSE
                RETURN False
            END IF
        END check_if_user_exists

        FUNCTION parse_from_text(string)
            first_name, last_name, cust_id, address, email, password, loyalty_member = string.split("$%$")
            parsed_password = hash_password(password, False)
            IF loyalty_member == "True" OR loyalty_member == "True\n":
                parsed_loyalty_member = True
            ELSE:
                parsed_loyalty_member = False
            END IF
            RETURN new User(first_name, last_name, cust_id, address, email, parsed_password, parsed_loyalty_member)
        END parse_from_text

END User

CLASS Order
    Attributes:
        customer
        products
        total
        delivery
        date
    
    Methods:
        FUNCTION Order(new_customer, new_products, new_total, new_delivery, new_date)
            customer = new_customer
            products = new_products
            total = new_total
            delivery = new_delivery
            date = new_date
        END Order

        FUNCTION parse_to_text()
            string = "==========\n"
            string += customer.cust_id + "$%" + total + "$%" + delivery + "$%" + date.strftime('%Y-%m-%d') + "\n"
            FOR index = 0 TO products.length
                product = products[index]
                string += product.name + "$%" + str(product.price) + "$%" + product.description + "$%" + product.image + "\n"
            END FOR
            RETURN string
        END parse_to_text

        FUNCTION parse_from_text(string)
            lines = string.split("\n")
            customer_id, total, delivery, date = lines[0].split("$%$")
            IF delivery == "True" THEN
                parsed_delivery = True
            ELSE
                parsed_delivery = False
            END IF
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            products = []
            FOR line in lines[1:]
                IF line THEN
                    name, price, description, image = line.split("$%$")
                    products.append(new Product(name, float(price), description, image))
                END IF
            END FOR
            RETURN new Order(check_if_user_exists(customer_id, True), products, parsed_delivery, parsed_date, float(total))
        END parse_from_text
END Order

    