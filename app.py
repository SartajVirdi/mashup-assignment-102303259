from flask import Flask, request, render_template, send_file
import os
import smtplib
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# Import the function from your script (rename your script to mashup.py for import or copy the function here)
# For this example, I will assume the logic is copied below for simplicity in one file.

from yt_dlp import YoutubeDL
from pydub import AudioSegment

app = Flask(__name__)

def createMashup(singer, count, duration):
    outputFile = "mashup_output.mp3"
    # (Same logic as above, condensed)
    ydlOpts = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True, 'outtmpl': 'temp_web/%(title)s.%(ext)s', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',}]}
    if not os.path.exists('temp_web'): os.makedirs('temp_web')
    with YoutubeDL(ydlOpts) as ydl:
        ydl.download([f"ytsearch{count}:{singer}"])
    
    combined = AudioSegment.empty()
    files = [f for f in os.listdir('temp_web') if f.endswith('.mp3')]
    for f in files[:count]:
        audio = AudioSegment.from_mp3(os.path.join('temp_web', f))
        combined += audio[:duration*1000]
    
    combined.export(outputFile, format="mp3")
    
    # Zip it
    zipName = "mashup.zip"
    with zipfile.ZipFile(zipName, 'w') as zipF:
        zipF.write(outputFile)
        
    # Cleanup
    for f in os.listdir('temp_web'): os.remove(os.path.join('temp_web', f))
    os.rmdir('temp_web')
    os.remove(outputFile)
    
    return zipName

def sendEmail(recipientEmail, filename):
    senderEmail = "abhishekpanchal2005@gmail.com"
    senderPassword = "jqwj fgsh zpfs hdfo" 
    
    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = recipientEmail
    msg['Subject'] = "Your Mashup File"
    
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, senderPassword)
    server.send_message(msg)
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        singer = request.form['singer']
        count = int(request.form['count'])
        duration = int(request.form['duration'])
        email = request.form['email']
        
        zipFile = createMashup(singer, count, duration)
        sendEmail(email, zipFile)
        
        return "Mashup sent to your email!"
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
