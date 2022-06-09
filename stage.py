import stanza
import jgrapht

phrase = 'Le chien mange une saucisse.'

nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')
doc = nlp(phrase)

print()

donnees = []

for sent in doc.sentences:
    tempon = []
    for word in sent.words:
        tempon.append((word.text, word.upos))
        # print(f'word: {word.text+" "}\tlemma: {word.lemma} -> Type: {word.upos}')
    donnees.append(tempon)
    print()

# print('La prase :', phrase)

print()

regles = [
    ('DET', 'NOUN', 'GN'),
    ('DET', 'GN', 'GN'),
    ('DET', 'ACTION', 'PHRASE'),
    ('ADJ', 'NOUN', 'GN'),
    ('NOUN', 'ADJ', 'GN'),
    ('ADJ', 'GN', 'GN'),
    ('GN', 'ADJ', 'GN'),
    ('VERB', 'GN', 'CO'),  # COD / COI
    ('GN', 'CO', 'ACTION'),
    ('GN', 'VERB', 'ACTION'),
    ('ACTION', 'GN', 'ACTION'),
    ('ACTION', 'PUNCT', 'PHRASE')
]

connexion = []

for d in donnees:
    print("état : ", d)
    while len(d) > 1:
        probleme = True
        saut = False
        i = 0
        while (i + 1) < len(d):
            if saut:
                saut = False
            else:
                for r in regles:
                    if d[i][1] == r[0] and d[i + 1][1] == r[1]:
                        d[i] = (d[i][0] + ' ' + d[i + 1][0], r[2])
                        d.pop((i + 1))
                        saut = True
                        probleme = False
                        break
            i += 1
        if probleme:
            break

        print("état : ", d)

print("\nRésultat :", donnees)
