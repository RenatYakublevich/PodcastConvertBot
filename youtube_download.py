from pytube import YouTube
import pytube
import os
from moviepy.editor import *
from datetime import datetime
import time

def download_from_youtube(link,filename):
    '''
    Функция для скачивания видео с ютуба по ссылке
    link - сама ссылка, filename - путь куда установиться видео
    '''
    YouTube(link).streams.first().download('videos/',filename=str(filename))

def delete_audiofile(filename):
    ''' Функция для удаления аудио после конвертации -> отправки пользователю '''
    os.remove(f'videos/{str(filename)}.mp3')

def convert_mp4_to_mp3(filename):
    ''' Функция для конвертирования mp4 файла в mp3 '''
    video = VideoFileClip(os.path.join("videos/",f"{str(filename)}.mp4"))
    video.audio.write_audiofile(os.path.join('videos',f'{str(filename)}.mp3'))
