import telebot, os, json

bot = telebot.TeleBot('8025066988:AAE0psFm6krRRqkDp7RUPwHomtGxXUIGrS0')

Acceptance_of_applications = False
onEditForm = False
applications = {}
admin = {}
with open('admins.json', 'r', encoding='utf-8') as f:
  admin= json.load(f)

# INFO: START
@bot.message_handler(commands=['start'])
def start(message):
  print(message.text)
  global onEditForm, applications
  if Acceptance_of_applications and message.chat.id not in applications:
    onEditForm = True
    bot.send_message(
      message.chat.id,
      "Привет! 👋\n"
      "Чтобы подать заявку на мероприятие, заполните форму.\n"
    )
    bot.send_message(message.chat.id, "Введите ФИО.")
  elif not Acceptance_of_applications:
    bot.send_message(
      message.chat.id,
      "Привет! 👋\n"
      "Прием заявок на мероприятия закончилось и начнется на ближайших мероприятиях.\n"
      "Новости о ближайших мероприятях можно посмотреть в телеграм канале https://t.me/mcr_rb_03.\n"
    )
  elif message.chat.id in applications:
    bot.send_message(
      message.chat.id,
      "Вы уже подали заявку! 😉",
    )


# INFO: LIST
@bot.message_handler(commands=['list'])
def list_applications(message):
  if applications:
    text = "Список заявок:\n"
    for chat_id, data in applications.items():
      text += f"{str(data['name']).ljust(20, ' ')} {data['telegram_id']}\n"
    bot.send_message(message.chat.id, text)
  else:
    bot.send_message(message.chat.id, "Заявок пока нет. 🤔")



# INFO: GETFILE    
@bot.message_handler(commands=['getFile'])
def get_file(message):
  name = 'file.txt'
  with open(name, 'a+',encoding='utf-8') as file:
    for user in applications:
      file.write(f'{applications[user]["name"].ljust(100, ' ')} {applications[user]["telegram_id"]}\n')
    with open(name, 'rb') as file:
      bot.send_document(message.chat.id, file)
      os.remove(name)





# INFO: START EVENT
@bot.message_handler(commands=['startEvent'])
def start_application(message):
  global Acceptance_of_applications, applications
  if not Acceptance_of_applications:
    Acceptance_of_applications = True
    applications = {}
    bot.send_message(message.chat.id, "Команду понял, принимаю заявки!")
  else:
    bot.send_message(message.chat.id, "Я уже принимаю прием заявок.")






# INFO: END EVENT  
@bot.message_handler(commands=['endEvent'])
def end_application(message):
  global Acceptance_of_applications, applications
  if Acceptance_of_applications:
    Acceptance_of_applications = False
    bot.send_message(message.chat.id, "Команду понял, прием заявок закрываю!")






# INFO: text
@bot.message_handler(content_types=['text'])
def set_info(message):
  print(message.text)
  global onEditForm, applications
  if onEditForm:
    if message.chat.id in applications :
      if 'name' in applications[message.chat.id]:
        bot.send_message(
          message.chat.id,
          "Вы уже подали заявку! 😉",
        )
    else:
      if message.chat.id not in applications:
        applications[message.chat.id] = {}
      
  
    if 'name' not in applications[message.chat.id]:
      applications[message.chat.id]['name'] = message.text
      bot.send_message(message.chat.id, "Заявка принята! 👍")
      bot.send_message(
        message.chat.id, 
        "<b>Мы будем очень рады вас видеть на нашеи мероприятии.</b>😁\n"
        "Проведите это время с нами и поднимите себе настроение.\n"
        "Также завите своих <i>друзей</i>. Вместе веселей!🥳\n"
        "Отправь обязательно им меня для подачи заявки: @MCR03_bot",
        parse_mode="HTML"
      )
      onEditForm = False
      applications[message.chat.id]['telegram_id'] = f'https://t.me/@{message.chat.username}'
    
# INFO: POLLING
bot.polling()