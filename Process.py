from basic_movement import BasicMovement
from malmo_commands import SpeechToSteve
from Command import Command
import time

class Process:
    def __init__(self, malmo):
        self.malmo = malmo
        
    #return a list of words with given pos from the objList
    #POS is a list of part of speches wish to find 
    #sampled dependencies -> dep = ['acamp', 'pobj', 'dobj', 'advmod', 'compound']
    def find_obj(self, objList, pos = ['NOUN', 'ADV', 'ADJ'], dep = [] ):
        words = []
        for tok in objList:
            if dep:
                if tok.pos_ in pos and tok.dep_ in dep: #OR AND?
                    words.append(tok)
            else:
                if tok.pos_ in pos:
                    words.append(tok)
        return words
    
    #wrapper function for find_obj use this to parse how many times to do a command
    def parse_numerical(self, objList):
        numList = self.find_obj(objList, ['NUM'])
        if numList:
            return max([int(i.text) for i in numList])
        return None
    
    def check_tokList(self, tokList, string):
        for tok in tokList:
            if tok.lemma_ == string:
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
        direction = self.find_obj(objList)
        num = self.parse_numerical(objList)
        if num == None:
            num = 1
        if self.check_tokList(direction, "left"):
            self.malmo.turn_left(num)
            print('turn left')
        else:
            self.malmo.turn_right(num)
            print('turn right')
    
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

    #find the furthest pig to the right and kill it with a diamond shovel
    def process_find(self, objList, command):
        entity = self.find_obj(objList, ['NOUN'])
        modifier = self.find_obj(objList, ['ADJ', 'ADV'])
        directionList = self.find_obj(objList)
        times = self.parse_numerical(objList)

        if times == None:
            times = 1

        #check for direction modifier
        direction = None
        for d in directionList:
            if d.lemma_ == "left":
                direction = "right"
                break
            elif d.lemma_ == "right":
                direction = "right"
                break
        
        mostSimilarDist = 0 #can be either 0 or -1, 0 for closest, -1 for farthest. Default to 0 for now
        bestSimilarity = 0
        for mod in modifier:
            #replace mod with "close" or "far"
            print("SIMILAIRYT check ->", mod.lemma_)
            farSimilarity = max(command.similarity_words(mod.lemma_, "far"), command.similarity_words(mod.lemma_, "farth"))
            closeSimilarity = command.similarity_words(mod.lemma_, "close")
            print(closeSimilarity, farSimilarity)
            if farSimilarity > 0.8 and farSimilarity > bestSimilarity:
                mostSimilarDist = -1
                bestSimilarity = farSimilarity
            if closeSimilarity > 0.8 and closeSimilarity >  bestSimilarity:
                mostSimilarDist = 0
                bestSimilarity = closeSimilarity

        print("times ->", times)
        print("dir",direction)
        print("dist", mostSimilarDist)

        if entity:
            print("find")
            #find most similar entity:
            mostSimilarEnt = None
            bestSimilarity = 0
            for ent in entity:
                for foo in command.entities:
                    similarity = command.similarity_words(ent.lemma_, foo)
                    if similarity > bestSimilarity:
                        mostSimilarEnt = foo
                        bestSimilarity = similarity
                print("entity ->", mostSimilarEnt)
                self.malmo.find_entity(mostSimilarEnt, times, dis = mostSimilarDist, direction = direction)
        else:
            print('no entity specified')

    def process_switch(self, objList, command):
        hotbarList = self.malmo.get_hotbarList()
        item = self.find_obj(objList, ['NOUN'])
        #modifier = self.find_obj(objList, ['ADJ', 'ADV', ])
        if item:
            for i in item:
                print(i)
                iRight = [w.lemma_ for w in i.rights if w.pos_ == 'ADJ' or w.dep_ == 'compound']
                iLeft = [w.lemma_ for w in i.lefts if w.pos_ == 'ADJ' or w.dep_ == 'compound']
                print(iRight, iLeft)
                foo = " ".join( iLeft +[i.text] + iRight)

                bestSimilarItem = None
                bestSimilarity = 0
                print(hotbarList)
                for item in hotbarList:
                    similarity = command.similarity_words(foo, item.replace("_", " "))
                    print(similarity)
                    if similarity > bestSimilarity:
                        bestSimilarItem = item
                        bestSimilarity = similarity
                self.malmo.switch_item(bestSimilarItem)
        else:
            print('no item specified')

    
    def process_kill(self, objList, command):
        entity = self.find_obj(objList, ['NOUN'])
        item = self.find_obj(objList, ['NOUN'], ['pobj']) # kill [entity] with [item]
        modifier = self.find_obj(objList, ['ADJ', 'ADV'])
        directionList = self.find_obj(objList)
        times = self.parse_numerical(objList)

        if times == None:
            times = 1
        
        bestSimilarItem = None
        bestSimilarity = 0
        if item:
            hotbarList = self.malmo.get_hotbarList()
            for i in item:
                iRight = [w.lemma_ for w in i.rights if w.pos_ == 'ADJ' or w.dep_ == 'compound']
                iLeft = [w.lemma_ for w in i.lefts if w.pos_ == 'ADJ' or w.dep_ == 'compound']
                foo = " ".join( iLeft +[i.text] + iRight)

                for item in hotbarList:
                    similarity = command.similarity_words(foo, item.replace("_", " "))
                    if similarity > bestSimilarity:
                        bestSimilarItem = item
                        bestSimilarity = similarity
            
        #check for direction modifier
        direction = None
        for d in directionList:
            if d.lemma_ == "left":
                direction = "right"
                break
            elif d.lemma_ == "right":
                direction = "right"
                break
        
        mostSimilarDist = 0 #can be either 0 or -1, 0 for closest, -1 for farthest. Default to 0 for now
        bestSimilarity = 0
        for mod in modifier:
            #replace mod with "close" or "far"
            print("SIMILAIRYT check ->", mod.lemma_)
            farSimilarity = max(command.similarity_words(mod.lemma_, "far"), command.similarity_words(mod.lemma_, "farth"))
            closeSimilarity = command.similarity_words(mod.lemma_, "close")
            if farSimilarity > 0.8 and farSimilarity > bestSimilarity:
                mostSimilarDist = -1
                bestSimilarity = farSimilarity
            if closeSimilarity > 0.8 and closeSimilarity >  bestSimilarity:
                mostSimilarDist = 0
                bestSimilarity = closeSimilarity

        print("times ->", times)
        print("dir",direction)
        print("dist", mostSimilarDist)

        if entity:
            print("kill")
            #find most similar entity:
            mostSimilarEnt = None
            bestSimilarity = 0
            for ent in entity:
                for foo in command.entities:
                    similarity = command.similarity_words(ent.lemma_, foo)
                    if similarity > bestSimilarity:
                        mostSimilarEnt = foo
                        bestSimilarity = similarity
                print("entity ->", mostSimilarEnt)
                self.malmo.kill_entity(mostSimilarEnt, times, dis = mostSimilarDist, direction = direction, item = bestSimilarItem)
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
                elif verb == "find" or verb == 'go':
                    self.process_find(objList, command)
                elif verb == 'kill':
                    self.process_kill(objList, command)
                elif verb == 'switch' or verb == 'equip':
                    self.process_switch(objList,command)
