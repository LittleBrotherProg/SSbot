import json
import random
import re
import ast

import mysql.connector
from mysql.connector import Error
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


GROUP_ID = '204661014'
GROUP_TOKEN = '22117b50d967969e1e3d42997ef4cebba7aec9482cbaed68cf13a6e9551de367fe3ebb9b588df4cd504e8'
API_VERSION = '5.103'

vk_session = VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def buttons_name(database, list):
    keyboard7 = []
    select_users = f"SELECT {list} FROM `{database}`"
    users = execute_read_query(connection, select_users)
    for user_mysql in users:
        user_vkbot = re.sub("[(|'|,)]", "", str(user_mysql))
        keyboard7.append(user_vkbot)

    return keyboard7


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def filling_the_database(ID, first_name, name, phone):
    print(f"Поступила заявка на {name} от {first_name} из ВК. id заказчика {ID} и его номер телфона{phone}")
    sql = f"""INSERT INTO 
    `applications`(`id`, `first_name_vk`, `servis_name`, `social_network`, `number_phone`) 
    VALUES 
    ( {ID}, '{first_name}', '{name}', 'ВК', '{phone}')"""
    execute_query(connection, sql)


def to_create_carousel(link):
    foundation = {"type": "carousel", "elements": [], }
    label_buttons = ["Заказать услугу", "Скачать прайс"]
    service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")
    description = buttons_name("servis_buttons_name", "description")
    photo_id = buttons_name("servis_buttons_name", "photo_id")

    for title, description, photo_id in zip(service_buttons_name, description, photo_id):
        remember_buttons = {
            "buttons": [{"action": {"type": "text", "label": "", "payload": {'type': title}}, }, ]}

        properties_carousel = {"photo_id": photo_id,
                               "title": title, "description": description,
                               "action": {"type": "open_link", "link": link}, }

        for lb in label_buttons:
            template_buttons = {
                "buttons": [{"action": {"type": "text", "label": "", "payload": {'type': title}}, }, ]}

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


def send_message_carousel(user_id, text, template):
    post = {
        "user_id": user_id,
        "message": text,
        "random_id": 0,
        "template": template

    }
    vk_session.method("messages.send", post)


def send_file(user_id, doc):
    post = {
        "user_id": user_id,
        "doc": doc,
        "random_id": 0
    }
    vk_session.method("messages.send", post)


for event in VkBotLongPoll(vk_session, group_id=GROUP_ID).listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        text = event.obj.message['text']

        user_id = event.obj.message['from_id']
        peer_id = event.obj.message['peer_id']
        user_get = vk.users.get(user_ids=user_id)
        user_get = user_get[0]
        first_name = user_get['first_name']

        if text == 'Сервис':
            connection = create_connection("localhost", "root", "root", "super_servis")
            carousel = to_create_carousel("https://megazip33.ru/services/")
            carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
            carousel = str(carousel.decode('utf-8'))
            send_message_carousel(user_id, """Наша компания занимается не только продажей запчастей,
                                           но и ремонтом бытовой техники!\nОзнакомьтесь с полным списком наших услуг по ремонту и установке техники""",
                                  template=carousel)

        elif text == "Заказать услугу":
            payload_str = (event.object.message['payload'])
            send_message(user_id, "Для оформления заказа укажите свой номер. Номер должен начинаться с +7 или 8")

        elif text == "Скачать прайс":
            doc = "doc422264572_584086035"
            print("lol")

            vk_session.method("messages.send", {"user_id": user_id, "attachment": "doc-204661014_603928275",
                                                "random_id": 0})
        elif text[0] in ["1", "2", "3", "4", "5", "6", "7", "9"]:
            send_message(user_id, "Неправильно введён номер")

        elif text[0] in ["+", "7", "8"]:
            connection = create_connection("localhost", "root", "root", "super_servis")
            if len(text) == 11 or 12:
                send_message(user_id, "Спасибо, ваша заявка принята")
                payload_dict = re.sub("[{|'|})]", "", payload_str)
                payload = ast.literal_eval('{' + payload_dict + '}')
                filling_the_database(user_id, first_name, payload['type'], text)
            else:
                send_message(user_id, "Неправильно введён номер")


        elif text == "Начать":
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("Сервис", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Связь с менеджером", VkKeyboardColor.PRIMARY)
            send_message(user_id, "Доброго времени суток," + first_name, keyboard)
