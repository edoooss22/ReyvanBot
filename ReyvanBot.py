import sqlite3
import datetime
import telebot
import os
from time import time

#Настройки
bot = telebot.TeleBot("")
cfg = True #Поменяй на True, чтобы включить фичи с использованием конфига, для этого надо, чтобы скрипт мог создавать и хранить файлы на машине (устройство на котором запущен)


#Подключение бд
db = sqlite3.connect('reyvan.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS admins(
    chat TEXT,
    id INT,
    lvl INT,
    date TEXT
)""")
db.commit()


#Подгрузка кфг
if cfg == True:
    bug = "DEBUG: недостающие кфг файлы созданы:"
    if not os.path.exists("config.txt"):
        file = open("config.txt", "w")
        file.close()
        bug = bug + " config.txt"
    if not os.path.exists("ban_list.txt"):
        file = open("ban_list.txt", "w")
        file.close()
        bug = bug + " ban_list.txt"
    if bug != "DEBUG: недостающие кфг файлы созданы:":
        print(bug)
    print("DEBUG: кфг подключен")

#Вгрузка конфига
urls = list()
file = open("config.txt", "r")
pp = file.read()
file.close()
if pp != "":
    pp = pp.split("\n")
    for p in pp:
        if p != "":
            urls.append(f"{p}")
print("DEBUG: config загружен. Бот успешно запущен!")



#Мут
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен мут"))
def mute(message):
    try:
        klvl = check_adm(message)
        if klvl < 1:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 1-лвла админки. Твой лвл {klvl}!")
            return

        kklvl = check_adm(message.reply_to_message, False)
        if klvl <= kklvl:
            bot.reply_to(message,
                         "Вы не можете взаимодействовать с админами, лвл которых выше вашего или равен вашему!")
            return

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
        klvl = check_adm(message)
        if klvl < 1:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 1-лвла админки. Твой лвл {klvl}!")
            return

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
        klvl = check_adm(message)
        if klvl < 2:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 2-лвла админки. Твой лвл {klvl}!")
            return

        kklvl = check_adm(message.reply_to_message, False)
        if klvl <= kklvl:
            bot.reply_to(message,
                         "Вы не можете взаимодействовать с админами, лвл которых выше вашего или равен вашему!")
            return

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
        klvl = check_adm(message)

        if klvl < 3:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 3-лвла админки. Твой лвл {klvl}!")
            return

        kklvl = check_adm(message.reply_to_message, False)
        if klvl <= kklvl:
            bot.reply_to(message, "Вы не можете взаимодействовать с админами, лвл которых выше вашего или равен вашему!")
            return

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
            file = open("ban_list.txt", "a")
            file.write(f"{message.chat.id}%{uid}")
            file.close()
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
        file = open("ban_list.txt", "a")
        file.write(f"{message.chat.id}%{user}")
        file.close()
    except Exception as e:
        print("DEBUG: " + str(e))
        return

#Разбан
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен разбан"))
def unban(message):
    try:
        klvl = check_adm(message)
        if klvl < 3:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 3-лвла админки. Твой лвл {klvl}!")
            return
        if message.text.lower() != "рейвен разбан":
            uid = message.text.lower()[message.text.rfind(" ") + 1:]

            um_msg = f"Пользователь с id {uid} разблокирован в чате, если он был заблокирован!"

            bot.unban_chat_member(message.chat.id, uid, only_if_banned=True)
            bot.reply_to(message, um_msg, parse_mode="html")
            file = open("ban_list.txt", "r")
            hh = file.read()
            hhh = hh
            file.close()
            hh = hh.split("\n")
            for h in hh:
                if f"{message.chat.id}%{uid}" in h:
                    hhh = hhh.replace(h, "")
                    file = open("ban_list.txt", "w")
                    file.write(hhh)
                    file.close()
            return

        user = message.reply_to_message.from_user.id

        nick = str(message.reply_to_message.from_user.first_name) + str(message.reply_to_message.from_user.last_name)
        if str(message.reply_to_message.from_user.last_name) == "None":
            nick = str(message.reply_to_message.from_user.first_name)

        um_msg = f"Пользователь <a href='tg://user?id={user}'>{nick}</a> разблокирован в чате, если он был заблокирован!"

        file = open("ban_list.txt", "r")
        hh = file.read()
        hhh = hh
        file.close()
        hh = hh.split("\n")
        for h in hh:
            if f"{message.chat.id}%{user}" in h:
                hhh = hhh.replace(h, "")
                file = open("ban_list.txt", "w")
                file.write(hhh)
                file.close()
        bot.unban_chat_member(message.chat.id, user, only_if_banned=True)
        bot.reply_to(message, um_msg, parse_mode="html")
    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Удаление
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен удали"))
def delete(message):
    try:
        klvl = check_adm(message)
        kklvl = check_adm(message.reply_to_message, False)

        if klvl < 1:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 1-лвла админки. Твой лвл {klvl}!")
            return

        if klvl <= kklvl:
            bot.reply_to(message, "Вы не можете взаимодействовать с админами, лвл которых выше вашего или равен вашему!")
            return

        m = message
        if m.text.lower() == "рейвен удали":
            bot.delete_message(message.chat.id, message.reply_to_message.id)
            return
        if m.text.lower() == "рейвен удали чат":
            if klvl < 3:
                bot.reply_to(message, f"Команда доступна с 3-лвла админки. Твой лвл {klvl}!")
                return
            id = message.id
            for i in range(1, id):
                try:
                    bot.delete_message(message.chat.id, id-i)
                except:
                    continue
            bot.send_message(message.chat.id, "Чат успешно удалён!")
            return
    except:
        return


#Инфо
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен инфо"))
def getid(message):
    try:
        klvl = check_adm(message)
        if klvl < 1:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 1-лвла админки. Твой лвл {klvl}!")
            return
        bot.reply_to(message, f"id: {message.reply_to_message.from_user.id}\nchat id: {message.chat.id}\nmessage id: {message.id}")
    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Ссылки
@bot.message_handler(func=lambda message: message.entities is not None and str(message.chat.id).startswith("-"))
def detect_links(message):
    try:
        if str(message.chat.id) not in urls:
            return
        userinf = bot.get_chat_member(message.chat.id, message.from_user.id)

        #if str(userinf.status) == "creator" or str(userinf.status) == "administrator":
        #    return

        user = userinf.user
        nick = str(user.first_name) + str(user.last_name)
        if str(user.last_name) == "None":
            nick = str(user.first_name)

        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                bot.delete_message(message.chat.id, message.id)
                bot.send_message(message.chat.id,
                                 f"Я удалила сообщение, содержащие ссылку, пользователя <a href='tg://user?id={user.id}'>{nick}</a>!", parse_mode="html")
        return
    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Рейвен админ
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен админ"))
def adm_11(message):
    try:
        user = bot.get_chat_member(message.chat.id, message.from_user.id)

        if message.from_user.id == 1242173932 or message.from_user.id == 1071400424:
            bd_updater(message)
            return

        if str(user.status) != "creator":
            bot.reply_to(message, "Назначать администраторов может только создатель чата!")
            return

        bd_updater(message)
    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Вкл/Выкл url-удаление
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен url"))
def url_turn(message):
    try:
        m = message

        user = bot.get_chat_member(message.chat.id, message.from_user.id)
        if str(user.status) != "creator":
            bot.reply_to(message, "Ты не создатель чата!")
            return

        file = open("config.txt", "r")
        hh = file.read()
        file.close()
        if m.text.lower()[11:] == "вкл":
            if str(message.chat.id) in hh.split("\n"):
                bot.reply_to(message, "Ошибка! Авто-удаление URL(Ссылок) уже включено в этом чате!")
                return
            file = open("config.txt", "a")
            file.write(f"{message.chat.id}\n")
            file.close()
            bot.reply_to(message, "Авто-удаление URL(Ссылок) включено в чате!")
            urls.append(f"{message.chat.id}")
            return

        if m.text.lower()[11:] == "выкл":
            if str(message.chat.id) not in hh.split("\n"):
                bot.reply_to(message, "Ошибка! Авто-удаление URL(Ссылок) уже выключено в этом чате!")
                return
            hh = hh.replace(f"{message.chat.id}\n", "")
            file = open("config.txt", "w")
            file.write(hh)
            file.close()
            bot.reply_to(message, "Авто-удаление URL(Ссылок) выключено в чате!")
            urls.remove(f"{message.chat.id}")
            return



    except Exception as e:
        print("DEBUG: " + str(e))
        bot.reply_to(message, "Ошибка! Правильное использование:\n\nрейвен url вкл\nрейвен url выкл")
        return

#Бан-лист
@bot.message_handler(func=lambda m: m.text.lower().startswith("рейвен бан-лист") or m.text.lower().startswith("рейвен банлист"))
def bal_list(message):
    try:
        klvl = check_adm(message)
        if klvl < 1:
            if klvl == 0:
                return
            bot.reply_to(message, f"Команда доступна с 1-лвла админки. Твой лвл {klvl}!")
            return

        file = open("ban_list.txt", "r")
        hh = file.read()
        file.close()
        hh = hh.split("\n")
        bans = ""
        for h in hh:
            if f"{message.chat.id}%" in h:
                bans = bans + h.split("%")[1] + "\n"
        bot.reply_to(message, f"Бан-лист чата:\n{bans}")
        return
    except Exception as e:
        print("DEBUG: " + str(e))
        bot.reply_to(message, "Ошибка! Правильное использование:\n\nрейвен url вкл\nрейвен url выкл")
        return
#Назначение админки
def bd_updater(message):
    try:
        chat_id = str(message.chat.id)
        db = sqlite3.connect('reyvan.db')
        sql = db.cursor()

        try:
            id = int(message.reply_to_message.from_user.id)
        except:
            bot.reply_to(message, "Ошибка! Писать команду надо ответом на сообщение пользователя, которого хотите назначить админом!")
            return

        date = datetime.datetime.now()
        date = str(date.strftime('%d.%m.%Y %H:%M'))

        try:
            casta = int(message.text.lower()[13:])
            if casta > 3 or casta <= 0:
                bot.reply_to(message, "Ошибка! Максимальный лвл админки равен 3!")
                return
        except:
            bot.reply_to(message, "Ошибка! Скорее всего вы не указали ранг админки!\n\nрейвен админ 1\nрейвен админ 2\nрейвен админ 3")
            return

        sql.execute(f"""SELECT id FROM admins WHERE id = {id} AND chat = {chat_id}""")
        if sql.fetchone() is None:
            sql.execute("""INSERT INTO admins VALUES (?, ?, ?, ?)""", (chat_id, id, casta, date))
            db.commit()

            user = message.reply_to_message.from_user.id

            nick = str(message.reply_to_message.from_user.first_name) + str(
                message.reply_to_message.from_user.last_name)
            if str(message.reply_to_message.from_user.last_name) == "None":
                nick = str(message.reply_to_message.from_user.first_name)

            bot.reply_to(message, f"Пользователь <a href='tg://user?id={id}'>{nick}</a> назначен администратором {casta}-лвла в этом чате({chat_id})", parse_mode="html")
            return
        else:
            bot.reply_to(message, f"Этот пользователь уже назначен администратором в этом чате!")
            return

    except Exception as e:
        print("DEBUG: " + str(e))
        return


#Чек админки
def check_adm(message, kk=True):
    try:
        message = message
        chat_id = str(message.chat.id)
        id = message.from_user.id

        db = sqlite3.connect('reyvan.db')
        sqll = db.cursor()

        sqll.execute(f"""SELECT lvl FROM admins WHERE chat = {chat_id} AND id = {id}""")
        pizda = sqll.fetchone()
        if pizda is None:
            if kk:
                bot.reply_to(message, "Ты не назначен админом в этом чате!")
            xyu2 = 0
            return xyu2
        else:
            return int(pizda[0])
    except Exception as e:
        print("DEBUG: " + str(e))
        return



bot.polling()
