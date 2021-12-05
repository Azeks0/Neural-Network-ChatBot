import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

import random
import json
import pickle
import numpy as np
import nltk


from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer= WordNetLemmatizer

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.tokenize(pattern)
        words.append(word_list)
        documents.append((word_list), intent['tag'])
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lematize(word) for word in words if word not in ignore_letters]
word = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pk1','wb'))
pickle.dump(words, open('classes.pk1', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lematize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0,5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0,5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics = [])






engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def wishMe():
   list1=[1,2]
   if random.choice(list1) ==1:
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            speak("Good Morning,sir")
            print("Good Morning,sir")
        elif hour>=12 and hour<18:
            speak("Good Afternoon,sir")
            print("Good Afternoon,sir")
        else:
            speak("Good Evening,sir")
            print("Good Evening,sir")
        speak("it is currently ")
        speak(hour)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def options(statement):
    if 'mark' in statement:
        statement = statement.replace("mark", "")

    if 'search' in statement:
       wiki(statement)
    if 'that will be all' in statement:
        exit()



def wiki(statement):
    speak('Searching Wikipedia')
    statement = statement.replace("search","")
    results = wikipedia.summary(statement,)
    speak("According to Wikipedia")
    print(results)
    speak(results)





def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source2:
        print("Listening...")
        r.adjust_for_ambient_noise(source2, duration=0.3)
        audio2 = r.listen(source2)
        try:
            statement = r.recognize_google(audio2)
            statement = statement.lower()
            print(f"user said:{statement}\n")
            options(statement)



        except sr.RequestError as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

print("Loading  mark 1.02")
speak("Loading mark 1.02")

wishMe()
def check_key_word(word):
    a=2

def search_word(word):
    check_key_word(word)


def interpret_sentence(sentence):
    sentence = sentence.split(" ")
    for word in range(0, len(sentence)):
        search_word(sentence[word])


if __name__=='__main__':


    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue
