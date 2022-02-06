import sys
sys.path.append("c:\\users\\dom\\appdata\\local\\programs\\python\\python39\\lib\\site-packages")
#python main.py -c kivy:debug
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pytube import Playlist
from kivy.uix.widget import Widget
from pytube import YouTube
from datetime import datetime
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import time
from functools import partial
import threading
from kivy.properties import StringProperty
    

baseurl="C:\\Users\\dom\\Desktop\\Sciaganie"
now=datetime.now()
today = str(now.strftime("%d_%m_%Y %H_%M_%S")+".txt")
        
#Define different screens
class FirstWindow(Screen):
    def checkbox_click(self,instance,value,mp3):
        if value == True:
            self.ids.output_label.text="You selected downloading MP3 file"
        else:
           self.ids.output_label.text="You selected downloading video file"
    
    def DownloadSingle(self):
        url=self.ids.url.text
        urldownload=baseurl
        #my_video.streams.get_highest_resolution()    

        my_video=YouTube(url)
        if(my_video.age_restricted==True):
                with open(today,"a") as f:
                    f.write(my_video.title)
                    f.close()
                pass
        else:
            print(my_video.title)
            if(self.ids.output_label.text=="You selected downloading MP3 file"):
                self.ids.output_label.text=f'Currently downloading: {my_video.title}'
                vid = my_video.streams.filter(only_audio=True).first()
                out_file = vid.download(urldownload)
                base, ext = os.path.splitext(out_file)
                print(base)
                print(ext)
                new_file = base + '.mp3'
                print(new_file)
                os.rename(out_file, new_file)
            else:
                self.ids.output_label.text=f'Currently downloading: {my_video.title}'
                my_video.streams.get_highest_resolution().download(urldownload)
                
                
                

class SecondWindow(Screen):  
    
    title_text = StringProperty('') 
    
    def checkbox_click(self,instance,value,mp3):
        if value == True:
            self.ids.output_label.text="You selected downloading MP3 file"
        else:
            self.ids.output_label.text="You selected downloading video file"
    
    def DownloadSingle(self,video): 
        print("weszlo tutaj")
        urldownload=baseurl  
        my_video=video
        if(my_video.age_restricted==True):
                with open(today,"a") as f:
                    f.write(my_video.title)
                    f.close()
                pass
        else:
            if(self.ids.output_label.text=="You selected downloading MP3 file"):
                vid = my_video.streams.filter(only_audio=True).first()
                out_file = vid.download(urldownload)
                base, ext = os.path.splitext(out_file)
                print(base)
                print(ext)
                new_file = base + '.mp3'
                print(new_file)
                os.rename(out_file, new_file)
            else:
                my_video.streams.get_highest_resolution().download(urldownload) 

    def showtitle(self):
        titles = self.OrganisePlaylist()[1]
        for i in titles:          
            self.title_text=f'You are currently downloading: {i}'
            time.sleep(1)
        
             
    def OrganisePlaylist(self):
        url=self.ids.url.text
        urldownload=baseurl                        
        my_playlist=Playlist(url)
        listurls=[]
        titles=[]
        for my_video in my_playlist.videos:
            listurls.append(my_video)
            titles.append(my_video.title)
        return listurls, titles
    
    def DownloadPlaylist(self):
        listurls=self.OrganisePlaylist()[0]
        titles=self.OrganisePlaylist()[1]
        for i in listurls:
            self.DownloadSingle(i)                    
        print("Finished")
        
                                  

class WindowManager(ScreenManager):
    pass

#Define size and builder
kv = Builder.load_file('GUI2.kv')
Window.size = (800, 230)
    
           
class Downloader(App):
    def build(self):
        return kv

if __name__ == '__main__':
    Downloader().run()