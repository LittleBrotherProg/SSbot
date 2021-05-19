# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import random
import json
import re
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

    }
    ]
}
hg = {
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/littlebr0therr",
                    "label": "До 1500 куб|800 руб",
                    "payload": "{}"
                },
}
rp = ['с', 'п', 'и', 'с', 'о', 'к']

lp = {"type": "carousel", }




def car(id_photo, title, description, action):
    g = 3
    h = 0
    while g != h:
        lp["elements"] = [{"photo_id": id_photo,"title": title,"description": description,"action": action,"buttons": [hg]}]
        h += 1

    return lp




kok = car("asdasd", "asdasda", "asdasda", "asdasda")

kok = car("asdasd", "asdasda", "asdasda", "asdasda")

kok = car("asdasd", "asdasda", "asdasda", "asdasda")
print(lp)
lp["elements"][0]["buttons"].append(hg)

print(lp)

# print(carousel)
# bt = {"buttons": [{
#                 "action": {
#                     "type": "open_link",
#                     "link": "https://vk.com/littlebr0therr",
#                     "label": "До 1500 куб|800 руб",
#                     "payload": "{}"
#                 },
# }]
#
#             },
#
#
#

# ln = (",".join("Python"))
#
# bt = dict()
# print(bt)
# carousel.update([bt])
# # carousel['elements:[{buttons'].append(bt)
# print(carousel)
# # act = [{
# #                 "action": {
# #                     "type": "open_link",
# #                     "link": "https://vk.com/littlebr0therr",
# #                     "label": "До 1500 куб|800 руб",
# #                     "payload": "{}"
# #                 },
# #
# #             },]
#
#
# # bt["buttons"].append(act)
# # re.sub("[(|)]", "", bt)
#
kok = json.dumps(kok, ensure_ascii=False).encode('utf-8')
kok = str(kok.decode('utf-8'))

GROUP_ID = '146384697'
GROUP_TOKEN = '85a8d32f22314f81cb27945010b31f2b59b00c9dcca40c39f2a8f1a395653509eba9a1ae4bdd0ff2812cb'
API_VERSION = '5.103'

vk = vk_api.VkApi(token=GROUP_TOKEN)

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, GROUP_ID)


def send_message_carusel(user_id, text, keyboard=None, template=None):
    vk.method("messages.send", {"user_id": user_id, "message": text,"random_id": random.randint(-9223372036854775807, 9223372036854775807),"keyboard": keyboard, "template": template})


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
            send_message_carusel(user_id, "Карусель!", template=kok)
