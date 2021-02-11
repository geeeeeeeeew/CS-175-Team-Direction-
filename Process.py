from basic_movement import BasicMovement
from Command import Command
import time

class Process:
    def __init__(self, malmo):
        self.malmo = malmo

    def process_walk(self, objList, command):
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
    
    def process_run(self, objList, command):
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
    
    def process_turn(self, objList, command):
        if "left" in objList:
            pass
        if "right" in objList:
            pass
    
    def process_jump(self, objList, command):
        num_jumps = max([command.parse_numerical(obj) for obj in objList])
        self.malmo.jump(num_jumps = num_jumps)
    
    def process_crouch(self, objList, command):
        length = max([command.parse_numerical(obj) for obj in objList])
        self.malmo.crouch(length = length)
        
    #the basic flow is to iterate through all the dicts parseList contains
    #then process the objList ties to the verb
    #depending on the verb process the objlist is processed differently
    #for example input is "walk left 5 blocks" -> [{walk:['left', '5 blocks']}] -> process_walk(objList, command) -> processes the objlist to dir = 'left' , dis = 5 -> sends to malmo
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
                    self.process_walk(objList, command)
                elif verb == "run":
                    self.process_run(objList, command)
                elif verb == "turn":
                    self.process_turn(objList, command)
                elif verb == "jump":
                    self.process_jump(objList, command)
                elif verb == "crouch":
                    self.process_crouch(objList, command)

                time.sleep(0.2)