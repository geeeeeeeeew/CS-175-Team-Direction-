from basic_movement import BasicMovement
from Command import Command

class Process:
    def __init__(self, malmo):
        self.malmo = malmo

    def process_command(self, command):
        parseList = command.parse()
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
                        elif "backwards" in objList:
                            pass
                        else:
                            print("WALK", command.parse_numerical(obj))
                            self.malmo.move_forward(distance = command.parse_numerical(obj))
                    elif verb == "run":
                        if "left" in objList:
                            pass
                        elif "right" in objList:
                            pass
                        elif "backwards" in objList:
                            pass
                        else:
                            pass
                    elif verb == "turn":
                        if "left" in objList:
                            pass
                        elif "right" in objList:
                            pass
                        elif "backwards" in objList:
                            pass
                        else:
                            pass
                    elif verb == "jump":
                        print("JUMP")
                        print(command.parse_numerical(obj))
                        self.malmo.jump(num_jumps=command.parse_numerical(obj))
                    elif verb == "crouch":
                        pass