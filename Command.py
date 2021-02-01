import spacy
import neuralcoref

#installing neuralcoref:
#pip install neuralcoref
#pip install spacy==2.1.0
#python -m spacy download en_core_web_sm

#check for similiaty with list of supported actions and nouns
#possible optimization: remove ununsed pipelines in spacy
#suppot numerical commands "jump 6 times"
#Processing POS TAGGING, rule based matching, entity recognition (Proper Nouns), lemmatization (reduce words to their base playing -> play)

nlp = spacy.load('en_core_web_sm') #use small sized english model
nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
neuralcoref.add_to_pipe(nlp)

stopwords = ['a', 'an', 'the']

class Command:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.doc = nlp(raw_text)
        if self.doc._.has_coref:
            self.doc = nlp(self.doc._.coref_resolved)

    #helper function for parse() used to get conjunctive sentence/ compound words
    #ie Find a sheep, horse, and cow -> [sheep, horse, cow]
    def parse_conj(self, dobj):
        objList = []
        for child in dobj.children:
            print(child.text)
            if child.pos_ == 'NOUN' and (child.dep_ == 'appos' or child.dep_ == 'conj'):
                objList.append(child.text)
                objList += self.parse_conj(child)
                break
            elif child.dep_ == 'compound':
                objList.append(child.text + ' ' + child.head.text)
        return objList
        
    #Parses doc object and returns a list of dicts. Each dict's key is the verb and the value a list of objects the verb is acting on
    #kind of buggy works on grammarly correct sentences, and mixed results on more relaxed sentences
    def parse(self):
        parseList = []
        for token in self.doc:
            dobjs = []
            pair = {token.lemma_: dobjs}
            if token.pos_ == 'VERB': 
                for child in token.children:
                    if child.pos_ == 'NOUN' or child.dep_ == 'dobj': #verb then noun
                        dobjs.append(child.text)
                        objList = self.parse_conj(child) #check for conjunctions
                        if objList:
                            dobjs += objList
                    elif child.pos_ == 'ADP' and child.dep_ == 'prep': # prepositional phrases
                        for p in child.children:
                            if p.pos_ == 'NOUN':
                                dobjs.append(p.text)
                parseList.append(pair)

        #TODO filter parse
        #TODO search similarty for supported actions
        return parseList

    #filter useless words from object list
    def filter(self, parseList):
        pass

    #check similiarty of action
    def similarity(self, foo, bar):
        pass
