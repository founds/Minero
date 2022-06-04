__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.01"
__email__ = "info@altsys.es"

import youtube_dl
#from __future__ import unicode_literals

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Youtuber():
    def __init__(self):
        pass

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading \n Now converting ...')

    def download(self, urls):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])



Youtuber().download()