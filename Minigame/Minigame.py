def make_prompt(question: str):
    prompt = input(question).lower()
    while prompt != "y" and prompt != "n":
        prompt = input(question).lower()
    return True if prompt == "y" else False

def make_list_prompt(question: str, array: int):
    while True:
        try:
            choosed_variant = int(input(question))
            while choosed_variant not in range(1, array + 1):
                choosed_variant = int(input(question))
            break
        except:
            pass
    return choosed_variant

class Item:
    def __init__(self, name: str, lore: str):
        self.type = "ITEM"
        self.name = name
        self.lore = lore
        
    def print_info(self):
        print("____ITEM____")
        print("Name:", self.name)
        print("Lore:", self.lore)
        
    def use(self):
        self.print_info()

class Weapon:
    def __init__(self, name: str, dmg: int, crit_chance: int, crit_damage: int):
        self.type = "WEAPON"
        self.name = name
        self.dmg = dmg
        self.crit_damage = dmg + (dmg * crit_damage * 0.01)
        self.crit_chance = crit_chance
        
    def print_info(self):
        print("____WEAPON____")
        print("Name:", self.name)
        print("Damage:", self.dmg)
        print("Critical chance:", self.crit_chance)
        print("Critical damage:", self.crit_damage)
        
class Consumable:
    def __init__(self, name: str, need_for: str, power: int):
        self.type = "CONSUMABLE"
        self.name = name
        self.need_for = need_for
        self.power = power
        
    def use(self, entity):
        if self.need_for == "H":
            print(f">>> [{entity.name}] использовал аптечку")
            entity.health += self.power
        if self.need_for == "A":
            print(f">>> [{entity.name}] восстановил броню")
            entity.armor += self.power
        
class Player:
    def __init__(self, name: str, health: int, armor: int, weapon: Weapon):
        self.type = "ENTITY"
        self.name = name
        self.health = health
        self.armor = armor
        self.weapon = weapon
        self.inventory = []
        
    def print_info(self):
        print("____PLAYER____")
        print("Name:", self.name)
        print("HP/AR:", self.health, "/", self.armor)
        print("Weapon:", self.weapon.name)
            
    def pickup(self, entity):
        if entity.type == "ITEM" or "CONSUMABLE":
            print(f">>> [{self.name}] подобрал [{entity.name}]")
            self.inventory.append(entity)
        if entity.type == "WEAPON":
            entity.print_info()
            do_pickup = self.make_prompt(f"Вы уверены что хотите взять [{entity.name}] вместо своего оружия? (y/n)")
            if do_pickup:
                print(f">>> [{self.name}] сменил свое оружие на [{entity.name}]")
                
    def open_inventory(self):
        while True:
            print("Инвентарь", self.name)
            print("1. Использовать предмет")
            print("2. Удалить предмет") 
            print("3. Выйти из инвентаря")
            menu = make_list_prompt("Выберите действие: ", 3)
            if menu == 1:
                print("Ваш инвентарь: ")
                i = 1
                for item in self.inventory:
                    print(f"{i}. {item.name}")
                    i += 1
                print(f"{i}. Назад")
                item = make_list_prompt("Выберите предмет: ", i)
                if item == i:
                    self.open_inventory()
                    return
                self.inventory[item - 1].use()
                if self.inventory[item - 1].type == "CONSUMABLE":
                    self.inventory.pop(item - 1)  
            if menu == 2:
                print("Выбрали Удалить")
            if menu == 3:
                break
        
        
    def do_fight(self, entity):
        if entity.type == "ENTITY":
            pass

fists = Weapon("Fists", 10, 10, 55)

player = Player("Vasya", 100, 100, fists)

for i in range(10):
    test_item = Item(f"Item{i}", f"LoreItem{i}")
    player.pickup(test_item)

player.open_inventory()