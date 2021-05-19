# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import random
import json
import mysql.connector
from mysql.connector import Error
import re


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
        user_vkbot = re.sub("[(|,)]", "", str(user_mysql))
        keyboard7.append(user_vkbot)
        print(keyboard7)
    return keyboard7


main_buttons_name = buttns_name("main_buttons_name", "buttons_name")

print(main_buttons_name)

joj = ["До 1500 куб|800 руб", "До 3000 куб|1000 руб", "От 3000 куб|1400 руб"]
def car(id_photo, title, description, link, label):

    lp = {"type": "carousel", "elements": [], }
    gnt = None

    g = 0

    for kt in main_buttons_name:

        hg = {"buttons": [{"action": {"type": "open_link", "link": link, "label": "", "payload": "{}"}, }, ]}
        mom = hg["buttons"][0]["action"]

        rp = {"photo_id": id_photo,
              "title": kt, "description": description,
              "action": {"type": "open_link", "link": link}, }
        for tk in joj:

            print(mom)
            if hg["buttons"][0]["action"]["label"] == "":
                hg["buttons"][0]["action"]["label"] = tk
                print(hg)
                print(1)
            elif hg["buttons"][0]["action"]["label"] != "":
                print(mom)
                hg["buttons"][0]["action"]["label"] = tk


                hy = hg["buttons"][0]
                hg["buttons"].append(hy)
                print(hg)
                print(2)



        gnt = gnt + lp

        pup = {**rp, **hg}
        lp["elements"].append(pup)
        print(hg)
        print(pup)
        print(lp)
        g += 1
        print(g)
    print(lp)



    return lp


kok = car("-204661014_457239019", "asdasda", "asdasda", "https://vk.com/littlebr0therr", "asdasda")

#
kok = json.dumps(kok, ensure_ascii=False).encode('utf-8')
kok = str(kok.decode('utf-8'))

GROUP_ID = '204661014'
GROUP_TOKEN = '22117b50d967969e1e3d42997ef4cebba7aec9482cbaed68cf13a6e9551de367fe3ebb9b588df4cd504e8'
API_VERSION = '5.103'

vk = vk_api.VkApi(token=GROUP_TOKEN)

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, GROUP_ID)


def send_message_carusel(user_id, text, keyboard=None, template=None):
    vk.method("messages.send", {"user_id": user_id, "message": text,
                                "random_id": random.randint(-9223372036854775807, 9223372036854775807),
                                "keyboard": keyboard, "template": template})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        info = event.object.client_info["carousel"]
        print(info)

        text = event.object.message["text"]
        user_id = event.obj.message['from_id']
        print(text)
        if text == "":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_openlink_button("URL кнопка", "Кнопка")

        elif event.object.message["text"] == "3":
            send_message_carusel(user_id, "Карусель!", template=kok)
