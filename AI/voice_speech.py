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

nome = db.reference('/profiles/funcionario1/nome')
planta = db.reference('/plantas/id')

engineio = pyttsx3.init() #inicializa a engine
voices = engineio.getProperty('voices')

engineio.setProperty('rate', 130)    # Aquí puedes seleccionar la velocidad de la voz
# engineio.setProperty('voice',voices[0].id) # escolhe a voz a ser falada
engineio.setProperty('voice', b'brazil') # passando a voz para ptbr

def speak(text):
    engineio.say(text) # fala a string setada
    engineio.runAndWait() # executa e espera

# fala incial de boas vindas
speak('Olá, ' + str(nome.get()) + '! Meu nome é, Alfa!')
# speak('Hello, ' + str(nome.get()) + '! My name is, Alpha!')

# fala sobre destino de plantas
if str(planta.get()) == 'pv14':
    speak('Próximo destino: PV14')
    # speak('Next station: PV14')
elif str(planta.get()) == 'pe3':
    speak('Próximo destino: P, É3')
elif str(planta.get()) == 'pv5':
    speak('Próximo destino: PV5')

# while(1):
#     phrase = input("--> ")
#     if (phrase == "exit"):
#         exit(0)
#     speak(phrase) # seta a string a ser falada
#     print(voices)

# Lista vozes disponiveis
# for voice in voices:
#     if voice.name == 'brazil':
#         engineio.setProperty('voice', voice.id)
#     print(voice.name)