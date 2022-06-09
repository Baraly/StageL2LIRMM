import stanza


class Mot:
    def __init__(self, mot, type, lemma):
        self.mot = mot
        self.type = type
        self.lemma = lemma

    def getMot(self):
        return self.mot

    def getType(self):
        return self.type

    def getLemma(self):
        return self.lemma

    def __str__(self):
        return "(" + self.mot + ", " + self.type + ", " + self.lemma + ")"


class Noeud:
    def __init__(self, value):
        self.value = value
        self.visite = False

    def getValue(self):
        return self.value

    def getVisite(self):
        return self.visite

    def visiter(self):
        self.visite = True

    def __str__(self):
        return self.value.__str__()


class Arc:
    def __init__(self, sortant, entrant, typeConnexion, poids):
        self.sortant = sortant
        self.entrant = entrant
        self.typeConnexion = typeConnexion
        self.poids = poids

    def getDebut(self):
        return self.sortant

    def getArrive(self):
        return self.entrant

    def getTypeConnexion(self):
        return self.typeConnexion

    def getPoids(self):
        return self.poids

    def setPoids(self, poids):
        self.poids = poids


def constructionSyntaxe(doc):
    phrase = []
    for sent in doc.sentences:
        noeud = []
        for word in sent.words:
            mot = Mot(word.text, word.upos, word.lemma)
            noeud.append(Noeud(mot))
            # print(f'word: {word.text+" "}\tlemma: {word.lemma} -> Type: {word.upos}')
        phrase.append([noeud, []])
    return phrase


def constructionGraphe(phrase, regles):
    for p in phrase:
        indice = 0
        while (p[0][-1].getValue()).getType() != 'PHRASE':
            # print(p[0][indice].getValue().getMot() + " -> " + str(p[0][indice].getVisite()))
            if not p[0][indice].getVisite():
                for v in getSuivant(p[1], indice):
                    # print("L'un des ses voisins est : " + str(v))
                    for r in regles:
                        # print(p[0][indice].getValue().getType() + " =? " + r[0] + " ET " + p[0][
                        # v].getValue().getType() + " =? " + r[1])
                        if p[0][indice].getValue().getType() == r[0] and p[0][v].getValue().getType() == r[1] and not \
                                p[0][v].getVisite():
                            # print("L'une des règles à été respectée ! \n")
                            noeud = Noeud(
                                Mot(p[0][indice].getValue().getMot() + " " + p[0][v].getValue().getMot(), r[2],
                                    p[0][indice].getValue().getLemma() + " " + p[0][v].getValue().getLemma()))
                            p[0].append(noeud)

                            p[0][indice].visiter()
                            p[0][v].visiter()

                            p[1].append(Arc(indice, len(p[0]) - 1, 1, 1))
                            p[1].append(Arc(v, len(p[0]) - 1, 1, 1))

                            for voisin in getAncien(p[1], indice):
                                if voisin != len(p[0]) - 1:
                                    p[1].append(Arc(voisin, len(p[0]) - 1, 2, 1))

                            for voisin in getSuivant(p[1], v):
                                if voisin != len(p[0]) - 1:
                                    p[1].append(Arc(len(p[0]) - 1, voisin, 2, 1))

                            break
            # print("L'indice " + str(indice) + " a été utilisé sur " + str(len(p[0])) + " sommets")
            indice += 1

            if indice == len(p[0]):
                break


def getSuivant(connexion, indice):
    list = []
    for arc in connexion:
        if arc.getDebut() == indice:
            list.append(arc.getArrive())
    return list


def getAncien(connexion, indice):
    list = []
    for arc in connexion:
        if arc.getArrive() == indice:
            list.append(arc.getDebut())
    return list


def getConnexion(phrase, num, typeConnexion):
    indice = 1
    for arc in phrase[num][1]:
        print(
            "indice " + str(indice) + " : (" + phrase[num][0][arc.getDebut()].getValue().getMot() + " -> " +
            phrase[num][0][arc.getArrive()].getValue().getMot() + ") (" + phrase[num][0][
                arc.getDebut()].getValue().getType() + ", " +
            phrase[num][0][arc.getArrive()].getValue().getType() + ") / TYPE : " + typeConnexion[
                arc.getTypeConnexion()] + " / POIDS : " + str(arc.getPoids()))
        indice += 1


def main():
    phrase = 'Le chien mange une saucisse.'

    nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')
    doc = nlp(phrase)

    # phrase = [[Noeud[] , Connexion[]], Noeud[] , Connexion[]], ...]

    phrase = constructionSyntaxe(doc)

    for p in phrase:
        for n in range(len(p[0]) - 1):
            p[1].append(Arc(n, n + 1, 0, 1))

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

    typeConnexion = [
        "successeur",
        "combinaison",
        "alternatif"
    ]

    constructionGraphe(phrase, regles)

    print()

    for i in range(len(phrase[0][0])):
        print(print("Les voisins antérieurs de " + str(i) + " sont : " + str(getAncien(phrase[0][1], i))))

    print()
    getConnexion(phrase, 0, typeConnexion)

    print()

    print(phrase)

    print()

    print("J'ai " + str(len(phrase)) + " phrase")
    print("J'ai " + str(len(phrase[0][0])) + " noeuds")
    print("J'ai " + str(len(phrase[0][1])) + " arcs")


main()
