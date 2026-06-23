import csv
from itertools import combinations
from pathlib import Path


MAX_BUDGET = 500
CSV_FILE = "Liste+d'actions+-+P7+Python+-+Feuille+1 (1).csv"


def read_actions(file_path):
    actions = []

    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            price = float(row[1])
            profit_percent = float(row[2].replace("%", ""))
            profit = price * profit_percent / 100

            actions.append(
                {
                    "name": name,
                    "price": price,
                    "profit_percent": profit_percent,
                    "profit": profit,
                }
            )

    return actions


def find_best_investment(actions):
    best_combination = []
    best_profit = 0
    best_cost = 0

    for number_of_actions in range(1, len(actions) + 1):
        for combination in combinations(actions, number_of_actions):
            total_cost = sum(action["price"] for action in combination)

            if total_cost <= MAX_BUDGET:
                total_profit = sum(action["profit"] for action in combination)

                if total_profit > best_profit:
                    best_combination = combination
                    best_profit = total_profit
                    best_cost = total_cost

    return best_combination, best_cost, best_profit


def display_result(best_combination, best_cost, best_profit):
    print("Meilleur investissement :")

    for action in best_combination:
        print(
            f"- {action['name']} : "
            f"{action['price']:.2f} euros, "
            f"{action['profit_percent']:.2f}% de benefice"
        )

    print()
    print(f"Cout total : {best_cost:.2f} euros")
    print(f"Benefice total apres 2 ans : {best_profit:.2f} euros")


def main():
    current_folder = Path(__file__).parent
    file_path = current_folder / CSV_FILE

    actions = read_actions(file_path)
    best_combination, best_cost, best_profit = find_best_investment(actions)
    display_result(best_combination, best_cost, best_profit)


if __name__ == "__main__":
    main()
