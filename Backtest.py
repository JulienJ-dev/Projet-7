import csv
from pathlib import Path


MAX_BUDGET = 50000
CSV_FILE = r"data\dataset1_Python+P7.csv"


def read_actions(file_path):
    actions = []
    price_anomalies = []
    duplicated_name_anomalies = {}
    name_seen = {}
    lines_count = 1

    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            price = float(row[1])
            price_in_cents = round(price * 100)
            profit_percent = float(row[2].replace("%", ""))
            lines_count += 1

            if price_in_cents <= 0 or profit_percent <= 0 or name in name_seen:
                if price_in_cents <= 0:
                    price_anomalies.append(name)
                    continue
                
                if profit_percent <= 0:
                    continue
                
                if name in name_seen:
                    if name in duplicated_name_anomalies:
                        duplicated_name_anomalies[name].append(lines_count)
                    else:
                        duplicated_name_anomalies[name] = [name_seen[name], lines_count]
                    continue

            name_seen[name] = lines_count
            actions.append(
                {
                    "name": name,
                    "price": price,
                    "price_in_cents": price_in_cents,
                    "profit_percent": profit_percent,
                    "profit": price * profit_percent / 100,
                }
            )

    return actions, price_anomalies, duplicated_name_anomalies


def find_best_investment(actions):
    best_profits = [0] * (MAX_BUDGET + 1)
    best_combinations = [()] * (MAX_BUDGET + 1)

    for action in actions:
        action_price = action["price_in_cents"]

        for budget in range(MAX_BUDGET, action_price -1, -1):
            remaining_budget = budget - action_price
            new_profit = best_profits[remaining_budget] + action["profit"]

            if new_profit > best_profits[budget]:
                best_profits[budget] = new_profit
                best_combinations[budget] = (best_combinations[remaining_budget] + (action,))

    best_budget = max(range(MAX_BUDGET + 1), key=lambda budget: best_profits[budget],)
    best_combination = best_combinations[best_budget]
    best_cost = sum(action["price_in_cents"] for action in best_combination) / 100
    best_profit = best_profits[best_budget]

    return best_combination, best_cost, best_profit

def display_anomalies(price_anomalies, duplicated_name_anomalies):
    if price_anomalies:
        print()
        print("Actions ignorés car prix semblant erroné ( prix <= 0 ) :")

        for anomaly in price_anomalies:
            print(anomaly)
    
    if duplicated_name_anomalies:
        print()
        print("Des doublons ont été trouvés pour les actions suivantes :")

        for name, lines in duplicated_name_anomalies.items():
            formatted_lines = ", ".join(str(line) for line in lines)
            print(f"{name} - Lignes {formatted_lines}")



def display_result(best_combination, best_cost, best_profit):
    print()
    print("Meilleur investissement :")

    for action in best_combination:
        print(f"- {action['name']} : {action['price']:.2f} euros, {action['profit_percent']:.2f}% de benefice")

    print()
    print(f"Cout total : {best_cost:.2f} euros")
    print(f"Benefice total apres 2 ans : {best_profit:.2f} euros")


def main():
    current_folder = Path(__file__).parent
    file_path = current_folder / CSV_FILE

    actions, price_anomalies, duplicated_name_anomalies = read_actions(file_path)
    best_combination, best_cost, best_profit = find_best_investment(actions)
    display_anomalies(price_anomalies, duplicated_name_anomalies)
    display_result(best_combination, best_cost, best_profit)


if __name__ == "__main__":
    main()
