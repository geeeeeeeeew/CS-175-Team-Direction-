from basic_movement import BasicMovement
from Command import Command
import time

class Process:
    def __init__(self, malmo):
        self.malmo = malmo
    #the basic flow is to iterate through all the dicts parseList contains
    #then process the objList ties to the verb
    #depending on the verb process the objlist is processed differently
    #for example input is "walk left 5 blocks" -> [{walk:['left', '5 blocks']}] -> process the objlist to dir = 'left' , dis = 5
    def process_command(self, command):
        parseList = command.parse()
        for c in parseList:
            print(c)
            for verb in c.keys():
                objList = c[verb]
                if not objList: #no dobj specified case
                    objList = [""]
                    #planned supported commands crouch, turn, walk, run, jump
                if verb == "walk":
                    dir = 0 #flag to indicate if a direction was specified
                    distance = max([command.parse_numerical(obj) for obj in objList]) #search for the largest numerical value in objList
                    if "left" in objList:
                        self.malmo.walk_left(distance)
                        dir = 1
                    if "right" in objList:
                        self.malmo.walk_right(distance)
                        dir = 1
                    if "backward" in objList or "backwards" in objList:
                        self.malmo.walk_backward(distance)
                        dir = 1
                    if "forward" in objList or dir == 0: # if dir == 0 then no direction was specified so default to forward
                        self.malmo.walk_forward(distance)
                elif verb == "run":
                    dir = 0
                    distance = max([command.parse_numerical(obj) for obj in objList])
                    if "left" in objList:
                        self.malmo.run_left(distance)
                        dir = 1
                    if "right" in objList:
                        self.malmo.run_right(distance)
                        dir = 1
                    if "backward" in objList or "backwards" in objList:
                        self.malmo.run_backward(distance)
                        dir = 1
                    if "forward" or dir == 0:
                        self.malmo.run_forward(distance)
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
                    num_jumps = max([command.parse_numerical(obj) for obj in objList])
                    self.malmo.jump(num_jumps = num_jumps)
                elif verb == "crouch":
                    length = max([command.parse_numerical(obj) for obj in objList])
                    self.malmo.crouch(length = length)

                time.sleep(0.2)