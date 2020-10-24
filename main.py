import os
from threading import Thread
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from random import Random
from gtts import gTTS
from playsound import playsound
from datetime import datetime


class BrainBoosterLayout(BoxLayout):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.max_1st_number_size = 0
        self.max_2nd_number_size = 0
        self.actions = ['плюс', 'минус', 'умножить на', 'разделить на']
        self.max_number_1 = 0
        self.max_number_2 = 0
        self.current_result = 0
        self.start_time = None
        self.end_time = None

    def start_training(self):
        self.ids.submit_answer_button.disabled = False
        self.ids.result_input.disabled = False
        self.max_1st_number_size = int(self.ids.number_1_size_input.text)
        self.max_2nd_number_size = int(self.ids.number_2_size_input.text)
        self.max_number_1 = 1
        self.max_number_2 = 1
        iteration = 0
        while iteration < self.max_1st_number_size:
            self.max_number_1 *= 10
            iteration += 1
        iteration = 0
        while iteration < self.max_2nd_number_size:
            self.max_number_2 *= 10
            iteration += 1
        ExpressionGenerator(self).start()
        self.start_time = datetime.now()

    def submit_answer(self):
        self.end_time = datetime.now()
        time = self.end_time - self.start_time
        user_result = float(self.ids.result_input.text)
        if user_result == self.current_result:
            self.ids.info_label.text = 'Правильно. Потрачено {0} секунд'.format(time.seconds)
        else:
            self.ids.info_label.text = 'Неправильно. Потрачено {0} секунд'.format(time.seconds)
        self.ids.result_input.text = ''
        ExpressionGenerator(self).start()
        self.start_time = datetime.now()


class ExpressionGenerator(Thread):
    def __init__(self, brain_booster_layout):
        Thread.__init__(self)
        self.brain_booster_layout = brain_booster_layout

    def run(self):
        self.generate_expression()

    def generate_expression(self):
        random = Random()
        number1 = random.randint(self.brain_booster_layout.max_number_1 / 10,
                                 self.brain_booster_layout.max_number_1 - 1)
        number2 = random.randint(self.brain_booster_layout.max_number_2 / 10,
                                 self.brain_booster_layout.max_number_2 - 1)
        action = self.brain_booster_layout.actions[random.randint(0, 3)]
        if action == 'плюс':
            self.brain_booster_layout.current_result = number1 + number2
        elif action == 'минус':
            self.brain_booster_layout.current_result = number1 - number2
        elif action == 'умножить на':
            self.brain_booster_layout.current_result = number1 * number2
        elif action == 'разделить на':
            self.brain_booster_layout.current_result = round(number1 / number2, 2)
        expression = '{0} {1} {2}'.format(number1, action, number2)
        tts = gTTS(expression, lang='ru')
        tts.save('{0}.mp3'.format(expression))
        playsound('{0}.mp3'.format(expression))
        os.remove('{0}.mp3'.format(expression))


class BrainBoosterApp(App):
    def build(self):
        return BrainBoosterLayout()


if __name__ == '__main__':
    Window.clearcolor = [1, 1, 1, 1]
    BrainBoosterApp().run()
