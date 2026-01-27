import sqlite3
from datetime import datetime

class product:
    def __init__(self, name, price, quantity):
        """
        A product represents a single item in our inventory.
        Attributes: 
        name: string, product name(eg, "soap")
        price:float, price per unit
        quantity: int, how many are stock.
        sold_quantity: int, how many we've sold(start at 0)
        """
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sold_quantity = 0

    def sell(self, amount):
        """
        Sell a certain amount

        1.Check if stock is enough.
        2. reduce our stock.
        3. add sold_quantity.
        4. calculate money earned.

        return: Total_money earned or 0 if no sell
        """

        if amount > self.quantity:
            print(f"❌ Not enough {self.name}! Available: {self.quantity}")
            return 0
        
        self.quantity -= amount #remove from stock 
        self.sold_quantity += amount #add sold_quantity
        total_price = amount * self.price #calculate money 

        print(f"✅Sold {amount} {self.name}(s) for ${total_price:.2f}")
        return total_price
    
    def restock(self, amount):
        """Add more"""
        if amount < 0:
            print(f"❌ Cannot restock negative amount!")
            return
        
        self.quantity += amount
        print(f"📦 Restocked {amount} {self.name}(s). Total: {self.quantity}")

    def __str__(self):
        """String representation for printing."""
        return f"{self.name}: ${self.price:.2f}| Stock: {self.quantity} | Sold: {self.sold_quantity}"
    
    
class DatabaseManager:
    """ 
    Manages all database operations.
    -Create Tables
    -Saving Products
    -Recording sales
    - Fetching data
    """

    def __init__(self, db_name = "inventory.db"):
        """
        connect to sqlite Database
        sqlite stores data in a single file (inventory.db)
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
       
       #Products table - stores product information
        self.cursor.execute(
            """
             CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                sold_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

             )
            """
        )

        #Sales table -records every sale
        self.cursor.execute("""

         CREATE TABLES IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity_sold INTEGER NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESATMP,
            FOREIGN KEY (product_name) REFRENCES products(name)                                        
                            
        )
        """)
        
        #Add daily_sales table for reports
        self.cursor.execute("""
        CREATE TABLES IF NOT EXISTS daily_sales(
            date DATE PRIMARY KEY,
            total_sales REAL DEFAULT 0, 
            items_sold INTEGER DEFAULT 0               
        )
                            
        """)
        self.conn.commit()
        print("✅ Database tables created/verified")

    def add_product(self, name, price, quantity):
        """Add a new product or update.
        
          sqlite uses ? as placeholder to prevent sql injection attacks.
        """

        #Error handling 
        try:
            self.cursor.execute(
                """
            INSERT INTO products (name, price, quantity)
            VALUES(?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
            quantity = quantity +?
        """, (name, price, quantity, quantity))
            
            self.conn.commit()
            print(f"✅ Product '{name}' added/updated")
            return True
        except Exception as e:
            print(f"❌Error adding product: {e}")
            return False
        
    def sell_product(self, name, quantity):
        """
        1.Check if product exists and has enough stock
        2.Update product quantity
        3.Record sale in sales table
        4.Update daily sales summary
        """
        try:
            #Check product existence
            self.cursor.execute(
                """SELECT price, quantity FROM products WHERE name = ?""",
                (name,)
            )
            product = self.cursor.fetchone()

            if not product:
                print(f"❌ Product '{name}' not found!")
                return False
            
            price, current_stock = product

            #check if stock is enough
            if current_stock < quantity:
                print(f"❌Not enough stock! Available: {current_stock}")
                return False
            total_price = price * quantity

            #Update product quantity
            self.cursor.execute(
                """
                
                """
            )