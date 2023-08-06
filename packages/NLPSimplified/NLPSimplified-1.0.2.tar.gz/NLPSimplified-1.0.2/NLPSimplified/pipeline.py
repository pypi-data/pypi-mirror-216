import spacy

class NlpPipeline:
    def __init__(self, lang='en_core_web_sm'):
        self.nlp = spacy.load(lang)
        self.pipeline = []

    def add_to_pipeline(self, func):
        self.pipeline.append(func)

    def process(self, text):
        doc = self.nlp(text)
        for func in self.pipeline:
            doc = func(doc)
        return doc

def tokenize(doc):
    tokens = [token.text for token in doc]
    doc.set_extension('tokens', default=tokens, force=True)
    return doc

def pos_tagging(doc):
    pos_tags = [(token.text, token.pos_) for token in doc]
    doc.set_extension('pos_tags', default=pos_tags, force=True)
    return doc

def named_entity_recognition(doc):
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    doc.set_extension('entities', default=entities, force=True)
    return doc
