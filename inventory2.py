import sqlite3
from datetime import datetime

class Product:
    def __init__(self, name, price, quantity):
        """
        A Product represents a single item in our inventory.
        
        Attributes:
        - name: string, product name (e.g., "Soap")
        - price: float, price per unit
        - quantity: int, how many we have in stock
        - sold_quantity: int, how many we've sold (starts at 0)
        """
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sold_quantity = 0
    
    def sell(self, amount):
        """
        Sell a certain amount of this product.
        
        Steps:
        1. Check if we have enough stock
        2. Reduce our stock
        3. Increase sold count
        4. Calculate money earned
        
        Returns: Total price (or 0 if can't sell)
        """
        if amount > self.quantity:
            print(f"❌ Not enough {self.name}! Available: {self.quantity}")
            return 0 
        
        self.quantity -= amount  # Remove from stock
        self.sold_quantity += amount  # Add to sold count
        total_price = amount * self.price  # Calculate money
        
        print(f"✅ Sold {amount} {self.name}(s) for ${total_price:.2f}")
        return total_price
    
    def restock(self, amount):
        """Add more items to our stock."""
        if amount < 0:
            print("❌ Cannot restock negative amount!")
            return
            
        self.quantity += amount
        print(f"📦 Restocked {amount} {self.name}(s). Total: {self.quantity}")
    
    def __str__(self):
        """String representation for printing."""
        return f"{self.name}: ${self.price:.2f} | Stock: {self.quantity} | Sold: {self.sold_quantity}"


class DatabaseManager:
    """
    Manages all database operations.
    Think of this as a "data storage expert" who handles:
    - Creating tables
    - Saving products
    - Recording sales
    - Fetching data
    """
    
    def __init__(self, db_name="inventory.db"):
        """
        Connect to SQLite database.
        SQLite stores data in a single file (inventory.db).
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        
        # Products table - stores product information
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                sold_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sales table - records every sale
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity_sold INTEGER NOT NULL,
                total_price REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_name) REFERENCES products(name)
            )
        """)
        
        # Add daily_sales table for reports
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_sales (
                date DATE PRIMARY KEY,
                total_sales REAL DEFAULT 0,
                items_sold INTEGER DEFAULT 0
            )
        """)
        
        self.conn.commit()
        print("✅ Database tables created/verified")
    
    def add_product(self, name, price, quantity):
        """
        Add a new product or update existing one.
        
        SQLite uses ? as placeholder to prevent SQL injection attacks.
        """
        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, quantity) 
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET 
                quantity = quantity + ?
            """, (name, price, quantity, quantity))
            
            self.conn.commit()
            print(f"✅ Product '{name}' added/updated")
            return True
        except Exception as e:
            print(f"❌ Error adding product: {e}")
            return False
    
    def sell_product(self, name, quantity):
        """
        Process a sale:
        1. Check if product exists and has enough stock
        2. Update product quantity
        3. Record sale in sales table
        4. Update daily sales summary
        """
        try:
            # 1. Check product exists and get current stock
            self.cursor.execute(
                "SELECT price, quantity FROM products WHERE name = ?", 
                (name,)
            )
            product = self.cursor.fetchone()
            
            if not product:
                print(f"❌ Product '{name}' not found!")
                return False
                
            price, current_stock = product
            
            # 2. Check if we have enough stock
            if current_stock < quantity:
                print(f"❌ Not enough stock! Available: {current_stock}")
                return False
            
            total_price = price * quantity
            
            # 3. Update product quantity
            self.cursor.execute("""
                UPDATE products 
                SET quantity = quantity - ?, 
                    sold_quantity = sold_quantity + ?
                WHERE name = ?
            """, (quantity, quantity, name))
            
            # 4. Record the sale
            self.cursor.execute("""
                INSERT INTO sales (product_name, quantity_sold, total_price)
                VALUES (?, ?, ?)
            """, (name, quantity, total_price))
            
            # 5. Update daily sales summary
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                INSERT INTO daily_sales (date, total_sales, items_sold)
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                total_sales = total_sales + ?,
                items_sold = items_sold + ?
            """, (today, total_price, quantity, total_price, quantity))
            
            self.conn.commit()
            print(f"✅ Sold {quantity} {name}(s) for ${total_price:.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error processing sale: {e}")
            return False
    
    def get_all_products(self):
        """Get all products from database."""
        self.cursor.execute("SELECT name, price, quantity, sold_quantity FROM products")
        return self.cursor.fetchall()
    
    def get_product(self, name):
        """Get specific product details."""
        self.cursor.execute(
            "SELECT name, price, quantity, sold_quantity FROM products WHERE name = ?", 
            (name,)
        )
        return self.cursor.fetchone()
    
    def get_daily_report(self, date=None):
        """Get sales report for a specific day."""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "SELECT total_sales, items_sold FROM daily_sales WHERE date = ?",
            (date,)
        )
        return self.cursor.fetchone()
    
    def get_low_stock_products(self, threshold=5):
        """Get products with low stock (below threshold)."""
        self.cursor.execute(
            "SELECT name, quantity FROM products WHERE quantity < ?",
            (threshold,)
        )
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection."""
        self.conn.close()


class Inventory:
    """
    Main inventory system that combines:
    - Product logic (Product class)
    - Database operations (DatabaseManager class)
    - Business rules
    """
    
    def __init__(self):
        """Initialize with a database connection."""
        self.db = DatabaseManager()
        self.total_cash = self.calculate_total_cash()
    
    def calculate_total_cash(self):
        """Calculate total cash from all sales."""
        try:
            self.db.cursor.execute("SELECT SUM(total_price) FROM sales")
            result = self.db.cursor.fetchone()
            return result[0] if result[0] else 0
        except:
            return 0
    
    def add_product(self, name, price, quantity):
        """Add new product or restock existing one."""
        if price < 0:
            print("❌ Price cannot be negative!")
            return
        if quantity < 0:
            print("❌ Quantity cannot be negative!")
            return
            
        return self.db.add_product(name, price, quantity)
    
    def sell_product(self, name, quantity):
        """Sell a product."""
        if quantity <= 0:
            print("❌ Quantity must be positive!")
            return False
            
        success = self.db.sell_product(name, quantity)
        if success:
            self.total_cash += self.get_product_price(name) * quantity
        return success
    
    def get_product_price(self, name):
        """Get price of a product."""
        product = self.db.get_product(name)
        return product[1] if product else 0
    
    def show_summary(self):
        """Display inventory summary."""
        products = self.db.get_all_products()
        
        print("\n" + "="*50)
        print("📊 INVENTORY SUMMARY")
        print("="*50)
        
        if not products:
            print("No products in inventory")
            return
            
        total_value = 0
        for product in products:
            name, price, quantity, sold = product
            value = price * quantity
            total_value += value
            print(f"• {name:<15} | Price: ${price:<7.2f} | "
                  f"Stock: {quantity:<4} | Sold: {sold:<4} | "
                  f"Value: ${value:<7.2f}")
        
        print("-"*50)
        print(f"Total products: {len(products)}")
        print(f"Total inventory value: ${total_value:.2f}")
        print(f"Total cash earned: ${self.total_cash:.2f}")
        print("="*50)
    
    def show_low_stock(self, threshold=5):
        """Show products running low."""
        low_stock = self.db.get_low_stock_products(threshold)
        
        print("\n" + "="*50)
        print(f"📉 LOW STOCK ALERT (below {threshold})")
        print("="*50)
        
        if not low_stock:
            print("All products have sufficient stock ✓")
        else:
            for product in low_stock:
                print(f"⚠️  {product[0]}: Only {product[1]} left!")
        print("="*50)
    
    def show_daily_report(self, date=None):
        """Show sales report for a day."""
        report = self.db.get_daily_report(date)
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        print("\n" + "="*50)
        print(f"📈 DAILY SALES REPORT - {date}")
        print("="*50)
        
        if report:
            total_sales, items_sold = report
            print(f"Total Sales: ${total_sales:.2f}")
            print(f"Items Sold: {items_sold}")
            print(f"Average Sale: ${total_sales/items_sold:.2f}" if items_sold > 0 else "No sales")
        else:
            print("No sales recorded for this date")
        print("="*50)
    
    def export_to_csv(self, filename="inventory_report.csv"):
        """Export inventory to CSV file."""
        import csv
        
        products = self.db.get_all_products()
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Product', 'Price', 'Stock', 'Sold', 'Total Value'])
            
            for product in products:
                name, price, quantity, sold = product
                total_value = price * quantity
                writer.writerow([name, price, quantity, sold, total_value])
        
        print(f"✅ Exported to {filename}")
    
    def close(self):
        """Close database connection."""
        self.db.close()


# ============================================================================
# SIMPLE COMMAND LINE INTERFACE
# ============================================================================

def main_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print("🏪 INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add/Restock Product")
    print("2. Sell Product")
    print("3. View Inventory Summary")
    print("4. Check Low Stock")
    print("5. View Daily Report")
    print("6. Export to CSV")
    print("7. Exit")
    print("="*50)

def run_cli():
    """Run command line interface."""
    inventory = Inventory()
    
    while True:
        main_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n➕ ADD/RESTOCK PRODUCT")
            name = input("Product name: ").strip()
            
            try:
                price = float(input("Price per unit: $"))
                quantity = int(input("Quantity: "))
                inventory.add_product(name, price, quantity)
            except ValueError:
                print("❌ Invalid input! Please enter numbers for price and quantity.")
        
        elif choice == "2":
            print("\n💰 SELL PRODUCT")
            name = input("Product name: ").strip()
            
            try:
                quantity = int(input("Quantity to sell: "))
                inventory.sell_product(name, quantity)
            except ValueError:
                print("❌ Invalid input! Please enter a number for quantity.")
        
        elif choice == "3":
            inventory.show_summary()
        
        elif choice == "4":
            try:
                threshold = int(input("Low stock threshold (default 5): ") or 5)
                inventory.show_low_stock(threshold)
            except ValueError:
                print("❌ Invalid threshold!")
        
        elif choice == "5":
            date = input("Date (YYYY-MM-DD) or Enter for today: ").strip()
            inventory.show_daily_report(date if date else None)
        
        elif choice == "6":
            filename = input("CSV filename (default: inventory_report.csv): ").strip()
            inventory.export_to_csv(filename if filename else "inventory_report.csv")
        
        elif choice == "7":
            print("\n👋 Goodbye!")
            inventory.close()
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-7.")
        
        input("\nPress Enter to continue...")
#===========================
#Run program
#===========================

if __name__ == "__main__":
    print("\n🚀 Starting Inventory Management System...")
    run_cli()