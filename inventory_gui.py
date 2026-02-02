import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from inventory2 import Inventory
from datetime import datetime

class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Inventory Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Status bar (create first)
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize inventory
        self.inventory = Inventory()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.add_product_tab()
        self.sell_product_tab()
        self.view_inventory_tab()
        self.low_stock_tab()
        self.daily_report_tab()
        self.export_tab()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def add_product_tab(self):
        """Tab for adding/restocking products."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="➕ Add/Restock Product")
        
        # Create form
        form_frame = ttk.LabelFrame(frame, text="Product Information", padding=15)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
        
        # Product name
        ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.add_name_entry = ttk.Entry(form_frame, width=30)
        self.add_name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Price
        ttk.Label(form_frame, text="Price per Unit ($):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.add_price_entry = ttk.Entry(form_frame, width=30)
        self.add_price_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.add_quantity_entry = ttk.Entry(form_frame, width=30)
        self.add_quantity_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Button
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text=" Add/Restock", 
                   command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Clear", 
                   command=self.clear_add_form).pack(side=tk.LEFT, padx=5)
        
        form_frame.columnconfigure(1, weight=1)
    
    def sell_product_tab(self):
        """Tab for selling products."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Sell Product")
        
        # Create form
        form_frame = ttk.LabelFrame(frame, text="Process Sale", padding=15)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
        
        # Product name
        ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sell_name_entry = ttk.Entry(form_frame, width=30)
        self.sell_name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Quantity to sell
        ttk.Label(form_frame, text="Quantity to Sell:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sell_quantity_entry = ttk.Entry(form_frame, width=30)
        self.sell_quantity_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Button
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text=" Process Sale", 
                   command=self.sell_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Clear", 
                   command=self.clear_sell_form).pack(side=tk.LEFT, padx=5)
        
        form_frame.columnconfigure(1, weight=1)
    
    def view_inventory_tab(self):
        """Tab for viewing inventory summary."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Inventory Summary")
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(padx=10, pady=10)
        ttk.Button(button_frame, text=" Refresh", 
                   command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        
        # Display area
        display_frame = ttk.LabelFrame(frame, text="Inventory", padding=10)
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.inventory_text = tk.Text(display_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.inventory_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.inventory_text.yview)
        
        # Display initial data
        self.refresh_inventory()
    
    def low_stock_tab(self):
        """Tab for checking low stock products."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Low Stock Alert")
        
        # Threshold input
        input_frame = ttk.Frame(frame)
        input_frame.pack(padx=10, pady=10)
        
        ttk.Label(input_frame, text="Low Stock Threshold:").pack(side=tk.LEFT, padx=5)
        self.threshold_entry = ttk.Entry(input_frame, width=10)
        self.threshold_entry.insert(0, "5")
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text=" Check", 
                   command=self.check_low_stock).pack(side=tk.LEFT, padx=5)
        
        # Display area
        display_frame = ttk.LabelFrame(frame, text="Low Stock Products", padding=10)
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.low_stock_text = tk.Text(display_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.low_stock_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.low_stock_text.yview)
    
    def daily_report_tab(self):
        """Tab for viewing daily sales reports."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Daily Report")
        
        # Date input
        input_frame = ttk.Frame(frame)
        input_frame.pack(padx=10, pady=10)
        
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.report_date_entry = ttk.Entry(input_frame, width=15)
        self.report_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.report_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text=" Get Report", 
                   command=self.get_daily_report).pack(side=tk.LEFT, padx=5)
        
        # Display area
        display_frame = ttk.LabelFrame(frame, text="Sales Report", padding=10)
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.report_text = tk.Text(display_frame, wrap=tk.WORD, height=15)
        self.report_text.pack(fill=tk.BOTH, expand=True)
    
    def export_tab(self):
        """Tab for exporting to CSV."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=" Export to CSV")
        
        info_frame = ttk.LabelFrame(frame, text="Export Options", padding=20)
        info_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(info_frame, text="Filename:").pack(pady=5)
        self.export_filename_entry = ttk.Entry(info_frame, width=40)
        self.export_filename_entry.insert(0, "inventory_report.csv")
        self.export_filename_entry.pack(pady=5)
        
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=" Export to CSV", 
                   command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=" Browse Location", 
                   command=self.browse_export_location).pack(side=tk.LEFT, padx=5)
        
        info_label = ttk.Label(info_frame, 
                               text="Select filename and click 'Export to CSV' to save.\nThe file will be saved in the current directory.",
                               wraplength=400, justify=tk.CENTER)
        info_label.pack(pady=20)
    
    # ===== Button Actions =====
    
    def add_product(self):
        """Add or restock a product."""
        try:
            name = self.add_name_entry.get().strip()
            price = float(self.add_price_entry.get())
            quantity = int(self.add_quantity_entry.get())
            
            if not name:
                messagebox.showwarning("Input Error", "Please enter a product name!")
                return
            
            self.inventory.add_product(name, price, quantity)
            messagebox.showinfo("Success", f" Added/Restocked '{name}'")
            self.clear_add_form()
            self.status_var.set(f"Added/Restocked: {name}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for price and quantity!")
    
    def clear_add_form(self):
        """Clear add product form."""
        self.add_name_entry.delete(0, tk.END)
        self.add_price_entry.delete(0, tk.END)
        self.add_quantity_entry.delete(0, tk.END)
    
    def sell_product(self):
        """Sell a product."""
        try:
            name = self.sell_name_entry.get().strip()
            quantity = int(self.sell_quantity_entry.get())
            
            if not name:
                messagebox.showwarning("Input Error", "Please enter a product name!")
                return
            
            success = self.inventory.sell_product(name, quantity)
            if success:
                messagebox.showinfo("Success", f" Sold {quantity} {name}(s)")
                self.clear_sell_form()
                self.status_var.set(f"Sold: {quantity} x {name}")
            else:
                messagebox.showerror("Sale Failed", f" Could not process sale")
                
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity!")
    
    def clear_sell_form(self):
        """Clear sell product form."""
        self.sell_name_entry.delete(0, tk.END)
        self.sell_quantity_entry.delete(0, tk.END)
    
    def refresh_inventory(self):
        """Refresh and display inventory summary."""
        self.inventory_text.config(state=tk.NORMAL)
        self.inventory_text.delete(1.0, tk.END)
        
        products = self.inventory.db.get_all_products()
        
        if not products:
            self.inventory_text.insert(tk.END, "No products in inventory")
            self.inventory_text.config(state=tk.DISABLED)
            return
        
        # Header
        header = f"{'Product':<20} {'Price':<10} {'Stock':<8} {'Sold':<8} {'Value':<10}\n"
        header += "=" * 60 + "\n"
        self.inventory_text.insert(tk.END, header)
        
        total_value = 0
        for product in products:
            name, price, quantity, sold = product
            value = price * quantity
            total_value += value
            line = f"{name:<20} ${price:<9.2f} {quantity:<8} {sold:<8} ${value:<9.2f}\n"
            self.inventory_text.insert(tk.END, line)
        
        # Footer
        footer = "\n" + "=" * 60 + "\n"
        footer += f"Total products: {len(products)}\n"
        footer += f"Total inventory value: ${total_value:.2f}\n"
        footer += f"Total cash earned: ${self.inventory.total_cash:.2f}"
        self.inventory_text.insert(tk.END, footer)
        
        self.inventory_text.config(state=tk.DISABLED)
        self.status_var.set("Inventory refreshed")
    
    def check_low_stock(self):
        """Check low stock products."""
        try:
            threshold = int(self.threshold_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid threshold!")
            return
        
        self.low_stock_text.config(state=tk.NORMAL)
        self.low_stock_text.delete(1.0, tk.END)
        
        low_stock = self.inventory.db.get_low_stock_products(threshold)
        
        if not low_stock:
            self.low_stock_text.insert(tk.END, f"✓ All products have sufficient stock (above {threshold})")
        else:
            self.low_stock_text.insert(tk.END, f" Products below threshold ({threshold} units):\n\n")
            for product in low_stock:
                line = f"• {product[0]}: Only {product[1]} left!\n"
                self.low_stock_text.insert(tk.END, line)
        
        self.low_stock_text.config(state=tk.DISABLED)
        self.status_var.set(f"Low stock check completed (threshold: {threshold})")
    
    def get_daily_report(self):
        """Get daily sales report."""
        date = self.report_date_entry.get().strip()
        
        if date and date != datetime.now().strftime("%Y-%m-%d"):
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Date Error", "Please enter date in YYYY-MM-DD format!")
                return
        else:
            date = None
        
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete(1.0, tk.END)
        
        report = self.inventory.db.get_daily_report(date)
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        header = f" DAILY SALES REPORT - {date}\n"
        header += "=" * 40 + "\n\n"
        self.report_text.insert(tk.END, header)
        
        if report:
            total_sales, items_sold = report
            self.report_text.insert(tk.END, f"Total Sales: ${total_sales:.2f}\n")
            self.report_text.insert(tk.END, f"Items Sold: {items_sold}\n")
            if items_sold > 0:
                avg = total_sales / items_sold
                self.report_text.insert(tk.END, f"Average Sale: ${avg:.2f}\n")
        else:
            self.report_text.insert(tk.END, "No sales recorded for this date")
        
        self.report_text.config(state=tk.DISABLED)
        self.status_var.set(f"Report generated for {date}")
    
    def export_to_csv(self):
        """Export inventory to CSV."""
        filename = self.export_filename_entry.get().strip()
        
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a filename!")
            return
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            self.inventory.export_to_csv(filename)
            messagebox.showinfo("Success", f" Exported to {filename}")
            self.status_var.set(f"Exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"❌ Error exporting: {e}")
    
    def browse_export_location(self):
        """Browse for export location."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=self.export_filename_entry.get()
        )
        if filename:
            self.export_filename_entry.delete(0, tk.END)
            self.export_filename_entry.insert(0, filename)
    
    def on_closing(self):
        """Handle window closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.inventory.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    gui = InventoryGUI(root)
    root.mainloop()
