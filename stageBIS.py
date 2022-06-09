import stanza
import jgrapht

phrase = 'Le chien mange une saucisse.'

nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')
doc = nlp(phrase)

print()

donnees = []

g = jgrapht.create_graph(directed=True, weighted=True, allowing_self_loops=False, allowing_multiple_edges=False,
                         any_hashable=True)

for sent in doc.sentences:
    tempon = []
    for word in sent.words:
        tempon.append((word.text, word.upos, word.lemma))
        # print(f'word: {word.text+" "}\tlemma: {word.lemma} -> Type: {word.upos}')
        g.add_vertex((word.text, word.upos, word.lemma))
    donnees.append(tempon)
    print()

for i in range(len(donnees) - 1):
    g.add_edge(donnees[0][i], donnees[0][i + 1])

print(donnees)

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

print(g)
print(donnees[0][0])
