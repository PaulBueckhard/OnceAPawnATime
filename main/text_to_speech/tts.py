from gtts import gTTS
import playsound
import os

name = "test"
filename = "%s.mp3" % name


tts = gTTS('This move is not legal', lang='en')

tts.save(filename)

playsound.playsound(filename)

os.remove(filename) 