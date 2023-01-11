#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import telebot
from sensor_msgs.msg import CompressedImage


BOT_TOKEN = '5102129490:AAETN7xYWjjbjjaFkMnptfPuoeNAhiv0eb8'

bot = telebot.TeleBot(BOT_TOKEN)
chat_id =0

sended = False

img = None

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    global chat_id
    bot.reply_to(message, "Se ha iniciado el bot")
    chat_id = message.chat.id

def callback_person(data):
    global sended
    if chat_id != 0:
        if data.data > 0:
            if sended == False:
                bot.send_message(chat_id, "Se ha detectado un intruso", parse_mode="Markdown")
                bot.send_photo(chat_id, img)
                sended = True
        else:
            sended = False

def callback_image(data):
    global img
    img = data.data
    

if __name__ == '__main__':
    rospy.init_node('telegram')
    rospy.Subscriber("/person_tracking/person_detections", Int32, callback_person)
    rospy.Subscriber("person_tracking/deepsort_image/compressed", CompressedImage, callback_image)

    while True:
        bot.infinity_polling()
        if rospy.is_shutdown():
            break
