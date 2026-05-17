import os

def run_edge():
    print("\n[1] Running Edge Simulator...")
    os.system("python edge_simulator.py")


def run_encrypt():
    print("\n[2] Running Encryption Module...")
    os.system("python encrypt_module.py")


def run_server():
    print("\n[3] Running Server Module...")
    os.system("python server_module.py")


def run_log_verify():
    print("\n[4] Verifying Logs...")
    os.system("python verify_logs.py")


def run_ai():
    print("\n[5] Running AI Analysis...")
    os.system("python ai_module.py")


def run_full_system():
    print("\n🚀 Running Full Secure Edge System...\n")
    run_edge()
    run_encrypt()
    run_server()
    run_log_verify()
    run_ai()
    print("\n✅ Full system execution completed.\n")


def menu():
    while True:
        print("\n===== SECURE EDGE DATA TRANSMISSION SYSTEM =====")
        print("1. Generate Edge Data")
        print("2. Encrypt Data")
        print("3. Send to Server & Verify")
        print("4. Verify Logs")
        print("5. Run AI Analysis")
        print("6. Run Full System")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            run_edge()
        elif choice == '2':
            run_encrypt()
        elif choice == '3':
            run_server()
        elif choice == '4':
            run_log_verify()
        elif choice == '5':
            run_ai()
        elif choice == '6':
            run_full_system()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    menu()