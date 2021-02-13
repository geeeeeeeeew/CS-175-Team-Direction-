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
#nlp.Defaults.stop_words |= {'a','an','the', 'to'} 
#nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
#nlp.add_pipe(nlp.create_pipe('merge_entities'))
neuralcoref.add_to_pipe(nlp)

class Command:
    filterWords = {'a','an','the', 'to', 'then', 'for', 'in', 'on', 'at', 'by'} #static class atribute
    actions = {'move': ['jump', 'walk', 'crouch', 'run']} #planned supported actions for status report
    #used a dict so similarity checks for a category of actions (keys) and then searches for specfic supported actions(values)
    #reduces search to a category of actions instead the entire range of actions

    def __init__(self, rawText):
        numerical = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four':'4', 'five': '5', 'six':'6', 'seven': '7', 'eight':'8', 'nine': '9'}
        wordList = []
        for word in rawText.split():
            if word in numerical.keys():
                wordList.append(numerical[word])
            else:
                wordList.append(word)
        self.rawText = " ".join(wordList)
        self.doc = nlp(self.rawText)
        if self.doc._.has_coref:
            self.doc = nlp(self.doc._.coref_resolved)

    #helper function for check_adj()
    def check_prep(self, prep):
        nouns = []
        for tok in prep.children:
            if tok.pos_ == 'NOUN':
                print(tok.text)
                nouns.append(tok)
        return nouns
        
    #helper function for parse() used to pick up potential undetected noun chunks
    def check_adj(self, word):
        rightTokens = []   
        leftTokens = []     
        for tok in word.rights:
            if tok.pos_ == 'ADP' and tok.dep_ == 'prep':
                for n in self.check_prep(tok):
                    rightTokens += self.check_adj(n)
            elif tok.pos_ == "NUM" or tok.pos_ == "ADJ" or tok.pos_ == "ADV" or tok.dep_ == "compound":
                rightTokens.append(tok.lemma_)

        for tok in word.lefts:
            if tok.pos_ == 'ADP' and tok.dep_ == 'prep':
                for n in self.check_prep(tok):
                    leftTokens += self.check_adj(n)
            elif tok.pos_ == "NUM" or tok.pos_ == "ADJ" or tok.pos_ == "ADV" or tok.dep_ == "compound":
                    leftTokens.append(tok.lemma_)
                    
        print("check adj ->", word.text, '->', leftTokens + [word.text] + rightTokens)
        return leftTokens + [word.text] + rightTokens
    
    #helper function for parse() used to get conjunctive sentence/ compound words
    #ie Find a sheep, horse, and cow -> [sheep, horse, cow]
    def parse_conj(self, dobj, verb):
        objList = []
        for child in dobj.children:
            print("parse conjunction ->", dobj.text, '-> ', child.text)
            #three cases: noun+conj, adv+appos, adp+prep
            if child.pos_ == 'NOUN' or child.pos_ == 'ADV':
                objList.append( {verb: self.check_adj(child)} )
                objList += self.parse_conj(child, verb) 
        return objList
    
    #check prep function??

    #Parses doc object and returns a list of dicts. Each dict's key is the verb and the value a list of words that has
    #an important dependence on the verb
    #kind of buggy works on grammarly correct sentences, and mixed results on more relaxed sentences
    def parse(self):
        parseList = []
        for token in self.doc:
            if token.pos_ == 'VERB':
                print("VERB -> ", token.lemma_) 
                print("VERB CHILDREN -> ", [c.text for c in token.children])
                dobjs = []
                pair = {token.lemma_: dobjs}
                for child in token.children:
                    print("VERB CHILD ->", child.text)
                    if child.pos_ == 'NOUN' or child.dep_ == 'dobj': #verb then noun
                        print("NOUN CASE")
                        dobjs += self.check_adj(child)
                        objList = self.parse_conj(child, token.lemma_) #check for conjunctions
                        if objList:
                            parseList += objList
                    elif child.pos_ == 'ADP' and child.dep_ == 'prep': # prepositional phrases
                        print("PREP PHRASE CASE")
                        for p in child.children:
                            print("prep", p.text)
                            if p.pos_ == 'NOUN':
                                dobjs += self.check_adj(p) 
                                objList = self.parse_conj(p,token.lemma_) #don't check for conjunction preps?
                                if objList:
                                    parseList += objList
                    elif (child.pos_ == 'ADV' or child.dep_ == 'advmod') and not child.text in Command.filterWords: #add adverbs
                        print("ADVERB CASE")
                        dobjs += (self.check_adj(child))
                        objList = self.parse_conj(child, token.lemma_) #check for conjunctions
                        if objList:
                            parseList += objList
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
        doc = nlp("Steve has to " + word)
        for key in Command.actions.keys():
            currentProb = nlp("Steve has to " + key).similarity(doc)
            if currentProb > mostSimilarProb:
                mostSimilar = key
                mostSimilarProb = currentProb
        mostSimilarProb = 0 #rest max prob 
        for action in Command.actions[mostSimilar]:
            currentProb = nlp("Steve has to " + action).similarity(doc)
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

    #takes a string, returns any numerical modifier for an object as an int
    def parse_numerical(self, s):
        doc = nlp(s)
        n = 1
        for tok in doc:
            print(tok.text, tok.pos_)
            if tok.pos_ == "NUM":
                n = int(tok.text)
                break
        return n