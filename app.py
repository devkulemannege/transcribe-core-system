from pydub import AudioSegment
import yt_dlp as dlp
import os

# create dir if does not exist
try:
    os.mkdir('chunkAudio')
except Exception as e:
    print(e)

# get input file path
audioLink = input('------------------------------------\nEnter link: ')
print('------------------------------------')

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
file = AudioSegment.from_mp3(f'audio/{videoInfo['fulltitle']}.mp3')
count = 0 # variable for output filename iteration tracking

for splitStart in range(0, int(duration), 30):
    for splitStop in range(splitStart+30, splitStart+60, 30):
        # Example: 0-30, 30-60, 60-90, etc...
        count += 1

        chunk = file[splitStart*1000:splitStop*1000] # split in 30 second chunks
        chunk.export(f'chunkAudio/{folder}/chunk{count}.mp3',format='mp3')



