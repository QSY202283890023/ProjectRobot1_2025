import sys
from services import POSService


def clear_screen():
    """Clear the screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("            Supermarket cashier system (POS System)")
    print("=" * 50)
    print("  1. Start the cash register")
    print("  2. Handle returns")
    print("  3. View inventory")
    print("  4. Exit the system")
    print("=" * 50)


def main():
    """Main function"""
    service = POSService()

    while True:
        clear_screen()
        main_menu()

        try:
            choice = input("\nPlease select the operation (1-4): ").strip()

            if choice == '1':
                # 开始收银
                clear_screen()
                sale = service.process_sale()
                if sale:
                    input("\nPress the Enter key to return to the main menu...")

            elif choice == '2':
                # 处理退货
                clear_screen()
                return_obj = service.process_return()
                if return_obj:
                    input("\nPress the Enter key to return to the main menu...")

            elif choice == '3':
                # 查看库存
                clear_screen()
                service.show_inventory()
                input("\nPress the Enter key to return to the main menu...")

            elif choice == '4':
                # 退出系统
                print("\nThank you for using the supermarket checkout system. Goodbye!")
                sys.exit(0)

            else:
                print("Error: Invalid selection. Please re-enter")
                input("\nPress the Enter key to continue...")

        except KeyboardInterrupt:
            print("\n\nThe program was interrupted by the user")
            sys.exit(0)
        except Exception as e:
            print(f"\nError occurred {e}")
            input("\nPress the Enter key to continue...")


if __name__ == "__main__":
    main()
