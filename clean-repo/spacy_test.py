import spacy, dateparser
nlp = spacy.load("en_core_web_sm")
doc = nlp("Finish report by next Friday for Alice.")
print([(ent.text, ent.label_) for ent in doc.ents])
print("Parsed date:", dateparser.parse("next Friday"))
