import tkinter as tk
from tkinter import messagebox, simpledialog

menu = {
    'Food': {
        'Burger': 35.00,
        'Pizza': 40.00,
        'Fries': 48.00,
        'Wings': 50.00,
        'Waffle': 65.00,
        'Pasta': 89.00
    },
    'Drinks': {
        'Bloody Blink': 49.00,
        'Green Lily': 49.00,
        'Banana Muggle': 39.00,
        'Fuzzy Polyjuice': 49.00
    },
    'Special Drinks': {
        'Spicy Basilisk': 69.00,
        'Manhattan Beauxbatons': 59.00,
        'Forbidden Quidditch': 59.00,
        'Goblet of Daigure': 59.00
    }
}

PENDING = 'Pending'
IN_PROGRESS = 'In Progress'
READY = 'Ready'

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []
        self.status = PENDING
        self.total = 0.0
        self.payment = 0.0

    def add_item(self, item, price):
        self.items.append((item, price))
        self.total += price

    def update_status(self, status):
        self.status = status

class SportsBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Bar Ordering System")
        self.orders = {}
        self.current_order_id = 1
        self.current_order = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.title_label = tk.Label(self.main_frame, text="Welcome to the Sports Bar!", font=('Helvetica', 16, 'bold'))
        self.title_label.pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        self.order_btn = tk.Button(self.main_frame, text="Place Order", width=30, command=self.start_order)
        self.order_btn.pack(pady=5)

        self.prepare_btn = tk.Button(self.main_frame, text="Prepare Order", width=30, command=self.prepare_order)
        self.prepare_btn.pack(pady=5)

        self.complete_btn = tk.Button(self.main_frame, text="Complete Order", width=30, command=self.complete_order)
        self.complete_btn.pack(pady=5)

        self.receipt_btn = tk.Button(self.main_frame, text="Show Receipt", width=30, command=self.show_receipt)
        self.receipt_btn.pack(pady=5)

        self.exit_btn = tk.Button(self.main_frame, text="Exit", width=30, command=self.root.quit)
        self.exit_btn.pack(pady=5)

    def start_order(self):
        self.current_order = Order(self.current_order_id)
        self.orders[self.current_order_id] = self.current_order
        self.current_order_id += 1

        self.select_items()

    def select_items(self):
        category = simpledialog.askstring("Category", "Enter Category (Food, Drinks, Special Drinks):")
        if category is None or category.title() not in menu:
            messagebox.showerror("Error", "Invalid category.")
            return

        category = category.title()
        items = list(menu[category].keys())
        item_str = "\n".join([f"{item} - ${menu[category][item]:.2f}" for item in items])
        item = simpledialog.askstring("Select Item", f"Choose from:\n{item_str}")

        if item is None or item.title() not in menu[category]:
            messagebox.showerror("Error", "Invalid item.")
            return

        item = item.title()
        price = menu[category][item]
        self.current_order.add_item(item, price)

        again = messagebox.askyesno("Add More?", "Would you like to add another item?")
        if again:
            self.select_items()
        else:
            self.show_order_summary()

    def show_order_summary(self):
        order = self.current_order
        summary = "\n".join([f"{item} - ${price:.2f}" for item, price in order.items])
        messagebox.showinfo("Order Summary", f"Order ID: {order.order_id}\nItems:\n{summary}\nTotal: ${order.total:.2f}")

    def prepare_order(self):
        order_id = simpledialog.askinteger("Prepare Order", "Enter Order ID to prepare:")
        if order_id in self.orders:
            self.orders[order_id].update_status(IN_PROGRESS)
            messagebox.showinfo("Order Update", f"Order {order_id} is now In Progress.")
        else:
            messagebox.showerror("Error", "Order ID not found.")

    def complete_order(self):
        order_id = simpledialog.askinteger("Complete Order", "Enter Order ID to complete:")
        if order_id in self.orders:
            order = self.orders[order_id]
            order.update_status(READY)
            payment = simpledialog.askfloat("Payment", f"Total: ${order.total:.2f}\nEnter payment amount:")
            if payment >= order.total:
                order.payment = payment
                change = payment - order.total
                messagebox.showinfo("Payment", f"Payment successful!\nChange: ${change:.2f}")
            else:
                messagebox.showwarning("Payment Failed", "Insufficient payment.")
        else:
            messagebox.showerror("Error", "Order ID not found.")

    def show_receipt(self):
        order_id = simpledialog.askinteger("Receipt", "Enter Order ID:")
        if order_id in self.orders:
            order = self.orders[order_id]
            items = "\n".join([f"{item} - ${price:.2f}" for item, price in order.items])
            receipt = f"Order ID: {order.order_id}\nStatus: {order.status}\nItems:\n{items}\nTotal: ${order.total:.2f}\nPayment: ${order.payment:.2f}"
            if order.payment >= order.total:
                receipt += f"\nChange: ${order.payment - order.total:.2f}"
            else:
                receipt += "\nPayment incomplete."
            messagebox.showinfo("Receipt", receipt)
        else:
            messagebox.showerror("Error", "Order ID not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsBarApp(root)
    root.mainloop()
