import stanza
import jgrapht


def voisin(graphe, i):
    pass


phrase = 'Le chien mange une saucisse.'

nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')
doc = nlp(phrase)

print()

donnees = []
connexion = []

g = jgrapht.create_graph(directed=True, weighted=True, allowing_self_loops=False, allowing_multiple_edges=False)

for sent in doc.sentences:
    tempon = []
    i = 0
    for word in sent.words:
        tempon.append((word.text, word.upos, word.lemma))
        # print(f'word: {word.text+" "}\tlemma: {word.lemma} -> Type: {word.upos}')
        connexion.append((word.text, word.upos, word.lemma))
        g.add_vertex(i)
        i += 1
    donnees.append(tempon)
    print()

for i in range(len(connexion) - 1):
    g.add_edge(i, i + 1)

print("Connexions :", connexion)

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

print("Graphe :", g)
print("La première étiquette pointe vers :", connexion[g.edge_target(0)])

# while connexion[-1][1] != 'PHRASE':

for d in range(len(connexion)):
    print("état : ", connexion[d])
    saut = False
    if saut:
        saut = False
    else:
        for r in regles:
            if connexion[d][1] == r[0] and connexion[d + 1][1] == r[1]:
                connexion.append(
                    (connexion[d][0] + ' ' + connexion[d + 1][0], r[2],
                     (connexion[d][2] + ' ' + connexion[d + 1][2])))
                g.add_vertex(len(connexion) - 1)
                g.add_edge(d, len(connexion) - 1)
                g.add_edge(d + 1, len(connexion) - 1)
                # g.add_edge(len(connexion) - 1, )
                saut = True
                probleme = False
                break

# print(voisin(g, 0))
for i in g.edges_of(1):
    print("arrête :", i, " -> élément :", g.edge_target(i))

print()
print(connexion)
print(g)
