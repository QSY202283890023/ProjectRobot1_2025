"""
POS System - Day 1
Project initialization and basic structure
"""

def main():
    print("Welcome to Supermarket POS System")
    print("System is initializing...")
    print("Features will be added in subsequent versions")

    while True:
        print("\n=== MAIN MENU ===")
        print("1. View Products")
        print("2. Exit System")

        choice = input("Please select: ")

        if choice == "1":
            print("\nProduct list feature under development...")
        elif choice == "2":
            print("Thank you for using our system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()
