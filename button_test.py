from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import json

GROUP_ID = '146384697'
GROUP_TOKEN = '85a8d32f22314f81cb27945010b31f2b59b00c9dcca40c39f2a8f1a395653509eba9a1ae4bdd0ff2812cb'
API_VERSION = '5.120'

f_toggle: bool = False

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
longpollbot = VkBotLongPoll(vk_session, group_id=GROUP_ID)
longpol = VkLongPoll(vk_session)


def send_message(user_id, message, keyboard_1):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "keyboard": keyboard_1.get_keyboard(),
        "peer_id": user_id

    }

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


for event in VkBotLongPoll(vk_session, group_id=GROUP_ID).listen():

    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.obj.message['text']
        user_id = event.obj.message['from_id']
        user_get = vk.users.get(user_ids=user_id)
        user_get = user_get[0]
        first_name = user_get['first_name']

        if text == 'Диагностика оборудования (за 1 точку)':
            keyboard_1 = VkKeyboard(one_time=False, inline=True)
            keyboard_1.add_callback_button(label='Добавить красного ',
                                           color=VkKeyboardColor.PRIMARY,
                                           payload={"type": "my_own_100500_type_edit"})
            send_message(user_id, "Сервисные услуги", keyboard_1)

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') == 'my_own_100500_type_edit':
            keyboard_2 = VkKeyboard(one_time=False, inline=True)
            keyboard_2.add_callback_button('Назад',
                                       color=VkKeyboardColor.NEGATIVE,
                                       payload={"type": "my_own_100500_type_edit"})
            edit_message("jnj", keyboard_2)
            f_toggle = not f_toggle
