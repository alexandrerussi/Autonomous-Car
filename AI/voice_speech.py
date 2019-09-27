
import pyttsx3
import engineio

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/Users/mac/Documents/GitHub/Autonomous-Car/AI/alphanumbraskem-firebase.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://alphanumbraskem.firebaseio.com/'
})

ref = db.reference('/profiles/funcionario1/nome')

print(ref.get())

engineio = pyttsx3.init() #inicializa a engine
voices = engineio.getProperty('voices')

# Lista vozes disponiveis
# for voice in voices:
#     if voice.name == 'brazil':
#         engineio.setProperty('voice', voice.id)
#     print(voice.name)

engineio.setProperty('rate', 130)    # Aquí puedes seleccionar la velocidad de la voz
#engineio.setProperty('voice',voices[0].id) # escolhe a voz a ser falada
engineio.setProperty('voice', b'brazil') # passando a voz para ptbr

def speak(text):
    engineio.say(text) # fala a string setada
    engineio.runAndWait() # executa e espera

speak('Olá, ' + str(ref.get()) + '! Meu nome é Alpha!')
# while(1):
#     phrase = input("--> ")
#     if (phrase == "exit"):
#         exit(0)
#     speak(phrase) # seta a string a ser falada
#     print(voices)
