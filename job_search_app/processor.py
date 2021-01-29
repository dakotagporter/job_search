import spacy
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")


def preprocessor(doc):
    doc = nlp(doc)
    return [token.lemma_ for token in doc if not token.is_stop and
            not token.is_punct]


def vectorize_text(text):
    vect = TfidfVectorizer(preprocessor=preprocessor)
    vect.fit(text)
    dtm = vect.transform(text)

    return dtm


def find_neighbors(dtm, new_desc_vect):
    nn = NearestNeighbors(algorithm='kd_tree', n_neighbors=5)
    nn.fit(dtm)
    dist, inds = nn.kneighbors(new_desc_vect)

    return inds
