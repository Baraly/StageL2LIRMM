from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

print("LANCEMENT DU PROGRAMME\n")


def algo1():
    text = ["Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Himalayas",
            "point with highest elevation in a region, or on the path of a race or route",
            "third planet from the Sun in the Solar System"]

    topic_model = BERTopic(language="english")

    topics, probs = topic_model.fit_transform()


def algo2():
    docs = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))['data']
    """
    docs = [
        "third planet from the Sun in the Solar System",
        "The Moon is Earth's only natural satellite.",
        "The most widely accepted origin explanation posits that the Moon formed 4.51 billion years ago.",
        "The near side of the Moon is marked by dark volcanic maria.",
        "The only human lunar missions to date have been those of the United States' Apollo program.",
        "The Moon's orbit around Earth has a sidereal period of 27.3 days.",
        "Orbiting Earth at an average distance of 384,400 km.",
        "third planet from the Sun in the Solar System",
        "The Moon is Earth's only natural satellite.",
        "The most widely accepted origin explanation posits that the Moon formed 4.51 billion years ago.",
        "The near side of the Moon is marked by dark volcanic maria.",
        "The only human lunar missions to date have been those of the United States' Apollo program.",
        "The Moon's orbit around Earth has a sidereal period of 27.3 days.",
        "Orbiting Earth at an average distance of 384,400 km."]
    """
    print("doc : " + str(docs))
    topic_model = BERTopic(embedding_model="xlm-r-bert-base-nli-stsb-mean-tokens").fit(docs)
    result = topic_model.transform(['the cat drinks milk.'])
    print()
    print(result.get_info())


algo2()
