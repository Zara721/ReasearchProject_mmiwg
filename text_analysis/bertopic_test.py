from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Read in data
df = pd.read_excel("../visualize_data/data/updated_mmiwg_urls.xlsx")


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]
    return " ".join(filtered_text)


# Convert the 'title' column to a list of strings
texts = df['title'].apply(lambda x: str(x)).tolist()
preprocessed_texts = [remove_stopwords(text) for text in texts]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(preprocessed_texts)

kmeans = KMeans(n_clusters=15, random_state=42)  # Adjust n_clusters as needed
clusters = kmeans.fit_predict(X)


representation_model = KeyBERTInspired()
topic_model = BERTopic(representation_model=representation_model, hdbscan_model=kmeans)
topics, probs = topic_model.fit_transform(preprocessed_texts)
# print(topics)

# Generate Labels
topic_labels = topic_model.generate_topic_labels(nr_words=3, topic_prefix=False, word_length=15, separator="_")
topic_model.set_topic_labels(topic_labels)

topic_df = pd.DataFrame(topic_model.get_topic_info())

selected_columns_df = topic_df.loc[:, ["Topic", "Count", "Name"]]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', None)
print(selected_columns_df)

# fig = topic_model.visualize_barchart(width=350, height=330, top_n_topics=12, n_words=10)
# fig = topic_model.visualize_heatmap(n_clusters=20)
fig = topic_model.visualize_documents(docs=texts)
fig.show()

