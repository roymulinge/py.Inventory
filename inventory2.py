

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
    


    