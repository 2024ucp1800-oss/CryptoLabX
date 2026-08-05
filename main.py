import os

from analysis.file_analysis import analyze_file
from utils.logger import log_action

DATASET_FOLDER = "datasets"


def menu():
    while True:
        print("\n========== CryptoLabX ==========")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze")
        print("5. Exit")

        choice = input("Enter choice : ").strip()

        if choice == "1":
            print("Encryption Module Coming Soon")
            log_action("Encrypt")

        elif choice == "2":
            print("Decryption Module Coming Soon")
            log_action("Decrypt")

        elif choice == "3":
            print("Attack Module Coming Soon")
            log_action("Attack")

        elif choice == "4":
            if not os.path.isdir(DATASET_FOLDER):
                print("Dataset folder not found.")
                continue

            files = [f for f in os.listdir(DATASET_FOLDER) if os.path.isfile(os.path.join(DATASET_FOLDER, f))]
            if not files:
                print("No dataset files found.")
                continue

            print("\nAvailable Files")
            for i, file in enumerate(files, start=1):
                print(i, file)

            try:
                number = int(input("\nSelect file : "))
            except ValueError:
                print("Invalid selection. Please enter a number.")
                continue

            if number < 1 or number > len(files):
                print("Invalid choice. Please select a valid file number.")
                continue

            filename = files[number - 1]
            filepath = os.path.join(DATASET_FOLDER, filename)
            analyze_file(filepath)
            log_action(f"Analyze {filename}")

        elif choice == "5":
            log_action("Exit")
            print("Thank You")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    menu()
