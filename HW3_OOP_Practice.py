# There is a Person whose characteristics are:
# 1. Name
# 2. Age
# 3. Availability of money
# 4. Having your own home
#
# Human can:
# 1. Provide information about yourself
# 2. Make money
# 3. Buy a house
#
# There is also a House, the properties of which include:
# 1. Area
# 2. Cost
#
# For Home you can:
# 1. Apply a purchase discount
#
# e.g.: There is also a Small Typical House with a required area of 40m2.
#
# *Realtor:
# 1. Name
# 2. Houses
# 3. Discount that he/she can give you.
#
# *There is only one realtor who handles small houses you wanna buy. (Singleton)
# Realtor is only one in your city and can:
# 1. Provide information about all the Houses
# 2. Give a discount
# 3. Steal your money with 10% chance
from abc import ABC, abstractmethod
import random


class Human(ABC):
    @abstractmethod
    def info(self):
        raise NotImplementedError

    @abstractmethod
    def make_money(self):
        raise NotImplementedError

    @abstractmethod
    def buy_a_house(self, house, realtor):
        pass


class Person(Human):
    def __init__(self, name, age, money, home: list):
        self.name = name
        self.age = age
        self.money = money
        self.home = home

    def info(self):
        print(f"My name is {self.name}. I'm {self.age} years old.\n"
              f"I have ${self.money} in my wallet.")
        if len(self.home) >= 1:
            print(f"{self.name}: I have such realty: {self.home}.")
        else:
            print(f"{self.name}: I have no realty.")

    def make_money(self):
        print(f"{self.name}: I earned some money. \n"
              f"Now I have ${self.money} in my wallet.")
        self.money += random.randrange(200, 500, 100)

    def buy_a_house(self, house, realtor):
        if realtor.steal_money is True:
            self.money = 0
            print("Shit! The realtor stole my money!")
            return
        if house in realtor.houses:
            if self.money >= house.cost:
                print(f"{self.name}: I buy the house {house.address} with area {house.area} sq.m. which costs"
                      f" ${house.cost}.")
                self.money -= house.cost
                print(f"{self.name}: Now I have ${self.money}.")
                self.home.append(house.address)
                realtor.sold_house(house)
            else:
                while self.money < house.cost:
                    print(f"Can't buy this house {house.address}. I must earn more money or choose another one.")
                    print("What should we do?\n")
                    action = input("Please input '1' for earning money or '2' for choosing another one': ")
                    if action == "1":
                        self.make_money()
                    elif action == "2":
                        return
                    else:
                        print("Incorrect action! Try again!")
        else:
            return "There is no houses available"


class Home(ABC):
    @abstractmethod
    def apply_a_purchase_discount(self, discount):
        raise NotImplementedError


class House(Home):
    def __init__(self, address, area, cost):
        self.address = address
        self.area = area
        self.cost = cost

    def apply_a_purchase_discount(self, discount):
        if discount > 0:
            print(f"You're lucky! A discount for house {self.address} is {discount}!"
                  f"Now it costs {self.cost - round(self.cost * discount)}")
            self.cost -= round(self.cost * discount)
        else:
            print(f"Sorry, but there is no discount for house {self.address}.")


class SmallTypicalHouse(House):
    def __init__(self, address, cost, area=40):
        super().__init__(address, area, cost)


class RealtorMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Realtor(metaclass=RealtorMeta):

    def __init__(self, name, houses: list, discount):
        self.name = name
        self.houses = houses
        self.discount = discount

    def provide_info_about_houses(self):
        if self.houses is not []:
            print(f"My name is {self.name} and I'm a realtor.\n"
                  f"{self.name}: There are such houses:")
            for house in self.houses:
                print(f"- {house.address} with {house.area} sq.m. which costs ${house.cost}")
            # self.houses = iter(self.houses)

        else:
            print("There is no houses on sale!")

    def give_a_discount(self, house):
        house.apply_a_purchase_discount(self.discount)

    def steal_money(self):
        i = random.randrange(1, 10)
        if i == 1:
            print(f"The realtor {self.name} steal your money!")
            return True

    def sold_house(self, house):
        self.houses.remove(house)


house1 = House("158 Shevchenko str", 200, 37000)
house2 = House("258 Franko str", 150, 45210)
house3 = House("359 Khmelnytskyi str", 100, 30500)
house4 = SmallTypicalHouse("65 Vahylevych str", 3750)
andriy = Person("Andriy", 30, 35000, [])
andriy.info()
realtorr = Realtor("Olesya", houses=[house1, house2, house3, house4], discount=round(random.uniform(0.05, 0.15), 2))
realtorr.steal_money()
realtorr.provide_info_about_houses()
realtorr.give_a_discount(house1)
andriy.buy_a_house(house1, realtorr)
andriy.info()
lesya = Person("Lesya", 34, 30000, ["457 Zelena str"])
lesya.info()
realtorr.provide_info_about_houses()
realtorr.steal_money()
realtorr.give_a_discount(house2)
lesya.buy_a_house(house2, realtorr)
lesya.info()
petro = Person("Petro", 28, 10000, [])
petro.buy_a_house(house4, realtorr)
petro.info()
