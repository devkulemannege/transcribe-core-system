<h1 align="left">
  Basic Audio Transcription Pipeline
  <img src="Assets\Vector.png" width="50" align="right" />
</h1>

**A simple project which contains the core system required for a basic audio transcription pipeline which uses Flask, yt-dlp and pydub.** 

## Prerequisites
- **Ngrok Authtoken** is required and can be obtained using an [Ngrok](https://ngrok.com/) account.
- **FFmpeg** must be installed in client machine to use `yt-dlp` & `pydub`. [Click to see instructions for Windows.](https://www.geeksforgeeks.org/installation-guide/how-to-install-ffmpeg-on-windows/)

## Setup & Usage 
#### 🖥️ Flask server in Colab
`model_server.ipynb` is a jupyter notebook which is intended to be running in a Google Colab enviroment using a TPU or GPU runtime type.
-  Add Ngrok Authtoken as a 'Secret' with the name "ngrok_key" in Colab. The `.ipynb` file (lines 2 - 4 in cell 2) will automatically use the Authtoken specified to authenticate the usage of the Ngrok tunnel.
<img src="Assets\Screenshot 2026-01-18 155711.png" align="center"/>
- Run all code cells in Colab using the "Run all" option to start the Flask server. 
From here onwards the server will be listening to any transcription requests sent from a client machine.

#### 💻 Client Side
The client side will be executing `app.py` Python program.
- Install required Python libraries by running the following. 
    ```bash
    pip install -r requirements.txt
    ```
- Run the client script.
- The script will ask for a YouTube video Link and the Server URL. **The Server URL should be copy-pasted from Colab on to the terminal where required. Server URL is auto-generated.**
→ *below is a dummy URL*
<img src="Assets\Screenshot 2026-01-18 163434.png" align="center"/>
<img src="Assets\Screenshot 2026-01-18 163553.png" align="center"/>
- Client side will download the YouTube video as an .m4a file, split the audio file into 5-second chunks and send them to the server for transcribing.

Both the Flask server and client-side terminals will show live updates as the process is ongoing. Once process is over, the transcription will be saved in `transcription.txt` file.

## Model Information
The model used in this solution can be found at [Hugging Face.](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english)
Specifications:
- A fine-tuned model of Facebook's Wav2Vec2-XLSR-53 model.
- Identificaton Language: English
- Parameters: 300 Million

## Use of Other Models
Other models which supports other languages can be used with this pipeline. But some of the code within cell 1 of `model_server.ipynb` will be required to be changed (depends on model).

**Example: Switching to Sinhala Transcribing...**
A model from Hugging Face such as [Lingalingeswaran/whisper-small-sinhala](https://huggingface.co/Lingalingeswaran/whisper-small-sinhala) for Sinhala transcribing can be used with this pipeline.  
The only change to be made is to add `return_timestamps=True` as an argument to `pipe()` at the following.
```python
text = pipe(audio, return_timestamps=True) # line 17 of cell 1
```


   
 


