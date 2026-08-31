def calculate_total(prices):
    total = 0
    for price in prices:
        total += price
    print(total)


prices = [10, 20, 30]
grand_total = calculate_total(prices)
print(f"Grand total with tax: {grand_total * 1.08:.2f}")
