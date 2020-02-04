import math
import random
import Public


class Animal:
    def __init__(self, _pos_x: int, _pos_y: int, _size: int, _pic: int):
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.size = _size
        self.pic = _pic
        self.grab = 0

        self.delta_x = 0
        self.delta_y = 0

        while self.delta_x == 0 and self.delta_y == 0:
            self.delta_x = random.randint(-Public.game_speed, Public.game_speed)
            self.delta_y = random.randint(-Public.game_speed, Public.game_speed)

    def calc_new_pos(self):
        self.pos_x += self.delta_x
        self.pos_y += self.delta_y

    def is_click_contain(self, _touch_x: int, _touch_y: int) -> bool:
        return (self.pos_x + self.size >= self.pos_x <= _touch_x) and (self.pos_y <= _touch_y <= self.pos_y + self.size)


class Animals:
    def __init__(self):
        self.animal_list = []

    def get_all_animals(self) -> [Animal]:
        return self.animal_list
