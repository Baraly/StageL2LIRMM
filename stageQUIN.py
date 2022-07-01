import stanza
import pygraphviz as pgv


class Mot:
    def __init__(self, mot, type):
        self.mot = mot
        self.type = type

    def getMot(self):
        return self.mot

    def getType(self):
        return self.type

    def __str__(self):
        return "(" + self.mot + ", " + self.type + ")"


class Noeud:
    def __init__(self, value):
        self.value = value
        self.poids = 1
        self.visite = False

    def getValue(self):
        return self.value

    def getVisite(self):
        return self.visite

    def getPoids(self):
        return self.poids

    def visiter(self):
        self.visite = True

    def __str__(self):
        return self.value.__str__() + " (poids : " + str(self.poids) + ")"


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

    def __str__(self):
        return "(" + str(self.sortant) + " -> " + str(self.entrant) + ") type : " + str(self.typeConnexion)


def constructionSyntaxe(doc):
    phrase = []
    for sent in doc.sentences:
        noeud = [Noeud(Mot("<start>", "CODON"))]
        for word in sent.words:
            mot = Mot(word.text, word.upos)  # word.lemma
            noeud.append(Noeud(mot))
            # print(f'word: {word.text+" "}\tlemma: {word.lemma} -> Type: {word.upos}')
        noeud.append(Noeud(Mot("<end>", "CODON")))
        phrase.append([noeud, []])

    for p in phrase:
        arcEntrant = {}
        arcSortant = {}
        for n in range(len(p[0]) - 1):
            p[1].append(Arc(n, n + 1, 0, 1))
            if n == 0:
                arcEntrant.__setitem__(0, [])
            else:
                arcEntrant.__setitem__(n, [n - 1])
            arcSortant.__setitem__(n, [n])
        arcSortant.__setitem__(len(p[0]) - 1, [])
        arcEntrant.__setitem__(len(p[0]) - 1, [len(p[1]) - 1])
        p.append(arcSortant)
        p.append(arcEntrant)

    return phrase


def appliquerRegles(listNoeud, listArc, listArcSortant, listArcEntrant, regles, indice1, indice2):
    for r in regles:
        if listNoeud[indice1].getValue().getType() == r[0] and listNoeud[indice2].getValue().getType() == r[1] and not \
                listNoeud[indice2].getVisite():

            noeud = Noeud(Mot(
                listNoeud[indice1].getValue().getMot() + " " + listNoeud[
                    indice2].getValue().getMot(),
                r[2]))
            listNoeud.append(noeud)
            listArcSortant.__setitem__(len(listNoeud) - 1, [])
            listArcEntrant.__setitem__(len(listNoeud) - 1, [])

            listNoeud[indice1].visiter()
            listNoeud[indice2].visiter()

            listArc.append(Arc(indice1, len(listNoeud) - 1, 1, 1))
            listArcSortant[indice1].append(len(listArc) - 1)
            listArcEntrant[len(listNoeud) - 1].append(len(listArc) - 1)

            listArc.append(Arc(indice2, len(listNoeud) - 1, 1, 1))
            listArcSortant[indice2].append(len(listArc) - 1)
            listArcEntrant[len(listNoeud) - 1].append(len(listArc) - 1)

            for v in listArcEntrant[indice1]:
                if listArc[v].getDebut() != len(listNoeud) - 1 and listArc[
                    v].getTypeConnexion() != 1:
                    listArc.append(Arc(listArc[v].getDebut(), len(listNoeud) - 1, 2, 1))
                    listArcSortant[listArc[v].getDebut()].append(len(listArc) - 1)
                    listArcEntrant[len(listNoeud) - 1].append(len(listArc) - 1)

            for v in listArcSortant[indice2]:
                if listArc[v].getArrive() != len(listNoeud) - 1:
                    listArc.append(Arc(len(listNoeud) - 1, listArc[v].getArrive(), 2, 1))
                    listArcSortant[len(listNoeud) - 1].append(len(listArc) - 1)
                    listArcEntrant[listArc[v].getArrive()].append(len(listArc) - 1)

            return True

    return False


def nombreNoeudNonVisite(listNoeud):
    compteur = 0
    for noeud in listNoeud:
        if not noeud.getVisite():
            compteur += 1
    return compteur


def constructionGraphe(phrase, regles):  # Prépare le doliprane, cet algorithme fait mal...
    for p in phrase:
        indice = 0
        while nombreNoeudNonVisite(p[0]) > 3:
            regleAppliquee = False
            for v in p[3][indice]:
                if not p[0][indice].getVisite() and not p[0][p[1][v].getDebut()].getVisite():
                    if appliquerRegles(p[0], p[1], p[2], p[3], regles, p[1][v].getDebut(), indice):
                        regleAppliquee = True
                        break

            if not regleAppliquee:
                for v in p[2][indice]:
                    if not p[0][indice].getVisite() and not p[0][p[1][v].getArrive()].getVisite():
                        if appliquerRegles(p[0], p[1], p[2], p[3], regles, indice, p[1][v].getArrive()):
                            break

            indice += 1

            if indice >= len(p[0]):
                print("ERREUR : arret d'urgence du while")
                for n in p[0]:
                    if not n.getVisite():
                        print("Le noeud : " + str(n))
                break


def ajoutLemme(phrase, nlp):
    for p in phrase:
        for a in range(1, len(p[1])):
            if (p[1][a]).getTypeConnexion() == 0:
                doc = nlp(p[0][p[1][a].getDebut()].getValue().getMot())
                motLemme = ""
                motUpos = ""
                for sent in doc.sentences:
                    for word in sent.words:
                        motLemme += word.lemma
                        motUpos += word.upos
                p[0].append(Noeud(Mot(motLemme, motUpos)))
                p[1].append(Arc(p[1][a].getDebut(), len(p[0]) - 1, 3, 1))
                p[2].__setitem__(len(p[0]) - 1, [])
                p[2][p[1][a].getDebut()].append(len(p[1]) - 1)
                p[3].__setitem__(len(p[0]) - 1, [len(p[1]) - 1])


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


def afficherGraphe(phrase):
    indice = 1
    for p in phrase:
        graph = pgv.AGraph(directed=True)
        graph.node_attr["shape"] = "box"

        graph.node_attr['style'] = 'filled'

        for arc in p[1]:
            graph.add_edge(p[0][arc.getDebut()].getValue().getMot(), p[0][arc.getArrive()].getValue().getMot())
            if arc.getTypeConnexion() == 0 and arc.getDebut() != 0:
                n = graph.get_node('' + p[0][arc.getDebut()].getValue().getMot())
                n.attr['fillcolor'] = "#FFC300"

        graph.layout('dot')

        nom = "phrase" + str(indice) + ".png"
        graph.draw(nom)

        graph.close()

        indice += 1


def getInfoBETA(id_noeud, listeNoeud, listArcs, listArcEntrant, regles):
    while True:
        parents = []
        for voisin in listArcEntrant[id_noeud]:
            if listArcs[voisin].getTypeConnexion() == 1:
                parents.append(listArcs[voisin].getDebut())

        print("Les voisins de " + str(id_noeud) + " sont : " + str(listArcEntrant[id_noeud]))
        if len(parents) == 2:
            p1 = parents[0]
            p2 = parents[1]

            print("Pour le type : " + listeNoeud[id_noeud].getValue().getType() + ", on a :")
            print(listeNoeud[p1].getValue().getType() + " + " + listeNoeud[p2].getValue().getType())
            n = input("\nChoissiez : ")

            if int(n) == 1:
                return getInfoBETA(p1, listeNoeud, listArcs, listArcEntrant, regles)
            else:
                return getInfoBETA(p2, listeNoeud, listArcs, listArcEntrant, regles)

        else:
            print("Nous sommes arrivés à " + listeNoeud[id_noeud].getValue().getMot())
            return


def getInfo(id_noeud, listeNoeud, listArcs, listArcEntrant, regles):
    while True:
        parents = []
        for voisin in listArcEntrant[id_noeud]:
            if listArcs[voisin].getTypeConnexion() == 1:
                parents.append(listArcs[voisin].getDebut())

        if len(parents) == 2:

            for p in parents:
                if listeNoeud[p].getValue().getType() == "GN":
                    return getInfo(p, listeNoeud, listArcs, listArcEntrant, regles)
                if listeNoeud[p].getValue().getType() == "GN+GV":
                    return getInfo(p, listeNoeud, listArcs, listArcEntrant, regles)
                if listeNoeud[p].getValue().getType() == "GN+GV+CDN":
                    return getInfo(p, listeNoeud, listArcs, listArcEntrant, regles)
                if listeNoeud[p].getValue().getType() == "PRON":
                    print("La phrase parle d'un : " + listeNoeud[p].getValue().getMot())
                    return
                if listeNoeud[p].getValue().getType() == "NOUN":
                    print("La phrase parle d'un : " + listeNoeud[p].getValue().getMot())
                    return

            print("La phrase parle d'un : " + listeNoeud[id_noeud].getValue().getMot())

            return


        else:
            print("ERROR")
            return


def main():
    phraseInit = "Le grand classeur rouge est rangé."

    # Le chien mange une saucisse.
    # Le chat noir boit calmement du lait frais de chêvre que sa jolie maîtresse lui a acheté au supermarché du village d'à coté.
    # Tu es un ordinateur.
    # J'aime le chocolat.
    # Le grand classeur rouge est rangé.

    nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma')
    doc = nlp(phraseInit)

    # phrase = [[Noeud[] , Arc[], ArcEntrant[], ArcSortant[]], Noeud[] , Arc[], ArcEntrant[], ArcSortant[]], ...]

    phrase = constructionSyntaxe(doc)

    regles = [
        ('DET', 'NOUN', 'GN'),  # le chat
        ('VERB', 'GN', 'GV'),  # mange une pomme
        ('DET', 'GN', 'GN'),  # le gros chat
        ('VERB', 'ADV', 'GV'),  # boit calmement
        ('AUX', 'ADV', 'GV'),  # est actuellement
        ('DET', 'GN+PRON+GV', 'GN+PRON+GV'),  # sa jolie maîtresse lui a acheté
        ('ADJ', 'NOUN', 'GN'),  # gros chat
        ('ADJ', 'GN', 'GN'),  # longue voiture rouge
        ('GN', 'ADJ', 'GN'),  # longue voiture rouge
        ('GN', 'CDN', 'GN'),  # le chat de la craimière
        # ('VERB', 'ADJ', 'GV'),
        ('AUX', 'ADJ', 'GV'),  # suis beau
        ('AUX', 'GN', 'GV'),  # suis un garçon
        ('PRON', 'GV', 'GN+GV'),  # je suis
        # ('VERB', 'GV', 'GV'),  #
        ('GN', 'GV', 'GN+GV'),  # le chat boit
        ('GN+PRON', 'VERB', 'GN+PRON+GV'),  # sa jolie maîtresse lui a acheté
        ('GN+PRON', 'GV+PUNCT', 'GN+PRON+GV'),  # sa jolie maîtresse lui a acheté .
        # ('GN+PRON+GV', 'CDN', 'GN+PRON+GV'),  #
        ('GN+GV', 'CDN', 'GN+GV+CDN'),  # le chat boit du lait de chêvre
        ('ADP', 'CDN', 'CDN'),  # d'à coté
        ('CDN', 'ADP', 'CDN'),  # en train de
        ('GN+GV', 'PUNCT', 'PHRASE'),  # le chat boit .
        ('ADP', 'NOUN', 'CDN'),  # de chêvre (Complément Du Nom)
        ('ADP', 'GN', 'CDN'),  # de chêvre blanche
        ('CDN', 'CDN', 'CDN'),  # du lait frais de chêvre
        ('VERB', 'CDN', 'GV'),  # boit du lait
        ('AUX', 'VERB', 'VERB'),  # j'ai été
        ('GN', 'PRON', 'GN+PRON'),  # sa jolie maîtresse lui
        ('PRON', 'GN+PRON+GV', 'SUBRELA'),  # que sa maîtresse lui a acheté
        ('SCONJ', 'GN+PRON+GV', 'SUBRELA'),  # que sa maîtresse lui a acheté ('que' peut varier de type..)
        ('GN+GV+CDN', 'SUBRELA', 'GN+GV'),  # le chat boit du lait que sa maîtresse lui a acheté
        ('GN+GV+CDN', 'GV', 'GN+GV'),  # l'ordinateur est actuellement en train de faire des calculs
        ('GN+GV+CDN', 'PUNCT', 'GN+GV+CDN'),
        ('VERB', 'PUNCT', 'GV'),  # suis .
        # ('ADP', 'GV', 'COD'),
        # ('VERB', 'COD', 'GV')
    ]

    typeConnexion = [
        "successeur",
        "combinaison",
        "alternatif",
        "lemme"
    ]

    constructionGraphe(phrase, regles)

    print()

    for p in phrase[0][0]:
        print(str(p.getValue().getMot()) + " (" + str(p.getValue().getType()) + ")")

    print()

    # print(phrase[0][0][len(phrase[0][0]) - 1])

    print("Dans la phrase :\n'" + phraseInit + "'\n")
    getInfo(len(phrase[0][0]) - 1, phrase[0][0], phrase[0][1], phrase[0][3], regles)

    ajoutLemme(phrase, nlp)

    print()

    for i in phrase:
        # print("Arcs Sortants :", i[2])
        # print("Arcs Entrants :", i[3])
        print()

    afficherGraphe(phrase)

    # print(str(calculCheminPlusCourt(phrase[0][1], phrase[0][2], 1, 9)))


main()
