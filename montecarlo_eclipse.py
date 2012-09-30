import random

class Ship:
    def __init__(self, computer, shield, hull, cannons={}):
        self.computer = computer
        self.shield = shield
        self.hull_init = hull
        self.cannons = cannons
        for cannon_type in map(lambda x: 2**x, range(3)):
            if cannon_type not in cannons.keys():
                cannons[cannon_type] = 0
        
        self.reset()

    def reset(self):
        self.hull = self.hull_init

    def attack_modifier(self, defender):
        modifier = self.computer + defender.shield
        if modifier < 0:
            modifier = 0
        return modifier

class GameState:
    def __init__(self, faction1, faction2):
        self.faction1 = faction1
        self.faction2 = faction2
        self.reset()

    def reset(self):
        self.faction1.reset()
        self.faction2.reset()

    def do_attack(self, a, b):
        modifier = a.attack_modifier(b)
        damage = 0
        for cannon_type in map(lambda x: 2**x, range(3)):
            for cannon in range(a.cannons[cannon_type]):
                throw = random.randrange(6) + 1
                if throw + modifier >= 6 and throw!=1:
                    damage += cannon_type
        b.hull -= damage

    def run(self):
        while True:
            # faction1 -> faction2
            dmg = self.do_attack(self.faction1, self.faction2)
            if self.faction2.hull < 0:
                return "faction1"

            # faction2 -> faction1
            dmg = self.do_attack(self.faction2, self.faction1)
            if self.faction1.hull < 0:
                return "faction2"

def main():
    s = GameState(Ship(2, -1, 0, cannons={2:2}), 
                  Ship(2, -1, 0, cannons={4:1}))

    no_runs = 50000
    print("Simulating %u runs" % no_runs)
    wins = {"faction1" : 0, "faction2": 0}
    for i in range(no_runs):
        s.reset()
        winner = s.run()
        wins[winner] += 1
    print("Faction 1 wins with a chance of %.2f %%" % (100 * wins["faction1"]/no_runs))

if __name__=="__main__":
    main()
