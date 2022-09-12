import telebot
import os
from time import time

#Настройки
bot = telebot.TeleBot("5363709877:AAErBCZfay87iui54BdyjR-faaLriVOTeAQ")
cfg = False #Поменяй на True, чтобы включить фичи с использованием конфига, для этого надо, чтобы скрипт мог создавать и хранить файлы на машине (устройство на котором запущен)

#Подгрузка кфг
if cfg:
    bug = "DEBUG: недостающие кфг файлы созданы:"
    if os.path.exists("config.txt"):
        file = open("config.txt", "w")
        file.close()
        bug = bug + " config.txt"
    if os.path.exists("ban_list.txt"):
        file = open("ban_list.txt", "w")
        file.close()
        bug = bug + " ban_list.txt"
    if os.path.exists("mute_list.txt"):
        file = open("mute_list.txt", "w")
        file.close()
        bug = bug + " mute_list.txt"
    if bug != "DEBUG: недостающие кфг файлы созданы:":
        print(bug)
    print("DEBUG: кфг подключен")

#Мут
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен мут"))
def mute(message):
    try:

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        checker = message.text.lower()
        error_msg = "Ошибка! Время мута указано неверно!\n\nПравильное оформление:\nРейвен мут 60 сек\nРейвен мут 5 мин\nРейвен мут 10 час"
        mute_time = 60
        m_msg_d = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> получил мут на "
        m_msg_s = False
        m_msg_h = False
        m_msg_m = False
        prichina = "не указана"

        userinf = bot.get_chat_member(message.chat.id, user)
        if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
            bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его нельзя ограничить.")
            return

        if checker == "рейвен мут":
            bot.restrict_chat_member(message.chat.id, user, until_date=mute_time)
            bot.reply_to(message, m_msg_d + "60 секунд!", parse_mode="html")
            return


        if " сек" in checker or " с" in checker:
            try:
                mute_time = int(message.text.lower()[11:message.text.lower().find(" с")])
                if mute_time < 60:
                    bot.reply_to(message, "Ошибка! Минимальное время мута 60 сек (1 минута)!")
                    return
                print(mute_time)
                m_msg_s = True
            except:
                bot.reply_to(message, error_msg)
                return

        elif (" м" in checker and checker[:checker.find(" м")] != "рейвен") or " мин" in checker:
            try:
                mute_time = int(message.text.lower()[11:message.text.lower().rfind(" м")]) * 60
                print(mute_time, mute_time / 60)
                m_msg_m = True
            except:
                bot.reply_to(message, error_msg)
                return

        elif " ч" in checker or " час" in checker:
            try:
                mute_time = int(message.text.lower()[11:message.text.lower().find(" ч")]) * 3600
                print(mute_time)
                m_msg_h = True
            except:
                bot.reply_to(message, error_msg)
                return
        print(1)
        m_msg = ""
        if m_msg_s:
            m_msg = f"{mute_time} секунд!"
        elif m_msg_m:
            m_msg = f"{mute_time / 60} минут!"
        elif m_msg_h:
            m_msg = f"{mute_time / 3600} часов!"

        if "\n" in checker:
            prichina = checker[checker.find("\n") + 1:]
            print(prichina)

        bot.restrict_chat_member(message.chat.id, user, until_date=time() + mute_time)
        bot.reply_to(message, m_msg_d + m_msg + f"\n\nПричина: {prichina}", parse_mode="html")

    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Размут
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен размут"))
def unmute(message):
    try:
        if message.text.lower() != "рейвен размут":
            uid = message.text.lower()[message.text.rfind(" ") + 1:]
            userinf = bot.get_chat_member(message.chat.id, uid)

            if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
                bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его права нельзя редактировать.")
                return

            userinf = userinf.user
            nick = str(userinf.first_name) + str(userinf.last_name)


            if str(userinf.last_name) == "None":
                nick = str(userinf.first_name)

            um_msg = f"Пользователь <a href='tg://user?id={uid}'>{nick}</a> размучен!"

            bot.restrict_chat_member(message.chat.id, uid, can_send_messages=True,
                                     can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True,
                                     can_add_web_page_previews=True, can_invite_users=True)
            bot.reply_to(message, um_msg, parse_mode="html")
            return

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        um_msg = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> размучен!"

        checker = message.text.lower()

        userinf = bot.get_chat_member(message.chat.id, user)
        if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
            bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его права нельзя редактировать.")
            return


        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True, can_invite_users=True)
        bot.reply_to(message, um_msg, parse_mode="html")
    except Exception as e:
        print("DEBUG: " + str(e))
        return

#Кик
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен кик"))
def kick(message):
    try:
        if message.text.lower() != "рейвен кик":
            uid = message.text.lower()[message.text.rfind(" ") + 1:]
            userinf = bot.get_chat_member(message.chat.id, uid)

            if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
                bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его нельзя кикнуть.")
                return

            userinf = userinf.user
            nick = str(userinf.first_name) + str(userinf.last_name)

            if str(userinf.last_name) == "None":
                nick = str(userinf.first_name)

            um_msg = f"Пользователь <a href='tg://user?id={uid}'>{nick}</a> кикнут с чата, но он может перезайти!"

            bot.kick_chat_member(message.chat.id, uid)
            bot.unban_chat_member(message.chat.id, uid)
            bot.reply_to(message, um_msg, parse_mode="html")
            return

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        um_msg = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> кикнут с чата, но он может перезайти!"

        userinf = bot.get_chat_member(message.chat.id, user)
        if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
            bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его нельзя кикнуть.")
            return

        bot.kick_chat_member(message.chat.id, user)
        bot.unban_chat_member(message.chat.id, user)
        bot.reply_to(message, um_msg, parse_mode="html")
    except Exception as e:
        print("DEBUG: " + str(e))
        return

#Бан
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен бан"))
def ban(message):
    try:
        if message.text.lower() != "рейвен бан":
            uid = message.text.lower()[message.text.rfind(" ") + 1:]
            userinf = bot.get_chat_member(message.chat.id, uid)

            if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
                bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его нельзя заблокировать.")
                return

            userinf = userinf.user
            nick = str(userinf.first_name) + str(userinf.last_name)

            if str(userinf.last_name) == "None":
                nick = str(userinf.first_name)

            um_msg = f"Пользователь <a href='tg://user?id={uid}'>{nick}</a> заблокирован в чате (навсегда)!"

            bot.kick_chat_member(message.chat.id, uid)
            bot.reply_to(message, um_msg, parse_mode="html")
            return

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        um_msg = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> заблокирован в чате (навсегда)!"

        userinf = bot.get_chat_member(message.chat.id, user)
        if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
            bot.reply_to(message, "Ошибка! Этот пользователь админ/создатель чата, его нельзя заблокировать.")
            return

        bot.kick_chat_member(message.chat.id, user)
        bot.reply_to(message, um_msg, parse_mode="html")
    except Exception as e:
        print("DEBUG: " + str(e))
        return

#Разбан
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен разбан"))
def unban(message):
    try:
        if message.text.lower() != "рейвен разбан":
            uid = message.text.lower()[message.text.rfind(" ") + 1:]

            um_msg = f"Пользователь с id {uid} разблокирован в чате, если он был заблокирован!"

            bot.unban_chat_member(message.chat.id, uid, only_if_banned=True)
            bot.reply_to(message, um_msg, parse_mode="html")
            return

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        um_msg = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> разблокирован в чате, если он был заблокирован!"

        bot.unban_chat_member(message.chat.id, user, only_if_banned=True)
        bot.reply_to(message, um_msg, parse_mode="html")
    except Exception as e:
        print("DEBUG: " + str(e))
        return

#Удаление
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен удали"))
def delete(message):
    try:
        id = message.id
        for i in range(1, id):
            try:
                bot.delete_message(message.chat.id, id-i)
            except:
                continue
    except:
        return

#Инфо
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен инфо"))
def getid(message):
    try:
        bot.reply_to(message, f"id: {message.reply_to_message.from_user.id}\nchat id: {message.chat.id}\nmessage id: {message.id}")
    except Exception as e:
        print("DEBUG: " + str(e))
        return
bot.polling()
