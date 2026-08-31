# Should print Total: 30

class Till:
    def __init__(self):
        self.total = 0

    def ring_up(self, amount):
        total = self.total + amount


till = Till()
till.ring_up(10)
till.ring_up(20)

print("Total:", till.total)
