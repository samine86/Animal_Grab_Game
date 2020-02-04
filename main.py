from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.screenmanager import WipeTransition, SwapTransition
from kivy.uix.button import Button
from kivy.uix.label import Label, CoreLabel
from kivy.uix.slider import Slider
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

import random
import GameItems
import Public

root = ScreenManager()


class SettingWindow(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'SettingWindow'

        self.add_widget(Label(text='Easy', font_size=50, pos_hint={'x': .1, 'y': .5}, size_hint=(.1, .1)))
        self.add_widget(Label(text='Hard', font_size=50, pos_hint={'x': .8, 'y': .5}, size_hint=(.1, .1)))

        self.Picker = Slider(pos_hint={'x': .25, 'y': .49}, size_hint=(.5, .1), min=1, max=100, value=25)
        self.Picker.bind(value=self.get_picker_value)
        self.add_widget(self.Picker)

        self.add_widget(
            Button(text='Start Game', pos_hint={'x': .02, 'y': .02}, size_hint=(.95, .1), on_press=self.start_game))

    def get_picker_value(self, instance, value):

        if 1 <= value < 25:
            Public.animal_size = 80
            Public.game_speed = 1
            Public.game_time = 150
        elif 25 <= value < 50:
            Public.animal_size = 65
            Public.game_speed = 3
            Public.game_time = 120
        elif 50 <= value < 75:
            Public.animal_size = 45
            Public.game_speed = 6
            Public.game_time = 90
        elif 75 <= value < 100:
            Public.animal_size = 30
            Public.game_speed = 9
            Public.game_time = 60

    def start_game(self, *args):
        root.transition = WipeTransition()
        root.add_widget(GameWindow())
        root.current = 'GameWindow'


class GameWindow(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'GameWindow'
        self.AnimalContainer = GameItems.Animals()
        self.AnimalCount = 7

        self.draw_event = Clock.schedule_interval(self.game_draw, 0.001)
        self.gametime_event = Clock.schedule_interval(self.game_time, 1)

        self.ScoreLabel = CoreLabel(font_size=40)
        self.TimeLabel = CoreLabel(font_size=40)

    def game_time(self, dt):
        Public.game_time -= 1

    def game_draw(self, dt):

        if Public.game_time == 0:
            self.game_end()

        self.canvas.clear()
        self.canvas.add(Rectangle(source='pics\\background.jpg', pos=(0, 0), size=(Window.width, Window.height)))

        self.ScoreLabel.text = 'Score : ' + str(Public.score)
        self.TimeLabel.text = 'Remain ' + str(Public.game_time) + ' Sec'

        self.ScoreLabel.refresh()
        self.TimeLabel.refresh()

        self.canvas.add(Rectangle(pos=(35, 35), size=self.ScoreLabel.texture.size, texture=self.ScoreLabel.texture))
        self.canvas.add(
            Rectangle(pos=(Window.width // 2, 35), size=self.TimeLabel.texture.size, texture=self.TimeLabel.texture))

        # Remove Outsider Animals from screen Loop

        for animal_temp in self.AnimalContainer.get_all_animals():
            if (animal_temp.pos_x <= 0 or
                    animal_temp.pos_x + animal_temp.size >= Window.width or
                    animal_temp.pos_y <= 0 or
                    animal_temp.pos_y + animal_temp.size >= Window.height):

                if animal_temp.grab == 0:
                    Public.score -= 5
                self.AnimalContainer.animal_list.remove(animal_temp)

        # Add New Animals To Container Loop

        while len(self.AnimalContainer.get_all_animals()) < self.AnimalCount:
            animal_pos_x = random.randint(Window.width // 2 - 150, Window.width // 2 + 150)
            animal_pos_y = random.randint(Window.height // 2 - 150, Window.height // 2 + 150)
            animal_pic = random.randint(10, 48)

            self.AnimalContainer.animal_list.append(GameItems.Animal(animal_pos_x,
                                                                     animal_pos_y,
                                                                     Public.animal_size,
                                                                     animal_pic))

        # Draw Animals Loop

        for animal_temp in self.AnimalContainer.get_all_animals():

            if animal_temp.grab == 0:
                self.canvas.add(Rectangle(source='pics\{}.png'.format(animal_temp.pic),
                                          pos=(animal_temp.pos_x, animal_temp.pos_y),
                                          size=(animal_temp.size, animal_temp.size)))
            elif animal_temp.grab == 1:
                self.canvas.add(Rectangle(source='pics\spark.png',
                                          pos=(animal_temp.pos_x, animal_temp.pos_y),
                                          size=(animal_temp.size, animal_temp.size)))
            animal_temp.calc_new_pos()

    def game_end(self):
        Clock.unschedule(self.draw_event)
        root.add_widget(ResultWindow())
        root.current = 'ResultWindow'

    def on_touch_down(self, touch):
        for animal_temp in self.AnimalContainer.get_all_animals():
            if animal_temp.is_click_contain(touch.pos[0], touch.pos[1]):
                animal_temp.grab = 1
                Public.score += 10


class ResultWindow(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'ResultWindow'
        self.add_widget(
            Label(text='Your Score : {}'.format(Public.score), pos_hint={'x': .35, 'y': .5}, size_hint=(.3, .1),
                  font_size=40))
        self.add_widget(
            Button(text='Restart Game', pos_hint={'x': .02, 'y': .02}, size_hint=(.5, .1), on_press=self.game_restart))
        self.add_widget(
            Button(text='Exit Game', pos_hint={'x': .55, 'y': .02}, size_hint=(.45, .1), on_press=self.game_exit))
    def game_restart(self, *args):
       root.current = 'GameWindow'

    def game_exit(self, *args):
        exit()

class AnimalGrabApp(App):
    def build(self):
        root.add_widget(SettingWindow())
        return root


AnimalGrabApp().run()
