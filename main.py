"""
POS System - Day 2
Complete sale processing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services import POSService

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("\n" + "="*50)
    print("          SUPERMARKET POS SYSTEM")
    print("="*50)
    print("  1. Process Sale")
    print("  2. View Inventory")
    print("  3. Exit System")
    print("="*50)

def main():
    service = POSService()
    
    while True:
        clear_screen()
        main_menu()
        
        try:
            choice = input("\nSelect operation (1-3): ").strip()
            
            if choice == '1':
                clear_screen()
                sale = service.process_sale()
                if sale:
                    input("\nPress Enter to return to main menu...")
            
            elif choice == '2':
                clear_screen()
                service.show_inventory()
                input("\nPress Enter to return to main menu...")
            
            elif choice == '3':
                print("\nThank you for using POS System. Goodbye!")
                sys.exit(0)
            
            else:
                print("Error: Invalid selection, please try again")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\nError occurred: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
