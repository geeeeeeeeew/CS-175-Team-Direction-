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
            print(c)
            for verb in c.keys():
                objList = c[verb]
                if not objList: #no dobj specified case
                    objList = [""]
                for obj in objList:
                    #planned supported commands crouch, turn, walk, run, jump
                    if verb == "walk":
                        if "left" in objList:
                            pass
                        elif "right" in objList:
                            pass
                        else:
                            print("WALK", command.parse_numerical(obj))
                            move.move_forward(distance = command.parse_numerical(obj))
                    elif verb == "run":
                        if "left" in objList:
                            pass
                        elif "right" in objList:
                            pass
                        else:
                            pass
                    elif verb == "turn":
                        if "left" in objList:
                            pass
                        elif "right" in objList:
                            pass
                        else:
                            pass
                    elif verb == "jump":
                        print("JUMP")
                        print(command.parse_numerical(obj))
                        move.jump(num_jumps=command.parse_numerical(obj))
                    elif verb == "crouch":
                        pass