from speech import record_audio
from Command import Command
from speech_recognition import UnknownValueError
from speech_recognition import RequestError

#sample main loop
if __name__ == "__main__":
    while True:
        try:
            command = Command(record_audio())
            print("raw_text", command.raw_text)
            print("coreference resolution", command.doc._.coref_resolved)
        except UnknownValueError:
            print("Cannot recognize audio")
            continue
        except RequestError:
            print("Speech service down")
            print("Exiting")
            break

        if "exit" in command.raw_text:
            print("Exiting")
            break

        #process text
        #execute list of commands in Malmo after processing