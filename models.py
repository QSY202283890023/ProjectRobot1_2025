import json
from datetime import datetime
from typing import List, Dict, Optional


class Product:
    """Product class"""

    def __init__(self, product_id: str, name: str, price: float, stock: int = 0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create object from dictionary"""
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            price=data['price'],
            stock=data['stock']
        )

    def __str__(self) -> str:
        return f"{self.name} (ID: {self.product_id}) - ¥{self.price:.2f} - Stock: {self.stock}"


class SaleItem:
    """Sales item"""

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity

    def __str__(self) -> str:
        return f"{self.product.name} × {self.quantity} = ¥{self.subtotal:.2f}"


class Sale:
    """Sales order"""

    def __init__(self, sale_id: str):
        self.sale_id = sale_id
        self.items: List[SaleItem] = []
        self.datetime = datetime.now()
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.payment_method = ""
        self.payment_status = False

    def add_item(self, product: Product, quantity: int):
        """Add product to sales order"""
        item = SaleItem(product, quantity)
        self.items.append(item)
        self._calculate_totals()

    def _calculate_totals(self):
        """Calculate total amount"""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax = self.subtotal * 0.10  # Assume 10% tax
        self.total = self.subtotal + self.tax

    def process_payment(self, payment_method: str, amount: float) -> bool:
        """Process payment"""
        self.payment_method = payment_method
        if amount >= self.total:
            self.payment_status = True
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
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
        """Print receipt"""
        print("\n" + "=" * 50)
        print("                SALES RECEIPT")
        print("=" * 50)
        print(f"Order ID: {self.sale_id}")
        print(f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        for item in self.items:
            print(f"{item.product.name:20} ×{item.quantity:3} ¥{item.product.price:7.2f} ¥{item.subtotal:8.2f}")

        print("-" * 50)
        print(f"Subtotal: ¥{self.subtotal:10.2f}")
        print(f"Tax (10%): ¥{self.tax:8.2f}")
        print(f"Total: ¥{self.total:10.2f}")
        print(f"Payment Method: {self.payment_method}")
        print("=" * 50)
        print("          Thank you for shopping with us!")
        print("=" * 50)


class Return:
    """Return order"""

    def __init__(self, return_id: str, original_sale_id: str):
        self.return_id = return_id
        self.original_sale_id = original_sale_id
        self.datetime = datetime.now()
        self.items: List[Dict] = []
        self.refund_amount = 0.0
        self.reason = ""

    def add_item(self, product: Product, quantity: int, reason: str):
        """Add return product"""
        self.items.append({
            'product': product,
            'quantity': quantity,
            'reason': reason
        })
        self.refund_amount += product.price * quantity

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'return_id': self.return_id,
            'original_sale_id': self.original_sale_id,
            'datetime': self.datetime.isoformat(),
            'items': [
                {
                    'product_id': item['product'].product_id,
                    'product_name': item['product'].name,
                    'quantity': item['quantity'],
                    'refund': item['product'].price * item['quantity'],
                    'reason': item['reason']
                }
                for item in self.items
            ],
            'refund_amount': self.refund_amount,
            'reason': self.reason
        }
