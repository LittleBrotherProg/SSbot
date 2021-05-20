from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import json
import mysql.connector
from mysql.connector import Error
import re
import random

GROUP_ID = '204661014'
GROUP_TOKEN = '22117b50d967969e1e3d42997ef4cebba7aec9482cbaed68cf13a6e9551de367fe3ebb9b588df4cd504e8'
API_VERSION = '5.103'


vk_session = VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)


def create_connection(user_name, user_password, db_name):

    try:
        config = {

            'user': user_name,
            'password': user_password,
            'host': '127.0.0.1',
            'port': '3306',
            'database': db_name,
            'raise_on_warnings': True, }
        print("Поцепил mySQL")
    except Error as e:
        print(f"Вот такая ошибка в функции create_connection: {e}")
    return config


connection = create_connection("root", "root", "super_servis")


def execute_read_query(connection, query):
    try:
        cnx = mysql.connector.connect(**connection)
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Вот такая ошибка {e}")


keyboard7 = []


def buttons_name(database, list):
    keyboard7.clear()
    select_users = f"SELECT * FROM `{database}` ORDER BY `{database}`.`{list}` DESC"
    users = execute_read_query(connection, select_users)
    for user_mysql in users:
        print(user_mysql)
        user_vkbot = re.sub("[(|'|,)]", "", str(user_mysql))
        keyboard7.append(user_vkbot)
        print(keyboard7)
    return keyboard7


def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0

    }
    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        posе = post

    vk_session.method("messages.send", post)



def send_message_carousel(user_id, text, keyboard=None, template=None):
    vk_session.method("messages.send", {"user_id": user_id, "message": text,
                                        "random_id": random.randint(-9223372036854775807, 9223372036854775807),
                                        "keyboard": keyboard, "template": template})


def to_create_carousel(id_photo, title, description, link, label):
    foundation = {"type": "carousel", "elements": [], }
    label_buttons = ["Заказать услугу", "Скачать прайс"]
    service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")

    for title in service_buttons_name:
        remember_buttons = {
            "buttons": [{"action": {"type": "open_link", "link": link, "label": "", "payload": "{}"}, }, ]}

        properties_carousel = {"photo_id": id_photo,
                               "title": title, "description": description,
                               "action": {"type": "open_link", "link": link}, }

        for lb in label_buttons:
            template_buttons = {
                "buttons": [{"action": {"type": "open_link", "link": link, "label": "", "payload": "{}"}, }, ]}

            if remember_buttons["buttons"][0]["action"]["label"] == "":
                remember_buttons["buttons"][0]["action"]["label"] = lb

            elif remember_buttons["buttons"][0]["action"]["label"] != "":
                template_buttons["buttons"][0]["action"]["label"] = lb
                tb = template_buttons["buttons"][0]
                remember_buttons["buttons"].append(tb)

        properties = {**properties_carousel, **remember_buttons}
        foundation["elements"].append(properties)

    return foundation


def main_menu(buttons_name):
    keybrd = []
    for button in buttons_name:
        but = f"{button}"
        keybrd.append(but)
    return keybrd


def send_message_carusel(user_id, text, keyboard=None, template=None):
    vk_session.method("messages.send", {"user_id": user_id, "message": text,
                                        "random_id": random.randint(-9223372036854775807, 9223372036854775807),
                                        "keyboard": keyboard, "template": template})


for event in VkBotLongPoll(vk_session, group_id=GROUP_ID).listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.obj.message['text']
        user_id = event.obj.message['from_id']
        user_get = vk.users.get(user_ids=user_id)
        user_get = user_get[0]
        first_name = user_get['first_name']

        if text == 'Сервис':
            carousel = to_create_carousel("-204661014_457239019", "asdasda", "asdasda", "https://vk.com/littlebr0therr",
                                          "asdasda")
            carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
            carousel = str(carousel.decode('utf-8'))
            send_message_carousel(user_id, "Карусель!", template=carousel)
        elif text == "Назад":
            g = -1
            h = 0
            main_buttons_name = buttons_name("main_buttons_name", "buttons_name")
            keyboard = VkKeyboard(one_time=True)

            for kk in main_buttons_name:
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g == h:
                    keyboard.add_line()
                    h += 1
                else:
                    g += 1

            keyboard.add_button("<Назад", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Сервисные услуги", keyboard)

        elif text != "":
            g = -1
            h = 0
            main_buttons_name = buttons_name("main_buttons_name", "buttons_name")
            keyboard = VkKeyboard(one_time=False)
            for kk in main_menu(main_buttons_name):
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g != h:
                    keyboard.add_line()
                    g += 1
            send_message(user_id, "Доброго времени суток " + first_name, keyboard)
