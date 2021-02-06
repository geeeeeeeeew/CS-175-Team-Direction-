import spacy
import neuralcoref

#installing neuralcoref:
#pip install neuralcoref
#pip install spacy==2.1.0
#python -m spacy download en_core_web_md

#check for similiaty with list of supported actions and nouns
#possible optimization: remove ununsed pipelines in spacy
#suppot numerical commands "jump 6 times"
#Processing POS TAGGING, rule based matching, entity recognition (Proper Nouns), lemmatization (reduce words to their base playing -> play)

nlp = spacy.load('en_core_web_md') #use medium sized english model
nlp.Defaults.stop_words |= {'a','an','the', 'to'} #add stop words to default set
nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
nlp.add_pipe(nlp.create_pipe('merge_entities'))
neuralcoref.add_to_pipe(nlp)

class Command:
    filterWords = nlp.Defaults.stop_words #static class atribute
    filterWords |= {'a','an','the', 'to'} #add to filter word set
    actions = {'move': ['jump', 'walk', 'sprint']} #current supported actions
    #used a dict so similarity checks for a category of actions (keys) and then searches for specfic supported actions(values)
    #reduces search to a category of actions instead the entire range of actions

    def __init__(self, rawText):
        self.rawText = rawText
        self.doc = nlp(rawText)
        if self.doc._.has_coref:
            self.doc = nlp(self.doc._.coref_resolved)

    #helper function for parse() used to pick up potential undetected noun chunks
    def check_adj(self, word):
        newWord = word.text
        rightChildTokens = [tok.text for tok in word.rights if tok.pos_ == "NUM" or tok.pos_ == "ADJ"]
        leftChildTokens = [tok.text for tok in word.lefts if tok.pos_ == "NUM" or tok.pos_ == "ADJ"]
        if rightChildTokens and leftChildTokens:
            newWord = " ".join(leftChildTokens) + " " + word.text + " ".join(rightChildTokens)
        elif rightChildTokens:
            newWord =  word.text + " ".join(rightChildTokens)
        elif leftChildTokens:
            newWord = " ".join(leftChildTokens) + " " + word.text
        return newWord
    
    #helper function for parse() used to get conjunctive sentence/ compound words
    #ie Find a sheep, horse, and cow -> [sheep, horse, cow]
    def parse_conj(self, dobj):
        objList = []
        for child in dobj.children:
            #print("parse conjunction", child.text)
            if child.pos_ == 'NOUN' and (child.dep_ == 'appos' or child.dep_ == 'conj'):
                objList.append(self.check_adj(child))
                objList += self.parse_conj(child)
                break
        return objList
        
    #Parses doc object and returns a list of dicts. Each dict's key is the verb and the value a list of objects the verb is acting on
    #kind of buggy works on grammarly correct sentences, and mixed results on more relaxed sentences
    def parse(self):
        parseList = []
        for token in self.doc[3:]:
            print(token.text)
            dobjs = []
            pair = {token.lemma_: dobjs}
            if token.pos_ == 'VERB': 
                for child in token.children:
                    if child.pos_ == 'NOUN' or child.dep_ == 'dobj': #verb then noun
                        dobjs.append(self.check_adj(child)) # need to check for adj noun chunks do not pick up
                        objList = self.parse_conj(child) #check for conjunctions
                        if objList:
                            dobjs += objList
                    elif child.pos_ == 'ADP' and child.dep_ == 'prep': # prepositional phrases
                        for p in child.children:
                            if p.pos_ == 'NOUN':
                                dobjs.append(self.check_adj(p)) #need to check for adj noun chunks do not pickup
                parseList.append(pair)
        print("PARSELIST BEFORE FILTER ->", parseList)
        self.filter(parseList) #filtering
        print("PARSELIST AFTER FILTER ->", parseList)
        parseList = self.similarity(parseList) #similarity check against Command.actions
        print("PARSELIST AFTER SIMILARITY ->", parseList)
        return parseList

    #filter unnecessary words from object list
    def filter(self, parseList):
        for i, pair in enumerate(parseList):
            for k in pair.keys():
                for j,obj in enumerate(pair[k]):
                        filteredString = ' '.join([word for word in obj.split() if not word in Command.filterWords])
                        parseList[i][k][j] = filteredString
    
    #helper function for similarity
    def best_similarity(self,word):
        mostSimilar = ""
        mostSimilarProb = 0
        doc = nlp(word)
        for key in Command.actions.keys():
            currentProb = nlp(key).similarity(doc)
            if currentProb > mostSimilarProb:
                mostSimilar = key
                mostSimilarProb = currentProb

        mostSimilarProb = 0 #rest max prob 

        for action in Command.actions[mostSimilar]:
            currentProb = nlp(action).similarity(doc)
            if currentProb > mostSimilarProb:
                mostSimilar = action
                mostSimilarProb = currentProb

        return mostSimilar

    #jump run walk
    #check similiarty of action
    #only actions
    def similarity(self, parseList):
        newParseList = []
        for i,pair in enumerate(parseList):
            for k in pair.keys():
                objList = parseList[i][k] #save old keys objList
                newKey = self.best_similarity(k)
                newParseList.append({newKey:objList})
        return newParseList