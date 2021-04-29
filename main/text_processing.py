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
    actors = {}
    rawActions= []
    b_passive = isPassive(sent) 
    actors = determineActors(b_passive,sent)
    #rawActions = determineActions(b_passive,sent)     
    return b_passive, actors  


"""
Determine Actors is the key method to resolve actors, resources which helps in identification of entitites
"""
def determineActors(b_passive,sent):
    results={}
    #print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
    for word in sent.words:
        if not b_passive:
            if word.deprel == 'nsubj':
                results[word.id] = word.text
        else:
            if word.deprel == 'nsubj:pass':
                results[word.id] = word.text
    """
    for word in sent.words:
        # if one compound has as its head another compound ithen they need to be carry forward togethr
        if word.head > 0 and word.deprel == 'compound' :
            for id, result in enumerate(results):
                if sent.words[word.head-1].text == result:
                    results[id] = word.text + ' ' + result
        if word.head > 0 and word.deprel == 'flat':
            for id, result in enumerate(results):
                newResult = result
                if sent.words[word.head - 1].text == result:
                    rnewResult = newRresult + ' ' + word.text
                    print(results[id])
            results[id] = newResult
    """
    #print(results)
    for k, v in results.items(): 
        new_Subject =''
        condition_no = 0
        for word in sent.words:
            if word.id <= k and word.head > 0 and word.deprel == 'compound': # condition for compounds between nsubj & det
                new_Subject = new_Subject + word.text + ' '
                condition_no = 1
            elif word.head > 0 and word.head == k and word.deprel == 'flat': # condition for following flat relations after nsubj
                new_Subject = new_Subject + ' ' + word.text 
                condition_no = 2
        
        if condition_no == 1:
            results[k]= new_Subject + v 
        elif condition_no == 2:
            results[k] = v + new_Subject

    return results

"""
qualifyActors is the method in wich we can add logic to further disambiguiate the type of Actors/ resouces
"""
def qualifyActors(actors):
    resultsDict = {}
    entities =[]
    for sent in doc.sentences:
             for ent in sent.ents:
                 entities.append(ent)

    #print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
    for k,actor in actors.items():
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
       # print (i+1, extract_elements(sent))
        _,actors = extract_elements(sent)
        print(qualifyActors(actors))
    #print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
    