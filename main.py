from speech import record_audio
from Command import Command
from speech_recognition import UnknownValueError
from speech_recognition import RequestError

#sample main loop
if __name__ == "__main__":
    while True:
        try:
            command = Command("Steve has to " + record_audio()) 
            #add "steve has to" to the string so spacy understand the command better
            #ie user says "find 2 sheep" spacy parses "Steve has to find 2 sheep"
            print("raw_text", command.rawText)
            for token in command.doc:
                print(token.text, end=' ')
                print(token.dep_, token.pos_)
            print(command.parse())

            #break
        except UnknownValueError:
            print("Cannot recognize audio")
            continue
        except RequestError:
            print("Speech service down")
            print("Exiting")
            break

        if "exit" in command.rawText:
            print("Exiting")
            break

        #process text
        #execute list of commands in Malmo after processing
