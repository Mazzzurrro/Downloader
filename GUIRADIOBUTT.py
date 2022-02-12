import kivy
kivy.require('1.11.1')
kivy.config.Config.set('graphics','resizable', False)
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
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
from plyer import filechooser
from tkinter import Tk, filedialog
import urllib.request
import re
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

   


now=datetime.now()
today = str(now.strftime("%d_%m_%Y %H_%M_%S")+".txt")
      
#Define different screens
class FirstWindow(Screen):
    baseurl="C:\\Downloads"
    path=f'{baseurl}'
    title_text=StringProperty('')
    titles=[]
    urls=[]
    titledict={}
    
    def suggest(self):
        search = self.ids.suggestioninput.text
        searched=""
        for i in search:
            if i==" ":
                searched+="+"
            else:
                searched+=i
                
        html=urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searched)
        video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
        urls=[]
        videos=[]
        titles=[]
        for i in range(len(video_ids)):
            urls.append("https://www.youtube.com/watch?v="+video_ids[i])
            video = YouTube(urls[i])
            titles.append(video.title)
        self.urls=urls
        self.titles=titles
        keys=titles
        values=urls
        zip_iterator=zip(keys,values)
        self.titledict=dict(zip_iterator)
        self.ids.rv.data= [{'text': str(title[0:60]), 'text_size': self.size, 'halign': 'center','valign': 'middle', 
                            'on_press': partial(self.geturl,title)} for title in titles]
        
    
    def geturl(self,title):
        self.ids.url.text=self.titledict[title]
        
    
        
    def file_chooser(self):
        root = Tk() 
        root.withdraw() 

        root.attributes('-topmost', True) 
        open_file = filedialog.askdirectory()
        self.baseurl=open_file 
        self.ids.path.text=f'{open_file}'
    
    def checkbox_click(self,instance,value,mp3):
        if value == True:
            self.ids.output_label.text="Selected: MP3 file"
        else:
           self.ids.output_label.text="Selected: Video file"
    
    def showtitle(self):
        url=self.ids.url.text
        my_video=YouTube(url)       
        self.thumbnail_url = my_video.thumbnail_url
        self.title_text=my_video.title
        downloaded = self.ids['downloaded']
        thumbnailphoto = AsyncImage(
            source=my_video.thumbnail_url,
            size_hint=(None,None),
            size=(200,200),
            pos_hint={'center_x':0.5,'center_y':-0.3}          
            )
        downloaded.add_widget(thumbnailphoto)
        

        
    def DownloadSingle(self):
        url=self.ids.url.text
        urldownload=self.baseurl
        #my_video.streams.get_highest_resolution()    

        my_video=YouTube(url)
        if(my_video.age_restricted==True):
                with open(today,"a") as f:
                    f.write(my_video.title)
                    f.close()
                pass
        else:
            print(my_video.title)
            if(self.ids.output_label.text=="Selected: MP3 file"):           
                vid = my_video.streams.filter(only_audio=True).first()
                out_file = vid.download(urldownload)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            else:
                my_video.streams.get_highest_resolution().download(urldownload)
                
                
                

class SecondWindow(Screen):  
    
    title_text = StringProperty('')
    baseurl="C:\\Downloads"
    path=f'{baseurl}'
    
    def file_chooser(self):
        root = Tk() 
        root.withdraw() 
        root.attributes('-topmost', True) 
        open_file = filedialog.askdirectory()
        self.baseurl=open_file
        self.ids.path.text=f'{open_file}'
        
    def checkbox_click(self,instance,value,mp3):
        if value == True:
            self.ids.output_label.text="Selected: MP3 file"
        else:
            self.ids.output_label.text="Selected: Video file"
    
    def DownloadSingle(self,video): 
        print("weszlo tutaj")
        urldownload=self.baseurl  
        my_video=video
        if(my_video.age_restricted==True):
                with open(today,"a") as f:
                    f.write(my_video.title)
                    f.close()
                pass
        else:
            if(self.ids.output_label.text=="Selected: MP3 file"):
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
        listurls = self.OrganisePlaylist()[0]
        for i in range(len(titles)):          
            self.title_text=f'Files in your playlist: {titles[i]}'
            downloaded = self.ids['downloaded']
            thumbnailphoto = AsyncImage(
                source=listurls[i].thumbnail_url,
                size_hint=(None,None),
                size=(200,200),
                pos_hint={'center_x':0.5,'center_y':-0.3}          
                )
            downloaded.add_widget(thumbnailphoto)
            time.sleep(2)
            
    def OrganisePlaylist(self):
        url=self.ids.url.text
        urldownload=self.baseurl                        
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

        
                                  

class WindowManager(ScreenManager):
    pass

#Define size and builder
kv = Builder.load_file('kivyfile.kv')
Window.size = (1000, 500)
    
           
class Downloader(App):
    def build(self):
        return kv

if __name__ == '__main__':
    Downloader().run()