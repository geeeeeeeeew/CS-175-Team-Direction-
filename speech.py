import speech_recognition as sr

r = sr.Recognizer()

def record_audio():
    try:
        with sr.Microphone() as source:
            print("Say something")
            audio = r.listen(source)
            voice_data = r.recognize_google(audio)
            return voice_data
    except sr.UnknownValueError:
        print("Cannot recognize audio")
    except sr.RequestError:
        print("Speech service down")

#sample main loop
if __name__ == "__main__":
    while True:
        command = record_audio()
        print(command)

        #process command

        if "exit" in command:
            print("Exiting")
            break