import os
import sqlite3
import traceback
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4


def logger(statement):
    print(f"""
--------------------------------------------------------
Executing:
 {statement}
--------------------------------------------------------
""")

class DataBase:
    order_id_counter = 1010

    def __init__(self, path_to_db='back/db.sqlite3'):
        self.path_to_db = os.path.abspath(path_to_db)
        print(f"Database path: {self.path_to_db}")

    @property
    def connection(self):
        try:
            return sqlite3.connect(self.path_to_db)
        except sqlite3.Error as e:
            print("SQLite connection error:", e)
            raise

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def get_user_by_chat_id(self, chat_id: int):
        """
        Retrieve user data from bot_app_user based on the provided chat_id.

        :param chat_id: The chat_id of the user.
        :return: User data as a tuple or None if not found.
        """
        sql = "SELECT * FROM bot_app_user WHERE chat_id = ?"
        user_data = self.execute(sql, (chat_id,), fetchone=True)
        return user_data

    def get_order_by_order_id(self, order_id):
        # Replace this with the actual query for retrieving order details from your database
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bot_app_order WHERE order_id=?", (order_id,))
        order = cursor.fetchone()
        return order

    def get_user_language_id(self, chat_id: int):
        """
        Retrieve the language ID of the user based on the provided chat_id.

        :param chat_id: The chat_id of the user.
        :return: Language ID as an integer or None if the user is not found.
        """
        sql = "SELECT lang_id FROM bot_app_user WHERE chat_id = ?"
        lang_id = self.execute(sql, (chat_id,), fetchone=True)
        return lang_id[0] if lang_id else None

    def get_all_users(self):
        """
        Retrieve all users from the bot_app_user table.

        :return: List of user data tuples.
        """
        sql = "SELECT * FROM bot_app_user"
        users_data = self.execute(sql, fetchall=True)
        return users_data
    def add_comment(self, user_id: int, comment_text: str, username: str):
        """
        Add a new comment to the bot_app_comment table.

        :param user_id: The user_id associated with the comment.
        :param comment_text: The text of the comment.
        :param username: The username associated with the comment.
        """
        sql = """
            INSERT INTO bot_app_comment(user_id, comment_text, username)
            VALUES (?, ?, ?)
        """
        self.execute(sql, (user_id, comment_text, username), commit=True)

    def get_order_product_details(self, date=None):
        try:
            # Если дата не предоставлена, используйте текущую дату
            if date is None:
                date = datetime.now().strftime('%Y-%m-%d')

            query = """
                WITH OrderIds AS (
                    SELECT DISTINCT order_id
                    FROM bot_app_order
                    WHERE strftime('%Y-%m-%d', created_at) = ?
                )

                SELECT 
                    op.amount,
                    op.created_at,
                    u.first_name,
                    u.phone_number,
                    u.shop_name,
                    p.name_uz AS product_name_uz
                FROM 
                    bot_app_orderproduct op
                JOIN 
                    OrderIds o ON op.id = o.order_id
                JOIN 
                    bot_app_user u ON u.chat_id = op.user_id
                JOIN 
                    bot_app_product p ON p.id = op.product_id;
            """

            parameters = (date,)  # Используйте кортеж для параметра

            # Выполните запрос
            result = self.execute(query, parameters)

            # Проверка на None перед итерацией по результату
            if result is None:
                print("Error: Result is None.")
                return []

            # Вывести результат запроса для отладки
            print("Query result:")
            for row in result:
                print(row)

            # Если результат пуст, вернуть пустой список
            if not result:
                print("No data found.")
                return []

            return result
        except Exception as e:
            # Запись ошибки с трассировкой стека для детальной информации
            print(f"Error executing query: {e}")
            traceback.print_exc()
            return None

    def get_root_categories(self):
        """
        Retrieve root categories from the bot_app_category table where parent_id is NULL.

        :return: List of root category data tuples.
        """
        sql = "SELECT * FROM bot_app_category WHERE parent_id IS NULL"
        root_categories_data = self.execute(sql, fetchall=True)
        return root_categories_data

    def get_shop_name(self):
        """
        Retrieve root categories from the bot_app_shop_name table where parent_id is NULL.

        :return: List of root category data tuples.
        """
        sql = "SELECT * FROM bot_app_shop_name WHERE parent_id IS NULL"
        get_shop_name = self.execute(sql, fetchall=True)
        return get_shop_name


    def get_categories_by_parent_id(self, parent_id):
        """
        Retrieve categories from the bot_app_category table based on the provided parent_id.

        :param parent_id: The parent_id to filter categories.
        :return: List of category data tuples.
        """
        # SQL query to select categories based on parent_id
        sql = "SELECT * FROM bot_app_category WHERE parent_id = ?"

        # Execute the query with the provided parent_id and fetch all the results
        categories_data = self.execute(sql, (parent_id,), fetchall=True)

        # Return the list of category data tuples
        return categories_data

    def get_parent_id_by_category_id(self, category_id: int):
        """
        Retrieve parent_id from bot_app_category based on the provided category_id.

        :param category_id: The id of the category.
        :return: The parent_id or None if not found.
        """
        sql = "SELECT parent_id FROM bot_app_category WHERE id = ?"
        result = self.execute(sql, (category_id,), fetchone=True)
        return result[0] if result else None

    def get_all_about_data(self):
        """
        Retrieve all data from the bot_app_about table.

        :return: List of dictionaries where keys are column names and values are corresponding data.
        """
        try:
            # Get column names using PRAGMA table_info
            pragma_sql = "PRAGMA table_info(bot_app_about)"
            pragma_result = self.execute(pragma_sql, fetchall=True)

            # Extract column names
            column_names = [column[1] for column in pragma_result]

            # Retrieve all data from the table
            sql = "SELECT * FROM bot_app_about"
            about_data = self.execute(sql, fetchall=True)

            # Convert data to a list of dictionaries
            result_list = [dict(zip(column_names, row)) for row in about_data]

            return result_list
        except Exception as e:
            # Handle exceptions (e.g., log the error)
            print(f"Error in get_all_about_data: {e}")

        return []

    def get_max_order_id(self):
        """
        Retrieve the largest order_id from the bot_app_order table.

        :return: The largest order_id as an integer.
        """
        sql = "SELECT MAX(order_id) FROM bot_app_order"
        result = self.execute(sql, fetchone=True)
        max_order_id = result[0] if result[0] is not None else 0
        return max_order_id

    def add_order(self, user_id: int, status: str, amount: str, created_at: str, order_id: str):
        """
        Add a new order to the bot_app_order table.

        :param user_id: The user_id associated with the order.
        :param status: The status of the order.
        :param payment_type: The payment type of the order.
        :param longitude: The longitude associated with the order.
        :param latitude: The latitude associated with the order.
        :param created_at: The creation timestamp of the order.
        """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO bot_app_order(user_id, status, amount,  created_at, order_id)
            VALUES (?, ?, ?,  ?, ?)
        """
        self.execute(sql, (user_id, status, amount,  created_at ,order_id), commit=True)

    def add_order_product(self, user_id: int, product_id: int, amount: int):
        """
        Add a new order product to the bot_app_orderproduct table.

        :param user_id: The user_id associated with the order product.
        :param product_id: The product_id associated with the order product.
        :param amount: The amount of the product in the order.
        """
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO bot_app_orderproduct(user_id, product_id, amount, created_at)
            VALUES (?, ?, ?,  ?)
        """
        with self.connection:  # Ensure that the connection is properly closed
            self.execute(sql, (user_id, product_id,  amount, created_at), commit=True)
    def get_product_by_id(self, product_id: int):
        """
        Retrieve product from the bot_app_product table based on the provided product_id.

        :param product_id: The id of the product.
        :return: Product data tuple or None if not found.
        """
        sql = "SELECT * FROM bot_app_product WHERE id = ?"
        product_data = self.execute(sql, (product_id,), fetchone=True)
        return product_data

    def get_all_order_products(self, user_id: int):
        """
        Retrieve all order products for a specific user from the bot_app_orderproduct table.
        Include both column names and values in the result.

        :param user_id: The user_id to filter order products.
        :return: List of dictionaries, each containing column names and values, or an empty list if not found.
        """
        try:
            sql = """
                SELECT bot_app_orderproduct.id,
                       bot_app_orderproduct.amount,
                       bot_app_orderproduct.created_at,
                       bot_app_orderproduct.user_id,
                       bot_app_orderproduct.product_id,
                       bot_app_product.name_uz as product_name_uz,
                       bot_app_product.name_ru as product_name_ru,
                       bot_app_product.name_en as product_name_en,
                       bot_app_product.price as product_price
                FROM bot_app_orderproduct
                INNER JOIN bot_app_product ON bot_app_orderproduct.product_id = bot_app_product.id
                WHERE bot_app_orderproduct.user_id = ?
            """
            order_products_data = self.execute(sql, (user_id,), fetchall=True)

            if order_products_data:
                # Explicitly list the column names
                column_names = [
                    'id', 'amount', 'created_at', 'user_id', 'product_id',
                    'product_name_uz', 'product_name_ru', 'product_name_en', 'product_price'
                ]

                # Combine column names with values for each row
                result_list = [dict(zip(column_names, row)) for row in order_products_data]
                return result_list
        except Exception as e:
            # Handle exceptions (e.g., log the error)
            print(f"Error in get_all_order_products: {e}")

        return []

    # def get_product_by_user_id(self, user_id: int):
    #     """
    #     Retrieve product from the bot_app_product table based on the provided product_id.
    #
    #     :param product_id: The id of the product.
    #     :return: Product data tuple or None if not found.
    #     """
    #     sql = "SELECT * FROM bot_app_product WHERE user_id = ?"
    #     product_data = self.execute(sql, (user_id,), fetchone=True)
    #     return product_data

    def get_order_products_by_id(self, id: int):
        """
        Retrieve order products with product details based on the provided order_id.
        Include both column names and values in the result.

        :param order_id: The order_id to filter order products.
        :return: List of dictionaries, each containing column names and values, or an empty list if not found.
        """
        try:
            sql = """
                SELECT 
                    bot_app_orderproduct.*, 
                    bot_app_product.name_uz as product_name_uz,
                    bot_app_product.name_ru as product_name_ru,
                    bot_app_product.name_en as product_name_en,
                    bot_app_product.price as product_price
                FROM 
                    bot_app_orderproduct
                INNER JOIN 
                    bot_app_product ON bot_app_orderproduct.product_id = bot_app_product.id
                WHERE 
                    bot_app_orderproduct.id = ?
            """
            order_products_data = self.execute(sql, (id,), fetchall=True)

            if order_products_data:
                # Explicitly list the column names
                column_names = [
                    'id', 'amount', 'created_at', 'product_id', 'user_id',
                    'name_uz', 'name_ru', 'name_en', 'product_price'
                ]

                # Combine column names with values for each row
                result_list = [dict(zip(column_names, row)) for row in order_products_data]
                return result_list

        except Exception as e:
            print(f"Error in get_order_products_by_order_id: {e}")

        return []

    def get_orders_by_order_id(self, user_id: int):
        """
        Retrieve orders from the bot_app_order table based on the provided user_id and status.

        :param user_id: The user_id to filter orders.
        :return: List of order data tuples.
        """
        sql = "SELECT * FROM bot_app_order WHERE order_id = ?"
        orders_data = self.execute(sql, (user_id,), fetchall=True)
        return orders_data

    def get_admin_by_chat_id(self, chat_id: int):
        """
        Retrieve admin data from the bot_app_admin table based on the provided chat_id.

        :param chat_id: The chat_id to filter admins.
        :return: Admin data as a dictionary or None if not found.
        """
        sql = "SELECT * FROM bot_app_admin WHERE chat_id = ?"
        admin_data = self.execute(sql, (chat_id,), fetchone=True)
        return admin_data


    def get_orders_by_user_and_status(self, user_id: int):
        """
        Retrieve orders from the bot_app_order table based on the provided user_id and status.
        Include both column names and values in the result.

        :param user_id: The user_id to filter orders.
        :return: List of dictionaries, each containing column names and values, or an empty list if not found.
        """
        try:
            sql = "SELECT * FROM bot_app_order WHERE user_id = ? AND status = 1"
            orders_data = self.execute(sql, (user_id,), fetchall=True)

            if orders_data:
                # Explicitly list the column names
                column_names = ['id','order_id','status','amount','created_at','user_id' ]

                # Combine column names with values for each row
                result_list = [dict(zip(column_names, row)) for row in orders_data]
                return result_list


        except Exception as e:
            print(f"Error in get_orders_by_user_and_status: {e}")

        return []

    def deactivate_orders_by_user_id(self, order_id: int):
        """
        Deactivate orders for a specific user by updating their status from 1 to 0.

        :param user_id: The user_id for which orders need to be deactivated.
        """
        try:
            # Update orders status from 1 to 0
            sql = "UPDATE bot_app_order SET status = 0 WHERE order_id = ? AND status = 1"
            self.execute(sql, (order_id,), commit=True)

            print(f"Orders for user_id {order_id} deactivated successfully.")

        except Exception as e:
            print(f"Error in deactivate_orders_by_user_id: {e}")

    def get_order_products_by_order_id(self, order_id: int):
        """
        Retrieve order products from the bot_app_orderproduct table based on the provided order_id.

        :param order_id: The order_id to filter order products.
        :return: List of order product data tuples.
        """
        sql = "SELECT * FROM bot_app_orderproduct WHERE id = ?"

        # Assuming self.execute is a method for executing SQL queries in your class
        order_products_data = self.execute(sql, (order_id,), fetchall=True)

        return order_products_data
    def get_products_by_category_id(self, category_id: int):
        """
        Retrieve products from the bot_app_product table based on the provided category_id.

        :param category_id: The id of the category to filter products.
        :return: List of product data tuples.
        """
        sql = "SELECT * FROM bot_app_product WHERE category_id = ?"
        products_data = self.execute(sql, (category_id,), fetchall=True)
        return products_data

    def get_shop_name_parent_id(self, parent_id: int):
        """
        Retrieve products from the bot_app_product table based on the provided category_id.

        :param category_id: The id of the category to filter products.
        :return: List of product data tuples.
        """
        sql = "SELECT * FROM bot_app_shop_name WHERE parent_id =  ?"
        products_data = self.execute(sql, (parent_id,), fetchall=True)
        return products_data

    def get_shop_hierarchy_by_id(self, shop_id: int):
        """
        Retrieve the hierarchical information of a shop and its ancestors based on the provided shop_id.

        :param shop_id: The id of the shop to retrieve hierarchy information.
        :return: Shop hierarchy data as a dictionary.
        """
        sql = """
            SELECT a.id AS id_10, a.name_uz AS name_uz_10, a.parent_id AS parent_id_10,
                   b.id AS parent_id, b.name_uz AS parent_name_uz,
                   c.id AS grandparent_id, c.name_uz AS grandparent_name_uz,
                   d.id AS great_grandparent_id, d.name_uz AS great_grandparent_name_uz
            FROM bot_app_shop_name a
            JOIN bot_app_shop_name b ON a.parent_id = b.id
            LEFT JOIN bot_app_shop_name c ON b.parent_id = c.id
            LEFT JOIN bot_app_shop_name d ON c.parent_id = d.id
            WHERE a.id = ?
        """
        shop_hierarchy_data = self.execute(sql, (shop_id,), fetchone=True)

        # Convert the result to a dictionary with column names as keys
        result_dict = {
            'id_10': shop_hierarchy_data[0],
            'name_uz': shop_hierarchy_data[1],
            'parent_id_1': shop_hierarchy_data[2],
            'parent_id': shop_hierarchy_data[3],
            'parent_name_uz': shop_hierarchy_data[4],
            'grandparent_id': shop_hierarchy_data[5],
            'grandparent_name_uz': shop_hierarchy_data[6],
            'great_grandparent_id': shop_hierarchy_data[7],
            'great_grandparent_name_uz': shop_hierarchy_data[8]
        }

        return result_dict

    def update_user_field(self, chat_id: int, key: str, value: str):
        """
        Update a field in the bot_app_user table based on chat_id.

        :param chat_id: The chat_id of the user.
        :param field: The field name to update.
        :param value: The new value for the field.
        """
        sql = f"UPDATE bot_app_user SET {key} = ? WHERE chat_id = ?"
        self.execute(sql, (value, chat_id), commit=True)

    def add_user(self, chat_id: int):
        """
        Add a new user to the bot_app_user table with the specified chat_id.

        :param chat_id: The chat_id of the user.
        """
        sql = """
            INSERT INTO bot_app_user(chat_id)
            VALUES (?)
        """
        self.execute(sql, (chat_id,), commit=True)

