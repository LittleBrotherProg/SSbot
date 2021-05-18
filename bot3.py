from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import mysql.connector
from mysql.connector import Error
import re

GROUP_ID = '146384697'
GROUP_TOKEN = '85a8d32f22314f81cb27945010b31f2b59b00c9dcca40c39f2a8f1a395653509eba9a1ae4bdd0ff2812cb'
API_VERSION = '5.120'
f_toggle: bool = False

vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
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


def edit_message(message, keyboard):
    post = {
        "random_id": 0,
        'peer_id': event.obj.peer_id,
        "message": message,
        "conversation_message_id": event.obj.conversation_message_id,
        "keyboard": (keyboard_1 if f_toggle else keyboard).get_keyboard()
    }

    vk_session.method("messages.edit", post)


def main_menu(buttons_name):
    keybrd = []
    for button in buttons_name:
        but = f"{button}"
        keybrd.append(but)
    return keybrd


for event in VkBotLongPoll(vk_session, group_id=GROUP_ID).listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.obj.message['text']
        user_id = event.obj.message['from_id']
        user_get = vk.users.get(user_ids=user_id)
        user_get = user_get[0]
        first_name = user_get['first_name']

        if text == 'Диагностика оборудования за 1 точку':
           keyboard_1 = VkKeyboard(one_time=False, inline=True)
           keyboard_1.add_callback_button(label='Добавить красного ',
                                           color=VkKeyboardColor.PRIMARY,
                                           payload={"type": "my_own_100500_type_edit"})
           send_message(user_id, "Сервисные услуги", keyboard_1)


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
