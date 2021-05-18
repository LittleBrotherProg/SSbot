# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import random
import json
from vk_api import VkApi


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

GROUP_ID = '146384697'
GROUP_TOKEN = '85a8d32f22314f81cb27945010b31f2b59b00c9dcca40c39f2a8f1a395653509eba9a1ae4bdd0ff2812cb'
API_VERSION = '5.103'

# vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
# vk = vk_session.get_api()
# longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

vk_session = VkApi(token=GROUP_TOKEN)
vk = vk_api.VkApi(token=GROUP_TOKEN)

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, GROUP_ID)


def send_message(user_id, text, keyboard=None, template=None):
    vk_session.method("messages.send", {"user_id": user_id, "message": text,
                                "random_id": random.randint(-9223372036854775807, 9223372036854775807),
                                "keyboard": keyboard, "template": template})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        info = event.object.client_info["carousel"]
        print(info)

        text = event.object.message["text"]
        user_id = event.obj.message['from_id']
        print(text)
        if text == "1":
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_openlink_button("URL кнопка", "Кнопка")

        elif event.object.message["text"] == "3":
            send_message(user_id, "Карусель!", template=carousel)

