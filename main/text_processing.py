import nltk
import stanza

#stanza.download('en') # This sets up a default neural pipeline in English. saved to C:\Users\user\stanza_resources.
nlp = stanza.Pipeline('en')

def tokenize_text(text):
    doc = nlp(text)
    return doc

# test works for simple sentences (sentences which do not have subsentences only)
def test():
    file = open("sample_passages/car_insurance_claim_process.txt")
    sample_text = file.readlines()
    doc = tokenize_text(sample_text[0])
    return doc, len(doc.sentences)

def isPassive(sent):
    passive_indicator = "Voice=Pass"
    isPassive = False
    for word in sent.words:
        if word.feats:
            if passive_indicator in word.feats:
                isPassive = True
    return isPassive           
        
def extract_elements(sent):
    actors = []
    rawActions= []
    b_passive = isPassive(sent) 
    actors = determineActors(b_passive,sent)
    rawActions = determineActions(b_passive,sent)     
    return b_passive  

def determineActors(b_passive,sent):
    result=[]
    return result

def determineActions(b_passive,sent):
    result=[]
    return result


if __name__ == "__main__":
    doc,s_count = test()
    for i,sent in enumerate(doc.sentences):
        print (i+1, extract_elements(sent), sent)
    