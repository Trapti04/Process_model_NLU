import nltk
import stanza

#stanza.download('en') # This sets up a default neural pipeline in English. saved to C:\Users\user\stanza_resources.

sample1 = 'Once the Senior General manager approves the invoice, then we can process it. It will  take 10 days after that to complete the reimbursement'
print(sample1)
file1 = open("sample_passages/car_insurance_claim_process.txt")
sample_text = file1.readlines()
nlp = stanza.Pipeline('en')

doc = nlp(sample_text[0])
for sentence in doc.sentences:
    print(sentence.ents)
for sentence in doc.sentences:
    print(sentence.dependencies)
print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')
print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
