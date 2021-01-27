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
neuralcoref.add_to_pipe(nlp)

class Command:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.doc = nlp(raw_text)

    def process(self):
        pass
