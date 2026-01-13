import json
import os
from typing import List, Dict, Optional
from models import Product, Sale, Return
import uuid
from datetime import datetime


class POSService:
    """POS system service"""

    def __init__(self):
        self.inventory_file = "inventory.json"
        self.sales_file = "sales.json"
        self.returns_file = "returns.json"
        self.products = self._load_inventory()

    def _load_inventory(self) -> Dict[str, Product]:
        """Load inventory"""
        if not os.path.exists(self.inventory_file):
            # Create sample products
            sample_products = [
                Product("001", "Apple", 5.0, 100),
                Product("002", "Banana", 3.0, 150),
                Product("003", "Orange", 4.5, 80),
                Product("004", "Milk", 8.0, 50),
                Product("005", "Bread", 6.5, 60),
                Product("006", "Egg", 12.0, 30),
                Product("007", "Water", 2.0, 200),
                Product("008", "Chocolate", 10.0, 40)
            ]
            self._save_inventory({p.product_id: p for p in sample_products})

        with open(self.inventory_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {pid: Product.from_dict(pdata) for pid, pdata in data.items()}

    def _save_inventory(self, products: Dict[str, Product]):
        """Save inventory"""
        data = {pid: product.to_dict() for pid, product in products.items()}
        with open(self.inventory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_sale(self, sale: Sale):
        """Save sales records"""
        if os.path.exists(self.sales_file):
            with open(self.sales_file, 'r', encoding='utf-8') as f:
                sales_data = json.load(f)
        else:
            sales_data = {}

        sales_data[sale.sale_id] = sale.to_dict()

        with open(self.sales_file, 'w', encoding='utf-8') as f:
            json.dump(sales_data, f, ensure_ascii=False, indent=2)

    def _save_return(self, return_obj: Return):
        """Save return records"""
        if os.path.exists(self.returns_file):
            with open(self.returns_file, 'r', encoding='utf-8') as f:
                returns_data = json.load(f)
        else:
            returns_data = {}

        returns_data[return_obj.return_id] = return_obj.to_dict()

        with open(self.returns_file, 'w', encoding='utf-8') as f:
            json.dump(returns_data, f, ensure_ascii=False, indent=2)

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        return self.products.get(product_id)

    def list_products(self) -> List[Product]:
        """List all products"""
        return list(self.products.values())

    def process_sale(self) -> Optional[Sale]:
        """Process sale"""
        print("\n" + "=" * 50)
        print("                PROCESS SALE")
        print("=" * 50)

        # Generate unique order number
        sale_id = f"SALE-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        sale = Sale(sale_id)

        while True:
            print("\nAvailable Products:")
            for product in self.list_products():
                print(f"  {product.product_id}: {product.name} - ¥{product.price:.2f} (Stock: {product.stock})")

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

                # Add product to sale
                sale.add_item(product, quantity)
                print(f"Added: {product.name} × {quantity}")
                print(f"Current Total: ¥{sale.total:.2f}")

            except ValueError:
                print("Error: Please enter a valid number")

        if not sale.items:
            print("No items added, sale cancelled")
            return None

        # Show total amount
        print(f"\nOrder Total: ¥{sale.total:.2f}")

        # Process payment
        payment_methods = {
            '1': 'Cash',
            '2': 'WeChat Pay',
            '3': 'Alipay',
            '4': 'Bank Card'
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

        # Enter payment amount
        while True:
            try:
                amount = float(input(f"Enter payment amount (minimum ¥{sale.total:.2f}): "))
                if sale.process_payment(payment_method, amount):
                    change = amount - sale.total
                    print(f"Payment successful! Change: ¥{change:.2f}")
                    break
                else:
                    print(f"Insufficient amount, minimum required: ¥{sale.total:.2f}")
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

    def process_return(self) -> Optional[Return]:
        """Process return"""
        print("\n" + "=" * 50)
        print("                PROCESS RETURN")
        print("=" * 50)

        # Check if there are sales records
        if not os.path.exists(self.sales_file):
            print("Error: No sales records")
            return None

        with open(self.sales_file, 'r', encoding='utf-8') as f:
            sales_data = json.load(f)

        print("Recent Sales Records:")
        sale_ids = list(sales_data.keys())[-5:]  # Show last 5 records
        for sale_id in sale_ids:
            sale = sales_data[sale_id]
            print(f"  Order ID: {sale_id}, Time: {sale['datetime'][:19]}, Amount: ¥{sale['total']:.2f}")

        while True:
            sale_id = input("\nEnter order ID to return (or enter 'cancel'): ").strip()

            if sale_id.lower() == 'cancel':
                return None

            if sale_id not in sales_data:
                print("Error: Order ID does not exist")
                continue

            original_sale = sales_data[sale_id]
            break

        # Generate return ID
        return_id = f"RETURN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        return_obj = Return(return_id, sale_id)

        print(f"\nOriginal Order Items:")
        for i, item in enumerate(original_sale['items'], 1):
            print(f"  {i}. {item['product_name']} × {item['quantity']} = ¥{item['subtotal']:.2f}")

        while True:
            print("\nEnter item number to return, 'done' to finish, 'cancel' to abort return")
            choice = input("Selection: ").strip()

            if choice.lower() == 'done':
                break
            elif choice.lower() == 'cancel':
                print("Return cancelled")
                return None

            try:
                item_idx = int(choice) - 1
                if item_idx < 0 or item_idx >= len(original_sale['items']):
                    print("Error: Invalid item number")
                    continue

                original_item = original_sale['items'][item_idx]
                product_id = original_item['product_id']

                # Get product object
                product = self.get_product_by_id(product_id)
                if not product:
                    print(f"Error: Product {original_item['product_name']} does not exist")
                    continue

                max_qty = original_item['quantity']
                try:
                    quantity = int(input(f"Enter return quantity (maximum {max_qty}): "))
                    if quantity <= 0 or quantity > max_qty:
                        print(f"Error: Quantity must be between 1 and {max_qty}")
                        continue
                except ValueError:
                    print("Error: Please enter a valid number")
                    continue

                reason = input("Enter return reason: ").strip() or "No reason"

                # Add to return
                return_obj.add_item(product, quantity, reason)
                print(f"Added return: {product.name} × {quantity}")
                print(f"Current refund amount: ¥{return_obj.refund_amount:.2f}")

            except ValueError:
                print("Error: Please enter a valid number")

        if not return_obj.items:
            print("No items added to return")
            return None

        # Show refund information
        print(f"\nTotal refund amount: ¥{return_obj.refund_amount:.2f}")

        # Confirm refund
        confirm = input("Confirm refund? (y/n): ").lower()
        if confirm != 'y':
            print("Return cancelled")
            return None

        # Update inventory
        for item in return_obj.items:
            product = item['product']
            product.stock += item['quantity']

        # Save data
        self._save_inventory(self.products)
        self._save_return(return_obj)

        # Show return receipt
        print("\n" + "=" * 50)
        print("                RETURN RECEIPT")
        print("=" * 50)
        print(f"Return ID: {return_obj.return_id}")
        print(f"Original Order ID: {return_obj.original_sale_id}")
        print(f"Time: {return_obj.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        for item in return_obj.items:
            product = item['product']
            refund = product.price * item['quantity']
            print(f"{product.name:20} ×{item['quantity']:3} ¥{refund:8.2f}")
            print(f"  Reason: {item['reason']}")

        print("-" * 50)
        print(f"Total refund amount: ¥{return_obj.refund_amount:.2f}")
        print("=" * 50)
        print("        Refund will be processed within 3 business days")
        print("=" * 50)

        return return_obj

    def show_inventory(self):
        """Show inventory"""
        print("\n" + "=" * 50)
        print("                INVENTORY STATUS")
        print("=" * 50)

        products = self.list_products()
        if not products:
            print("No products")
            return

        total_value = 0
        for product in products:
            value = product.price * product.stock
            total_value += value
            print(
                f"{product.product_id:5} {product.name:15} ¥{product.price:8.2f} × {product.stock:4} = ¥{value:10.2f}")

        print("-" * 50)
        print(f"Total inventory value: ¥{total_value:.2f}")
        print("=" * 50)
