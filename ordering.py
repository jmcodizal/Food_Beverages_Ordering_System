
# Menu items available in the bar
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
        'Bloody Blink' : 49.00,
        'Green Lily': 49.00,
        'Banana Muggle': 39.00, 
        'Fuzzy Polyjuice': 49.00
    },
    'Special Drinks': {
        'Spicy Basilisk' : 69.00,
        'Manhattan Beauxbatons' : 59.00,
        'Forbidden Quidditch' : 59.00,
        'Goblet of Daigure' : 59.00
    }
}

room = {
    'Single Room': {
        'Regular Single Room': 499.00,
        'Single Room with Aircon': 699.00,
        'Single Room with  ': 1999.00
    },
    'Double Room': {
        'Regular Double Room': 599.00,
        'Double Room with Aircon': 799.00,
        'Double Room with  ': 899.00
    },
    'Suite': {
        'Queen Suite' : 3999.00,
        'King Suite' : 4999.00,
        'Junior Suite' : 2999.00,
    }

}

# Order status constants
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

    def add_item(self, item, category):
        
        category = category.title()  
        
        print(f"Category selected: {category}")

        if category in menu:
            item = item.lower().title()  
            
            
            print(f"Item selected: {item}")

           
            if item in menu[category]:
                price = menu[category][item]
                self.items.append((item, price))
                self.total += price
                print(f"Added {item} to your order. Price: ${price:.2f}")
            else:   
                print(f"Sorry, {item} is not available in the {category} menu.")
        else:
            print(f"Invalid category: {category}. Please choose 'Food', 'Drinks', or 'Special Drinks'.")


    def display_order(self):
        print("\nYour Order Summary:")
        for item, price in self.items:
            print(f"- {item}: ${price:.2f}")
        print(f"Total: ${self.total:.2f}")
        print(f"Status: {self.status}")

    def update_status(self, status):
        self.status = status
        print(f"Order {self.order_id} status updated to {self.status}.")

class SportsBar:
    def __init__(self):
        self.orders = {}
        self.current_order_id = 1
        
    def display_menu(self):
        print("\n\t\t\t\t\t Welcome to the Sports Bar! \t\t\t\t\t\t")
        print("Here is the menu:")
        for category, items in menu.items():
            print(f"\n{category}:")
            for item, price in items.items():
                print(f"  - {item}: ${price:.2f}")

    def create_order(self):
        order = Order(self.current_order_id)
        self.orders[self.current_order_id] = order
        self.current_order_id += 1
        return order

    def take_order(self):
        self.display_menu()
        order = self.create_order()

        while True:
            category = input("\nSelect category (Food/Drinks/Special Drinks) or type 'done' to finish: ")
            if category == 'Done' or category == 'done':
                break
            if category not in ['Food', 'Drinks', 'Special Drinks']:
                print("Invalid category. Please choose 'Food' , 'Drinks' or 'Special Drinks'.")
                continue

            item = input(f"Enter the name of the {category} item: ")
            order.add_item(item, category)

        order.display_order()
        return order

    def prepare_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"\nPreparing Order {order_id}...")
            order.update_status(IN_PROGRESS)
        else:
            print("Order not found.")

    def complete_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"\nCompleting Order {order_id}...")
            order.update_status(READY)
            self.process_payment(order)
        else:
            print("Order not found.")

    def receipt_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"\n=== Receipt for Order {order_id} ===")
            for item, price in order.items:
                print(f"- {item}: ${price:.2f}")
            print(f"Total: ${order.total:.2f}")
            print(f"Payment: ${order.payment:.2f}")
            if order.payment >= order.total:
                change = order.payment - order.total
                print(f"Change: ${change:.2f}")
            else:
                print("Payment is incomplete.")
            print(f"Status: {order.status}")
        else:
            print("Order not found.")


    def process_payment(self, order):
        print(f"\nYour total is: ${order.total:.2f}")
        payment = float(input("Enter payment amount: $"))
        if payment >= order.total:
            order.payment = payment
            change = payment - order.total
            print(f"Payment successful! Your change is: ${change:.2f}")
        else:
            print("Insufficient payment. Please try again.")


def main():
    print("\n\t\t\t\t\t Welcome to the JMC Sports Bar System! \t\t\t\t\t\t")
    sports_bar_system()

def sports_bar_system():
    sports_bar = SportsBar()

    while True:
        print("\n                         ----------------------------------------------------------------------      ")
        print("\n\t\t\t\t\t === Sports Bar Ordering System ===\t\t\t\t\t\t")
        print("\t\t\t\t\t  1. Place Order \t\t\t\t\t\t")
        print("\t\t\t\t\t  2. Prepare Order \t\t\t\t\t\t")
        print("\t\t\t\t\t  3. Complete Order \t\t\t\t\t\t")
        print("\t\t\t\t\t  4. Order Receipt \t\t\t\t\t\t")
        print("\t\t\t\t\t  5. Exit \t\t\t\t\t\t")
        print("                         ----------------------------------------------------------------------      ")

        choice = input("Enter your choice: ")

        if choice == '1':
            order = sports_bar.take_order()
        elif choice == '2':
            order_id = int(input("Enter Order ID to prepare: "))
            sports_bar.prepare_order(order_id)
        elif choice == '3':
            order_id = int(input("Enter Order ID to complete: "))
            sports_bar.complete_order(order_id)
        elif choice == '4':
            order_id = int(input("Enter Order ID to get the receipt: "))
            sports_bar.receipt_order(order_id)
        elif choice == '5':
            print("Thank you for visiting! Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()