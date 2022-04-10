# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 18:25:43 2022

@author: Jackson
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.logger import Logger

from os.path import join

from number import Data
n = Data()

import speech_recognition as sr 
r = sr.Recognizer()

    
class Speech:
    
    def getCommand(seconds):
        try:
             with sr.Microphone() as source:
                print('Listening for', seconds, 'seconds')
                voice = r.adjust_for_ambient_noise(source)
                voice = r.record(source, duration=seconds)
                #voice = r.listen(source)
                command = r.recognize_google(voice)
                print(command)
                return command
        except:
            pass
        
    def save(words):
        fob = open('SpeechToTextOutput.txt','w')
        fob.write(words + "\n")
        fob.close()    

        
        

class MyGrid(Widget): 
    def pressed(self):
        print("Seconds: ", self.seconds.text)
        try:
            getSeconds = int(self.seconds.text)
            n.setNumber(getSeconds)
            self.labelMessage.text = f"Listening for {n.getNumber()} seconds." 
        except:
            n.setNumber(5)
            self.labelMessage.text = f"Default to {n.getNumber()} seconds." 
        self.seconds.background_color = 'black'
        
    
    def release(self):
        sentence = Speech.getCommand(n.getNumber())
        try:
            if len(sentence) < 470:
                self.sentenceMessage.text = f"Possible Translation: {sentence}"
            else:
                self.sentenceMessage.text = f"Too many words, but still saved to text file."
        except:
            self.sentenceMessage.text = "No voice input/error occurred. Try again."
        try:
            self.labelMessage.text = "Seconds: \nSuccessfully saved to file."
            Speech.save(sentence)
        except:
            Logger.exception("Cannot reset save file")
            self.labelMessage.text = "Seconds: \nCouldn't save to file."
        self.seconds.background_color = 'white'
        self.seconds.text = "" 
        

class MyApp(App):
    def build(self):
        return MyGrid()
    
if __name__ == "__main__":
    MyApp().run()