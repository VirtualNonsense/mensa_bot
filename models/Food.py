from datetime import datetime


class Food:
    def __init__(self):
        self.name = ""
        self.caption = ""
        self.priceStudent = 0.0
        self.priceStaff = 0.0
        self.priceVisitor = 0.0
        self.foodIcon = None

    def __str__(self):
        return "{} {}: {:4.2f}€(Stud.) {:4.2f}€(Bed.) {:4.2f}€(Gäste)".format(self.name, self.foodIcon,
                                                                              self.priceStudent, self.priceStaff,
                                                                              self.priceVisitor)


class Menu:
    def __init__(self, date: datetime, food: list):
        self.date = date
        self.food = food
