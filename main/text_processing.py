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
    #rawActions = determineActions(b_passive,sent)     
    return b_passive, actors  

def determineActors(b_passive,sent):
    results=[]
    #print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
    for word in sent.words:
        if not b_passive:
            if word.deprel == 'nsubj':
                results.append(word.text) 
        else:
            if word.deprel == 'nsubj:pass':
                results.append(word.text)
    
    for word in sent.words:
        if word.head > 0 and word.deprel == 'compound':
            for id, result in enumerate(results):
                if sent.words[word.head-1].text == result:
                    results[id] = word.text + ' ' + result
                    
    
    return results

def qualifyActors(actors):
    resultsDict = {}
    entities =[]
    for sent in doc.sentences:
             for ent in sent.ents:
                 entities.append(ent)

    #print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
    for actor in actors:
        resultsDict[actor]= 'Resource'
        for ent in entities:
            if ent.text in actor:
                    resultsDict[actor]= ent.type
          
        
    #resultsDict[actor] = doc
    return resultsDict


def determineActions(b_passive,sent):
    result=[]
    return result


if __name__ == "__main__":
    doc,s_count = test()
    for i,sent in enumerate(doc.sentences):
        print (i+1, extract_elements(sent))
        _,actors = extract_elements(sent)
        print(qualifyActors(actors))
    #print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
    