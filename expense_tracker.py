"""
Expense Tracker
---------------
Saves expenses in expenses.csv and loads them again on the next start.
Run with:  python expense_tracker.py
"""

import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


def load_expenses():
    """Read expenses.csv and return a list of dictionaries."""
    expenses = []
    try:
        with open(FILE_NAME, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expense = {
                        "date": row["date"],
                        "item": row["item"],
                        "category": row["category"],
                        "amount": float(row["amount"]),
                    }
                    expenses.append(expense)
                except (ValueError, KeyError, TypeError):
                    print("Skipped a damaged row in", FILE_NAME)
        print("Loaded", len(expenses), "expense(s) from", FILE_NAME + ".")
    except FileNotFoundError:
        # First run: the file does not exist yet, so start with an empty list
        print(FILE_NAME, "not found. Starting with an empty list.")
    return expenses


def save_expenses(expenses):
    """Write the header and all expenses to expenses.csv."""
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "item", "category", "amount"])
            for expense in expenses:
                writer.writerow([expense["date"], expense["item"],
                                 expense["category"], f"{expense['amount']:.2f}"])
        return True
    except PermissionError:
        print("Could not save. Close", FILE_NAME, "if it is open in another program.")
        return False


def ask_text(prompt):
    """Ask until the user types something that is not empty."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("This cannot be empty. Please try again.")


def ask_date():
    """Ask until the date is valid. Pressing Enter uses today's date."""
    while True:
        text = input("Date YYYY-MM-DD (Enter = today): ").strip()
        if text == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-11-14.")


def ask_amount():
    """Ask until the amount is a valid number greater than 0."""
    while True:
        text = input("Amount: ").strip()
        try:
            amount = round(float(text), 2)
        except ValueError:
            print("Invalid amount. Please enter a number, for example 12.50.")
            continue
        # nan fails this test, and inf fails the upper limit
        if amount > 0 and amount < 1000000000:
            return amount
        print("Amount must be a normal number greater than 0.")


def unique_categories(expenses):
    """Use a set to keep every category only once."""
    return set(expense["category"] for expense in expenses)


def add_expense(expenses):
    """Ask for one expense, add it to the list and save the file."""
    print("\n--- Add Expense ---")
    date = ask_date()
    item = ask_text("Item: ")
    category = ask_text("Category: ").title()
    amount = ask_amount()

    expenses.append({"date": date, "item": item,
                     "category": category, "amount": amount})
    if save_expenses(expenses):
        print("Expense added and saved.")


def show_all(expenses):
    """Print every expense and the unique categories."""
    print("\n--- All Expenses ---")
    if len(expenses) == 0:
        print("No expenses yet.")
        return

    print(f"{'Date':<12}{'Item':<20}{'Category':<16}{'Amount':>10}")
    print("-" * 58)
    for expense in expenses:
        print(f"{expense['date']:<12}{expense['item']:<20}"
              f"{expense['category']:<16}{expense['amount']:>10.2f}")
    print("\nUnique categories:", ", ".join(sorted(unique_categories(expenses))))


def total_by_category(expenses):
    """Print the unique categories and the total of each category."""
    print("\n--- Total by Category ---")
    if len(expenses) == 0:
        print("No expenses yet.")
        return

    categories = unique_categories(expenses)
    print("Unique categories:", ", ".join(sorted(categories)))
    print()

    all_total = 0
    for category in sorted(categories):
        total = 0
        for expense in expenses:
            if expense["category"] == category:
                total = total + expense["amount"]
        print(f"  {category:<16}{total:>10.2f}")
        all_total = all_total + total
    print(f"  {'ALL':<16}{all_total:>10.2f}")


def main():
    expenses = load_expenses()
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. Show all")
        print("3. Total by category")
        print("4. Quit")
        choice = input("Choose 1-4: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_all(expenses)
        elif choice == "3":
            total_by_category(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")
