import configparser
import pygame
import PySimpleGUI as sg
import io
from PIL import Image
import base64
import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser
import pyglet
import time
import os
import testaudio


class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''
        po = 0

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час'): self.time,
            ('привет', 'добрый день'): self.hello,
            ('пока', 'вырубись'): self.quite,
            ('выключи компьютер', 'выруби компьютер'): self.shut,
            ('включи режим разработчика', 'включить режим разработчика'): self.azb,
        }

        self.ndels = ['Нана', 'нана', 'на-на', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на', 'включи', 'вруби', 'туториал')):
            self.opener(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()

    def time(self):
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):
        links = {
            ('youtube', 'ютуб крутой', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инста', 'инсту'): 'https://www.instagram.com/',
            ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
            ('холлоу ', 'hollow'): 'https://hollowknight.ru/hallownest',
            ('салли ', 'sally'): 'https://www.youtube.com/watch?v=udrhqeAUzKI',
            ('террария ', 'terraria'): 'https://terraria.fandom.com/wiki/Terraria_Wiki',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            testaudio.open()
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break
                            self.quite

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
            file.close()

    def quite(self):
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        testaudio.goodbye()
        time.sleep(3)
        system('cls')
        sys.exit(0)

    def shut(self):
        self.talk("Подтвердите действие!")
        testaudio.access()
        time.sleep(3)
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            testaudio.shutdown()
            time.sleep(3)
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            testaudio.cancel()
            time.sleep(3)
            self.talk("Действие не подтверждено")
        else:
            testaudio.cancel()
            time.sleep(3)
            self.talk("Действие не подтверждено")

    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую кусок мяса']))
        testaudio.hello()
        time.sleep(3)

    def weather(self):

        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']  # Переменная для записи страны/кода страны
        country_and_place = place + ", " + country  # Запись города и страны в одну переменную через запятую
        owm = OWM('8f4586c589faf736fb54774ef96e476b')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город

        w = observation.weather

        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        self.talk("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
                  "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
                  "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
                  "\nСкорость ветра " + str(
            w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print(colorama.Fore.LIGHTGREEN_EX + "Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text

    def youtube(self):
        webbrowser.open('https://www.youtube.com/?feature=ytca', new=0)

    def vk(self):
        webbrowser.open('https:vk.com/feed', new=0)

    def insta(self):
        webbrowser.open('https://www.instagram.com/', new=0)

    def google(self):
        webbrowser.open('https://google.com/', new=0)

    def gmail(self):
        webbrowser.open('http://gmail.com/', new=0)

    def sleep(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def azb(self):
        self.talk("режим разработчика активирован")
        po = 1