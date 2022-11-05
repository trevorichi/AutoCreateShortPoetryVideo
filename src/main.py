from re import A
from urllib.request import HTTPBasicAuthHandler
import requests
import random
from gtts import gTTS
import creds
from moviepy.editor import * 

def get_poem():
    db_url = "https://poetrydb.org/"
    page = requests.get(db_url + "authors")
    page = page.json()
    authors = page['authors']
    
    num = random.randint(0,len(authors) - 1)
    #This is the Authors Name
    author = authors[num]
    author_page = requests.get(db_url + "author/" + str(author))
    author_page = author_page.json()

    another_num = random.randint(0,len(author_page) - 1)

    author_page = author_page[another_num]  

    #Title of the poem
    title = author_page['title']
    
    #content of the poem
    content = author_page['lines']

    content = ' '.join(content)

    return author,title,content


def create_audio(content):  
    audio = gTTS(text=content,lang='en',slow=False, tld='com.au')  
    audio.save("poem.mp3")  
    

def get_video():
    headers = {
    'Content-type': 'application/json', 
    'Authorization': f'{creds.api_key}'
                }  
    url = 'https://api.pexels.com/videos/popular?per_page=50'
    download_url_builder = 'https://www.pexels.com/video/'
    video = requests.get(url=url,headers=headers)
    video = video.json()

    video_link = video['videos'][random.randint(0,49)]['url']
    video_link = video_link.split('/')
    video_link = video_link[len(video_link)-2]

    video_id = video_link.split('-')
    video_id = video_id[len(video_id) - 1]
    download_url_builder = download_url_builder + video_id +'/download'
    print(download_url_builder)
    r = requests.get(download_url_builder,stream=True)

    # download started 
    print("Starting download...")
    with open('video', 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 
    print("Finished Download")


def create_short():
    print("Starting creating the short...")
    videoclip = VideoFileClip("video")
    audioclip = AudioFileClip("poem.mp3")

    clip = videoclip.set_audio(audioclip)

    clip = clip.loop(duration = audioclip.duration)
    
    print("Writing the file...")
    clip.write_videofile("generated_short.mp4")



if __name__ == "__main__":
   author,title,content = get_poem()
   create_audio(content)
   get_video()
   create_short()
   