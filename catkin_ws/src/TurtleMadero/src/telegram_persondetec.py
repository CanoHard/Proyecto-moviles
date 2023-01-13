#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import telebot
from sensor_msgs.msg import CompressedImage


BOT_TOKEN = '5102129490:AAETN7xYWjjbjjaFkMnptfPuoeNAhiv0eb8' # token del bot de telegram 

bot = telebot.TeleBot(BOT_TOKEN) # crea un objeto bot de la clase telebot 
chat_id =0  # id del chat de telegram
 
sended = False 

img = None

@bot.message_handler(commands=['start', 'hello']) # comando start y hello 
def send_welcome(message): # funcion que envia un mensaje de bienvenida
    global chat_id
    bot.reply_to(message, "Se ha iniciado el bot") # envia un mensaje de bienvenida 
    chat_id = message.chat.id

def callback_person(data): # funcion que recibe los datos de la deteccion de personas
    global sended
    if chat_id != 0:
        if data.data > 0: # si la cantidad de personas detectadas es mayor a 0 
            if sended == False: 
                bot.send_message(chat_id, "Se ha detectado un intruso", parse_mode="Markdown") # envia un mensaje de deteccion de intruso
                bot.send_photo(chat_id, img)
                sended = True
        else:
            sended = False # Se resetea la variable sended a False

def callback_image(data): # funcion que recibe la imagen de la deteccion de personas
    global img
    img = data.data
    

if __name__ == '__main__':
    rospy.init_node('telegram') # inicializa el nodo de telegram
    rospy.Subscriber("/person_tracking/person_detections", Int32, callback_person) # subscripcion al topic /person_tracking/person_detections
    rospy.Subscriber("person_tracking/deepsort_image/compressed", CompressedImage, callback_image) # subscripcion al topic person_tracking/deepsort_image/compressed

    while True: # bucle infinito
        bot.infinity_polling() # funcion que permite que el bot este siempre escuchando
        if rospy.is_shutdown(): # si el nodo se cierra
            break
