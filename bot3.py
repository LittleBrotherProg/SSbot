from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import mysql.connector
from mysql.connector import Error
import re
import random

buttons = {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/littlebr0therr",
                    "label": "От 3000 куб|1400 руб",
                    "payload": "{}"
                },

            },

bt = buttons


carousel = {
    "type": "carousel",
    "elements": [{
        "photo_id": "-146384697_457239210",
        "title": "Вентиляция приточная",
        "description": "Вентиляция приточная",
        "action": {
            "type": "open_link",
            "link": "https://vk.com/littlebr0therr"
        },
        "buttons": [
            {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/littlebr0therr",
                    "label": "До 1500 куб|800 руб",
                    "payload": "{}"
                },

            },
            {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/littlebr0therr",
                    "label": "До 3000 куб|1000 руб",
                    "payload": "{}"
                },

            },

            {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/littlebr0therr",
                    "label": "От 3000 куб|1400 руб",
                    "payload": "{}"
                },

            },
        ]
    },
    ]
}




carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
carousel = str(carousel.decode('utf-8'))

GROUP_ID = '204661014'
GROUP_TOKEN = '22117b50d967969e1e3d42997ef4cebba7aec9482cbaed68cf13a6e9551de367fe3ebb9b588df4cd504e8'
API_VERSION = '5.120'
f_toggle: bool = False

vk_session = VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)


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
        print(f"Вот такая ошибка {e}")
    return config


connection = create_connection("root", "root", "super_servis")


def execute_read_query(connection, query):
    result = None
    try:
        cnx = mysql.connector.connect(**connection)
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Вот такая ошибка {e}")


keyboard7 = []


def buttns_name(database, list):
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


# def edit_message(message, keyboard):
#     post = {
#         "random_id": 0,
#         'peer_id': event.obj.peer_id,
#         "message": message,
#         "conversation_message_id": event.obj.conversation_message_id,
#         "keyboard": (keyboard_1 if f_toggle else keyboard).get_keyboard()
#     }
#
#     vk_session.method("messages.edit", post)


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

        if text == 'Диагностика оборудования за 1 точку':

            send_message_carusel(user_id, "Карусель!", template=carousel)


        elif text == "Сервис":
            g = -1
            h = 0
            servis_buttons_name = buttns_name("servis_buttons_name", "buttons_name")
            keyboard = VkKeyboard(one_time=True)
            hg = main_menu(servis_buttons_name)
            for kk in hg:
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g == h:
                    keyboard.add_line()
                    h += 1
                else:
                    g += 1

            keyboard.add_button("<Назад", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Сервисные услуги", keyboard)

        elif text == "&lt;Назад":
            g = -1
            h = 0
            keyboard = VkKeyboard(one_time=True)
            hg = main_menu(main_buttons_name)
            for kk in hg:
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g != h:
                    keyboard.add_line()
                    g += 1

            send_message(user_id, "Главное меню", keyboard)

        elif text == "«Назад":
            g = -1
            h = 0
            keyboard = VkKeyboard(one_time=True)
            hg = main_menu(servis_buttons_name)
            for kk in hg:
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g == h:
                    keyboard.add_line()
                    h += 1
                else:
                    g += 1

            keyboard.add_button("<Назад", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Сервисные услуги", keyboard)

        elif text == "Вентиляционные системы":
            g = -2
            h = 0
            ventilation_buttons_name = buttns_name("ventilation_buttons_name", "buttons_name")
            keyboard = VkKeyboard(one_time=True)
            hg = main_menu(ventilation_buttons_name)
            for kk in hg:
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g != h:
                    keyboard.add_line()
                    g += 1

            keyboard.add_button("<<Назад", VkKeyboardColor.NEGATIVE)

            send_message(user_id, "Прайс листы:", keyboard)

        elif text != "":
            g = -1
            h = 0
            main_buttons_name = buttns_name("main_buttons_name", "buttons_name")
            keyboard = VkKeyboard(one_time=True)
            for kk in main_menu(main_buttons_name):
                keyboard.add_button(kk, VkKeyboardColor.PRIMARY)
                if g != h:
                    keyboard.add_line()
                    g += 1
            send_message(user_id, "Доброго времени суток " + first_name, keyboard)

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') == 'my_own_100500_type_edit':
            keyboard_2 = VkKeyboard(one_time=False, inline=True)
            keyboard_2.add_callback_button('Назад',
                                           color=VkKeyboardColor.NEGATIVE,
                                           payload={"type": "my_own_100500_type_edit"})
            edit_message("jnj", keyboard_2)
            f_toggle = not f_toggle
