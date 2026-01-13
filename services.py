"""
POS Service Module - Day 2
Core business logic for sale processing
"""

import json
import os
from datetime import datetime
import uuid


class Product:
    """Product class representing items in inventory"""

    def __init__(self, product_id: str, name: str, price: float, stock: int = 0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self):
        """Convert product to dictionary for JSON storage"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    @classmethod
    def from_dict(cls, data):
        """Create product from dictionary"""
        return cls(data['product_id'], data['name'], data['price'], data['stock'])

    def __str__(self):
        return f"{self.name} (ID: {self.product_id}) - ${self.price:.2f} - Stock: {self.stock}"


class SaleItem:
    """Individual item in a sale transaction"""

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity} = ${self.subtotal:.2f}"


class Sale:
    """Sales transaction record"""

    def __init__(self, sale_id: str):
        self.sale_id = sale_id
        self.items = []
        self.datetime = datetime.now()
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.payment_method = ""
        self.payment_status = False

    def add_item(self, product: Product, quantity: int):
        """Add item to sale"""
        item = SaleItem(product, quantity)
        self.items.append(item)
        self._calculate_totals()

    def _calculate_totals(self):
        """Calculate sale totals"""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax = self.subtotal * 0.10  # 10% tax
        self.total = self.subtotal + self.tax

    def process_payment(self, payment_method: str, amount: float) -> bool:
        """Process payment for the sale"""
        self.payment_method = payment_method
        if amount >= self.total:
            self.payment_status = True
            return True
        return False

    def to_dict(self):
        """Convert sale to dictionary for JSON storage"""
        return {
            'sale_id': self.sale_id,
            'datetime': self.datetime.isoformat(),
            'items': [
                {
                    'product_id': item.product.product_id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'subtotal': item.subtotal
                }
                for item in self.items
            ],
            'subtotal': self.subtotal,
            'tax': self.tax,
            'total': self.total,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status
        }

    def print_receipt(self):
        """Print sales receipt"""
        print("\n" + "=" * 50)
        print("               SALES RECEIPT")
        print("=" * 50)
        print(f"Sale ID: {self.sale_id}")
        print(f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        for item in self.items:
            print(f"{item.product.name:20} ×{item.quantity:3} ${item.product.price:7.2f} ${item.subtotal:8.2f}")

        print("-" * 50)
        print(f"Subtotal: ${self.subtotal:10.2f}")
        print(f"Tax (10%): ${self.tax:8.2f}")
        print(f"Total: ${self.total:10.2f}")
        print(f"Payment Method: {self.payment_method}")
        print("=" * 50)
        print("      Thank you for shopping with us!")
        print("=" * 50)

class ReturnItem:
    """Individual item in a return transaction"""

    def __init__(self, product: Product, quantity: int, reason: str):
        self.product = product
        self.quantity = quantity
        self.reason = reason
        self.refund_amount = product.price * quantity
        self.returns_file = "data/returns.json"

    def __str__(self):
        return f"{self.product.name} × {self.quantity} = ${self.refund_amount:.2f} (Reason: {self.reason})"

    def _save_return(self, return_obj: Return):
        """Save return record to JSON file"""
        if os.path.exists(self.returns_file):
            with open(self.returns_file, 'r', encoding='utf-8') as f:
                returns_data = json.load(f)
        else:
            returns_data = {}

        returns_data[return_obj.return_id] = return_obj.to_dict()

        with open(self.returns_file, 'w', encoding='utf-8') as f:
            json.dump(returns_data, f, ensure_ascii=False, indent=2)

    def start_return_process(self):
        """Start return process (basic framework)"""
        print("\n" + "=" * 50)
        print("              PROCESS RETURN")
        print("=" * 50)
        print("Return functionality under development...")
        print("Full feature will be available in next version")
        input("\nPress Enter to return...")
        return None


class Return:
    """Return transaction record"""

    def __init__(self, return_id: str, original_sale_id: str):
        self.return_id = return_id
        self.original_sale_id = original_sale_id
        self.datetime = datetime.now()
        self.items = []
        self.refund_amount = 0.0

    def add_item(self, product: Product, quantity: int, reason: str):
        """Add item to return"""
        item = ReturnItem(product, quantity, reason)
        self.items.append(item)
        self.refund_amount += item.refund_amount

    def to_dict(self):
        """Convert return to dictionary for JSON storage"""
        return {
            'return_id': self.return_id,
            'original_sale_id': self.original_sale_id,
            'datetime': self.datetime.isoformat(),
            'items': [
                {
                    'product_id': item.product.product_id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'refund': item.refund_amount,
                    'reason': item.reason
                }
                for item in self.items
            ],
            'refund_amount': self.refund_amount
        }

    def print_return_receipt(self):
        """Print return receipt"""
        print("\n" + "=" * 50)
        print("             RETURN RECEIPT")
        print("=" * 50)
        print(f"Return ID: {self.return_id}")
        print(f"Original Sale ID: {self.original_sale_id}")
        print(f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        for item in self.items:
            print(f"{item.product.name:20} ×{item.quantity:3} ${item.refund_amount:8.2f}")
            print(f"  Reason: {item.reason}")

        print("-" * 50)
        print(f"Total Refund Amount: ${self.refund_amount:.2f}")
        print("=" * 50)
        print("   Refund will be processed within 3 business days")
        print("=" * 50)


class POSService:
    """Main POS service handling business logic"""

    def __init__(self):
        self.inventory_file = "data/inventory.json"
        self.sales_file = "data/sales.json"
        self.products = self._load_inventory()

    def _load_inventory(self):
        """Load inventory from JSON file"""
        if not os.path.exists(self.inventory_file):
            # Create sample products if file doesn't exist
            sample_products = [
                Product("001", "Apple", 1.50, 100),
                Product("002", "Banana", 0.75, 150),
                Product("003", "Orange", 1.20, 80),
                Product("004", "Milk", 2.50, 50)
            ]
            self._save_inventory({p.product_id: p for p in sample_products})

        with open(self.inventory_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {pid: Product.from_dict(pdata) for pid, pdata in data.items()}

    def _save_inventory(self, products):
        """Save inventory to JSON file"""
        data = {pid: product.to_dict() for pid, product in products.items()}
        with open(self.inventory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_sale(self, sale: Sale):
        """Save sale record to JSON file"""
        if os.path.exists(self.sales_file):
            with open(self.sales_file, 'r', encoding='utf-8') as f:
                sales_data = json.load(f)
        else:
            sales_data = {}

        sales_data[sale.sale_id] = sale.to_dict()

        with open(self.sales_file, 'w', encoding='utf-8') as f:
            json.dump(sales_data, f, ensure_ascii=False, indent=2)

    def get_product_by_id(self, product_id: str):
        """Get product by ID"""
        return self.products.get(product_id)

    def list_products(self):
        """List all products"""
        return list(self.products.values())

    def process_sale(self):
        """Process a complete sale transaction"""
        print("\n" + "=" * 50)
        print("              PROCESS SALE")
        print("=" * 50)

        # Generate unique sale ID
        sale_id = f"SALE-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        sale = Sale(sale_id)

        while True:
            print("\nAvailable Products:")
            for product in self.list_products():
                print(f"  {product.product_id}: {product.name} - ${product.price:.2f} (Stock: {product.stock})")

            print("\nEnter product ID to add item, 'done' to finish, 'cancel' to abort sale")
            product_id = input("Product ID: ").strip()

            if product_id.lower() == 'done':
                break
            elif product_id.lower() == 'cancel':
                print("Sale cancelled")
                return None

            product = self.get_product_by_id(product_id)
            if not product:
                print(f"Error: Product ID '{product_id}' does not exist")
                continue

            try:
                quantity = int(input(f"Enter quantity for {product.name}: "))
                if quantity <= 0:
                    print("Error: Quantity must be greater than 0")
                    continue

                if quantity > product.stock:
                    print(f"Error: Insufficient stock. Available: {product.stock}")
                    continue

                # Add item to sale
                sale.add_item(product, quantity)
                print(f"Added: {product.name} × {quantity}")
                print(f"Current Total: ${sale.total:.2f}")

            except ValueError:
                print("Error: Please enter a valid number")

        if not sale.items:
            print("No items added. Sale cancelled.")
            return None

        # Show final total
        print(f"\nOrder Total: ${sale.total:.2f}")

        # Process payment
        payment_methods = {
            '1': 'Cash',
            '2': 'Credit Card',
            '3': 'Debit Card',
            '4': 'Mobile Payment'
        }

        print("\nSelect Payment Method:")
        for key, method in payment_methods.items():
            print(f"  {key}: {method}")

        while True:
            choice = input("Select payment method (1-4): ").strip()
            if choice in payment_methods:
                payment_method = payment_methods[choice]
                break
            print("Error: Invalid selection")

        # Input payment amount
        while True:
            try:
                amount = float(input(f"Enter payment amount (minimum ${sale.total:.2f}): "))
                if sale.process_payment(payment_method, amount):
                    change = amount - sale.total
                    print(f"Payment successful! Change: ${change:.2f}")
                    break
                else:
                    print(f"Insufficient amount. Minimum required: ${sale.total:.2f}")
            except ValueError:
                print("Error: Please enter a valid amount")

        # Update inventory
        for item in sale.items:
            product = item.product
            product.stock -= item.quantity

        # Save data
        self._save_inventory(self.products)
        self._save_sale(sale)

        # Print receipt
        sale.print_receipt()

        return sale

    def show_inventory(self):
        """Display current inventory status"""
        print("\n" + "=" * 50)
        print("              INVENTORY STATUS")
        print("=" * 50)

        products = self.list_products()
        if not products:
            print("No products available")
            return

        total_value = 0
        for product in products:
            value = product.price * product.stock
            total_value += value
            print(
                f"{product.product_id:5} {product.name:15} ${product.price:8.2f} × {product.stock:4} = ${value:10.2f}")

        print("-" * 50)
        print(f"Total Inventory Value: ${total_value:.2f}")
        print("=" * 50)
