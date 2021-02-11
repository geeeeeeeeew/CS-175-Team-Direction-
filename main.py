from speech import record_audio
from Command import Command
from speech_recognition import UnknownValueError
from speech_recognition import RequestError
from basic_movement import BasicMovement
import time

#sample main loop
if __name__ == "__main__":
    move = BasicMovement({})
    while True:
        try:
            command =  record_audio()
            #command = str(input("Type your command: ")) #for keyboard input, uncomment this line and comment out line 10
            command = Command("Steve has to " + command)
            #add "steve has to" to the string so spacy understand the command better
            #ie user says "find 2 sheep" spacy parses "Steve has to find 2 sheep"
            print("raw_text", command.rawText)
            for token in command.doc:
                print(token.text, end=' ')
                print(token.dep_, token.pos_)    
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
        
        parseList = command.parse()
        print(parseList)
        for c in parseList:
            for verb in c.keys():
                objList = c[verb]
                if not objList: #no dobj specified case
                    objList = [""]
                for obj in objList:
                    if verb == 'walk left' in obj:
                        print("WALK left", command.parse_numerical(obj))
                        move.walk_left(distance = command.parse_numerical(obj))
                    elif verb == 'walk' or verb == 'walk forward':
                        print("WALK", command.parse_numerical(obj))
                        move.walk_forward(distance = command.parse_numerical(obj))
                    elif verb == 'walk right':
                        print("WALK right", command.parse_numerical(obj))
                        move.walk_right(distance = command.parse_numerical(obj))
                    elif verb == 'walk backward':
                        print("WALK back", command.parse_numerical(obj))
                        move.walk_backward(distance = command.parse_numerical(obj))

                    elif verb == 'run left':
                        print("RUN left", command.parse_numerical(obj))
                        move.run_left(distance = command.parse_numerical(obj))
                    elif verb == 'run right':
                        print("RUN right", command.parse_numerical(obj))
                        move.run_right(distance = command.parse_numerical(obj))
                    elif verb == 'run' or verb == 'run forward':
                        print("RUN", command.parse_numerical(obj))
                        move.run_forward(distance = command.parse_numerical(obj))
                    elif verb == 'run backward':
                        print("RUN backward", command.parse_numerical(obj))
                        move.run_backward(distance = command.parse_numerical(obj))

                    elif verb == "jump":
                        print("JUMP")
                        print(command.parse_numerical(obj))
                        move.jump(num_jumps=command.parse_numerical(obj))
        time.sleep(.2)

        #execute list of commands in Malmo after processing
