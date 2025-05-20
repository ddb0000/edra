class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack_power = attack

    def attack(self, target):
        target.hp -= self.attack_power
        print(f"{self.name} attacked {target.name}, causing {self.attack_power} damage!")

def start_battle():
    hero = Character("Hero", 100, 20)
    enemy = Character("Enemy Soldier", 50, 15)

    turn = 1
    while hero.hp > 0 and enemy.hp > 0:
        print(f"\n--- Turn {turn} ---")
        hero.attack(enemy)
        if enemy.hp <= 0:
            print("Enemy defeated!")
            break
        enemy.attack(hero)
        if hero.hp <= 0:
            print("You were defeated!")
            break
        turn += 1

if __name__ == "__main__":
    start_battle()
