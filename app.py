from pydub import AudioSegment
import yt_dlp as dlp
import requests
import shutil
import os
import re

''' # Remove the comment markers to automatically delete previous downloaded audio and it's chunks
try:
    shutil.rmtree('audio')
    os.mkdir('audio')

    shutil.rmtree('chunkAudio')
    os.mkdir('chunkAudio')
except Exception as e:
    print(f'{e}')'''

# create dir & remove transcription.txt for fresh transcription
try:os.mkdir('chunkAudio')
except Exception as e:print(e)
try:os.mkdir('audio')
except Exception as e:print(e)
try:os.remove('transcription.txt')
except Exception as e:print(e)

# get input file path
print('------------------------------------')
audioLink = input('Enter video link: ')
server_url = input('Enter server url: ')
print('------------------------------------')

# yt-dlp section
yt_audio = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio[ext=wav]/bestaudio/best',
    'ignore_expires': True,
    'outtmpl': 'audio/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True
}

with dlp.YoutubeDL(yt_audio) as ydl: 
    videoInfo = ydl.extract_info(audioLink, download=False) # retrieve video infomation
    duration = videoInfo['duration'] # retreive video duration in seconds
    ydl.download([audioLink])

folder = videoInfo['fulltitle']
os.mkdir(f'chunkAudio/{folder}') # create folder for chunks

# pydub section
file = AudioSegment.from_mp3(f'audio/{folder}.mp3')
count = 0 # variable for output filename iteration tracking (Ex: chunk1, chunk2, chunk3)

for splitStart in range(0, int(duration), 5):
    for splitStop in range(splitStart+5, splitStart+10, 5):
        # Example: 0-5, 5-10, 10-15, etc...
        count += 1

        chunk = file[splitStart*1000:splitStop*1000] # split in 5 second chunks
        chunk.export(f'chunkAudio/{folder}/chunk{count}.mp3',format='mp3')

chunkDir = os.listdir(f'chunkAudio/{folder}') # get chunk files as a list
chunkDir.sort(key=lambda var: [int(x) if x.isdigit() else x for x in re.split('([0-9]+)', var)])
print(f'Chunk Files: {chunkDir}') # debug

# server transaction section
try:
    for chunk in chunkDir:
        with open(f'chunkAudio/{folder}/{chunk}', 'rb') as binary: # read chunk files as binary and send to server
            print(f'------------------------------------\nSending {chunk} to server...')

            response = requests.post(
                server_url, 
                files= {'file': (chunk, binary, 'audio/mpeg')},
                timeout=600
            ).json()

            with open('transcription.txt','a', encoding='utf-8') as export:
                export.write(response['reply']) # write to transcription.txt
            
        print(f'Transcription finished for {chunk}')
except Exception as e:
    print(f'Failed to communicate with server: {e}')

print('\nProcess Finished.')
    