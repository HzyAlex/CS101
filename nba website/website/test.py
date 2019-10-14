joy_hp = 100
joy_ack = 10
joy_def = 5
joy_level = 1
joy_exp = 0

joy_exp += 100

joy_level += 1
joy_hp += 10
joy_ack += 2
joy_def += 1

joy_exp += 230


################3

class Role:

    def __init__(self):
        self.hp = 100
        self.ack = 10
        self.def_ = 5
        self.level = 1
        self.exp = 0
    
    def add_exp(self, exp):
        self.exp += exp
        while self.exp >= 100:
            self.level_up()
    
    def level_up(self):
        self.hp += 10
        self.ack += 2
        self.def_ += 1
        self.exp -= 100


joy = Role()
joy.add_exp(380)
print(joy.hp)
