import csv
from pathlib import Path


MAX_BUDGET = 30
CSV_FILE = "data/Liste+d'actions+-+P7+Python+-+Feuille+1 (1).csv"


def read_actions(file_path):
    actions = []

    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            price = int(float(row[1]))
            profit_percent = float(row[2].replace("%", ""))

            if price <= 0 or profit_percent <= 0:
                continue

            actions.append(
                {
                    "name": name,
                    "price": price,
                    "profit_percent": profit_percent,
                    "profit": price * profit_percent / 100,
                }
            )

    return actions


def find_best_investment(actions):
    best_profits = [0] * (MAX_BUDGET + 1)
    best_combinations = [()] * (MAX_BUDGET + 1)

    for action in actions:
        action_price = action["price"]

        for budget in range(MAX_BUDGET, action_price -1, -1):
            remaining_budget = budget - action_price
            new_profit = best_profits[remaining_budget] + action["profit"]

            if new_profit > best_profits[budget]:
                best_profits[budget] = new_profit
                best_combinations[budget] = (best_combinations[remaining_budget] + (action,))
            #print(best_profits)

    best_budget = max(range(MAX_BUDGET + 1), key=lambda budget: best_profits[budget],)
    best_combination = best_combinations[best_budget]
    best_cost = sum(action["price"] for action in best_combination)
    best_profit = best_profits[best_budget]

    return best_combination, best_cost, best_profit


def display_result(best_combination, best_cost, best_profit):
    print("Meilleur investissement :")

    for action in best_combination:
        print(f"- {action['name']} : {action['price']} euros, {action['profit_percent']:.2f}% de benefice")

    print()
    print(f"Cout total : {best_cost} euros")
    print(f"Benefice total apres 2 ans : {best_profit:.2f} euros")


def main():
    current_folder = Path(__file__).parent
    file_path = current_folder / CSV_FILE

    actions = read_actions(file_path)
    best_combination, best_cost, best_profit = find_best_investment(actions)
    display_result(best_combination, best_cost, best_profit)


if __name__ == "__main__":
    main()
