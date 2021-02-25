from basic_movement import BasicMovement
from Command import Command
import time

class Process:
    def __init__(self, malmo):
        self.malmo = malmo

    #return a list of words with given pos from the objList
    #POS is a list of part of speches wish to find 
    def find_obj(self, objList, pos = ['NOUN', 'ADV', 'ADJ']):
        words = []
        for tok in objList:
            if tok.pos_ in pos:
                words.append(tok)
        return words
    
    #wrapper function for find_obj use this to parse how many times to do a command
    def parse_numerical(self, objList):
        numList = self.find_obj(objList, ['NUM'])
        if numList:
            return max([int(i) for i in numList])
        return None
    
    def check_tokList(self, tokList, str):
        for tok in tokList:
            if tok.lemma_ == "str":
                return True
        return False

    def process_walk(self, objList, command):
        direction = self.find_obj(objList) 
        distance = self.parse_numerical(objList)
        if distance == None: # no distance was specified
            distance = 1
        print("Distance ->", distance)
        print("Direction ->", direction)

        if self.check_tokList(direction, "left"):
            print("walk left")
            self.malmo.walk_left(distance)
        elif self.check_tokList(direction, "right"):
            print("walk right")
            self.malmo.walk_right(distance)
        elif self.check_tokList(direction, "backward") or self.check_tokList(direction, "backwards"):
            print("walk back")
            self.malmo.walk_backward(distance)
        else : 
            print("walk forward")
            self.malmo.walk_forward(distance)
    
    def process_run(self, objList, command):
        direction = self.find_obj(objList)
        distance = self.parse_numerical(objList)
        if distance == None: # no distance was specified
            distance = 1
        print("Distance ->", distance)
        print("Direction ->", direction)

        if self.check_tokList(direction, "left"):
            self.malmo.run_left(distance)
            print('run left')
        elif self.check_tokList(direction, "right"):
            self.malmo.run_right(distance)
            print('run right')
        elif self.check_tokList(direction, "backward") or self.check_tokList(direction, "backwards"):
            self.malmo.run_backward(distance)
            print('run backwards')
        else:
            self.malmo.run_forward(distance)
            print('run forward')
    
    def process_turn(self, objList, command):
        if "left" in objList:
            pass
        if "right" in objList:
            pass
    
    def process_jump(self, objList, command):
        numJumps = self.parse_numerical(objList)
        if numJumps == None: # no distance was specified
            numJumps = 1
        print("numJumps ->", numJumps)
        print("jump")
        self.malmo.jump(numJumps)
    
    def process_crouch(self, objList, command):
        length = self.parse_numerical(objList)
        if length == None:
            length = 2
        print("length ->", length)
        print("crouch")
        self.malmo.crouch(length)
    
    #TODO add support for synonym objects
    #only recognized specific obj ie recognizes 'find cow' but not 'find cows'
    def process_find(self, objList, command):
        entity = self.find_obj(objList, ['NOUN', 'ADJ'])
        times = self.parse_numerical(objList)
        if times == None:
            times = 1
        
        print("entity ->", entity)
        print("times ->", times)

        if entity:
            print("find")
            self.malmo.find_entity(entity[0].lemma_, times)
        else:
            print('no entity specified')

    #the basic flow is to iterate through all the dicts parseList contains
    #then process the objList ties to the verb
    #depending on the verb, process the objlist differently
    def process_command(self, command):
        parseList = command.parse()
        for c in parseList:
            for verb in c.keys():
                objList = c[verb]
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
                elif verb == "find":
                    self.process_find(objList, command)