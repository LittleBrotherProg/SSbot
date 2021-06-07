import json
import random
import re
import ast

import mysql.connector
from mysql.connector import Error
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

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


keyboard7 = []


def buttons_name(database, list):
    keyboard7.clear()
    select_users = f"SELECT * FROM `{database}` ORDER BY `{database}`.`{list}` DESC"
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


# def to_create_carousel(id_photo, title, description, link, label):
#     foundation = {"type": "carousel", "elements": [], }
#     label_buttons = ["Заказать услугу", "Скачать прайс"]
#     service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")
#
#     for title in service_buttons_name:
#         remember_buttons = {
#             "buttons": [{"action": {"type": "open_link", "link": link, "label": "", "payload": "{}"}, }, ]}
#
#         properties_carousel = {"photo_id": id_photo,
#                                "title": title, "description": description,
#                                "action": {"type": "open_link", "link": link}, }
#
#         for lb in label_buttons:
#             template_buttons = {
#                 "buttons": [{"action": {"type": "open_link", "link": link, "label": "", "payload": "{}"}, }, ]}
#
#             if remember_buttons["buttons"][0]["action"]["label"] == "":
#                 remember_buttons["buttons"][0]["action"]["label"] = lb
#
#             elif remember_buttons["buttons"][0]["action"]["label"] != "":
#                 template_buttons["buttons"][0]["action"]["label"] = lb
#                 tb = template_buttons["buttons"][0]
#                 remember_buttons["buttons"].append(tb)
#
#         properties = {**properties_carousel, **remember_buttons}
#         foundation["elements"].append(properties)
#     print(foundation)
#     return foundation
# def even_or_odd(a):
#     if a % 2 == 0:
#         answer = 'Четное число'
#     else:
#         answer = 'Нечентное число'
#     return answer


def to_create_carousel(id_photo, title, description, link, label):
    foundation = {"type": "carousel", "elements": [], }
    label_buttons = ["Заказать услугу", "Скачать прайс"]
    service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")

    for title in service_buttons_name:
        remember_buttons = {
            "buttons": [{"action": {"type": "text", "label": "", "payload": {'type': title}}, }, ]}

        properties_carousel = {"photo_id": id_photo,
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


def edit_message(keyboard):
    post = {
        "keyboard": keyboard
    }

    vk_session.method("messages.send", post)


def send_file(user_id, doc):
    post = {
        "user_id": user_id,
        "doc": doc,
        "random_id": 0
    }
    vk_session.method("messages.send", post)


def send_message_carusel(user_id, text, keyboard=None, template=None):
    vk_session.method("messages.send", {"user_id": user_id, "message": text,
                                        "random_id": random.randint(-9223372036854775807, 9223372036854775807),
                                        "keyboard": keyboard, "template": template})


for event in VkBotLongPoll(vk_session, group_id=GROUP_ID).listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        connection = create_connection("localhost", "root", "root", "super_servis")
        text = event.obj.message['text']

        user_id = event.obj.message['from_id']
        peer_id = event.obj.message['peer_id']
        user_get = vk.users.get(user_ids=user_id)
        user_get = user_get[0]
        first_name = user_get['first_name']

        if text == 'Сервис':
            carousel = to_create_carousel("-204661014_457239019", "asdasda", "asdasda", "https://vk.com/littlebr0therr",
                                          "asdasda")
            carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
            carousel = str(carousel.decode('utf-8'))
            send_message_carousel(user_id, "Карусель!", template=carousel)

        elif text == "Заказать услугу":
            send_message(user_id, "Для оформления заказа укажите свой номер")

        elif text == "Скачать прайс":
            doc = "doc422264572_584086035"
            print("lol")

            vk_session.method("messages.send", {"user_id": user_id, "attachment": "doc-204661014_603928275",
                                                "random_id": 0})


        elif text[0] not in ["7", "8"]:
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

        elif text[0] not in ["+", "7", "8"]:
            if len(text) == 11 or 12:
                send_message(user_id, "Введённый номер прошёл проверку")
                payload_str = (event.object.message['payload'])
                payload_dict = re.sub("[{|'|})]", "", payload_str)
                payload = ast.literal_eval('{' + payload_dict + '}')

                filling_the_database(user_id, first_name, payload['type'], text)
            else:
                send_message(user_id, "Вынеправильно ввели номер")

            # send_message_carousel(user_id, "Проверка номера пройдена")

            # service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")
            #
            # number_of_buttons = (len(service_buttons_name))
            #
            # button_counter = 0
            #
            # keyboard = VkKeyboard(one_time=False, inline=True)
            #
            # for name in service_buttons_name:
            #
            #     button_counter += 1
            #     counter = even_or_odd(button_counter)
            #
            #     if button_counter == 1:
            #         keyboard.add_callback_button(label=name, color=VkKeyboardColor.PRIMARY)
            #
            #     elif counter == "Четное число":
            #         keyboard.add_callback_button(label=name, color=VkKeyboardColor.PRIMARY,
            #                                      payload={"type": "Заявка на вентиляционные системы"})
            #
            #     elif counter == "Нечентное число":
            #
            #         keyboard.add_line()
            #         keyboard.add_callback_button(label=name, color=VkKeyboardColor.PRIMARY,
            #                                      payload={"type": "Заявка на вентиляционные системы"})
            #
            # send_message(user_id, "Сервисные услуги", keyboard)

        # elif text == "Вентиляционные системы":
        #
        #     label_buttons = ["Заказать услугу", "Скачать прайс"]
        #     number_of_buttons = (len(label_buttons))
        #
        #     button_counter = 0
        #
        #     keyboard = VkKeyboard(one_time=False, inline=True)
        #
        #     for name in label_buttons:
        #         print(button_counter)
        #         button_counter += 1
        #         counter = even_or_odd(button_counter)
        #         print(counter)
        #
        #         print(name)
        #         if button_counter == 1:
        #             keyboard.add_button(name, VkKeyboardColor.POSITIVE)
        #             print("first")
        #         elif counter == "Четное число":
        #             keyboard.add_button(name, VkKeyboardColor.NEGATIVE)
        #             print("add")
        #         elif counter == "Нечентное число":
        #             print("skip + add")
        #             keyboard.add_line()
        #             keyboard.add_button(name, VkKeyboardColor.NEGATIVE)
        #
        #     send_message(user_id, "Вентиляционные системы", keyboard)

    # elif event.type == VkBotEventType.MESSAGE_EVENT:
    #     service_buttons_name = buttons_name("servis_buttons_name", "buttons_name")
    #     for name in service_buttons_name:
    #         if event.object.payload.get('type') == name:
    #             print(event.object)
    #             send_message(user_id, "Для оформления заказа укажите свой номер")
    #             filling_the_database(user_id, first_name, name)
    #
    #             print(name)
    #
    #             print(user_id)
    #
    #             print("work")
