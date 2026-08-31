class Shopper:
    basket = []

    def __init__(self, name):
        self.name = name

    def add(self, item):
        self.basket.append(item)


ana = Shopper("Ana")
ben = Shopper("Ben")

ana.add("apple")

print(f"{ana.name}: {ana.basket}")
print(f"{ben.name}: {ben.basket}")
