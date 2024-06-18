import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

plt.style.use('ggplot')

# Read in data
df = pd.read_excel("../visualize_data/data/mmiwg_urls.xlsx")
test_titles = df['title'][50]

# tokens = nltk.word_tokenize(test_titles)
# print(tokens)

# tagged = nltk.pos_tag(tokens)
# print(tagged)
#
# entities = nltk.chunk.ne_chunk(tagged)
# entities.pprint()

# VADER (Valence Aware Dictionary and sEntiment Reasoner) Sentiment Scoring, uses the "bag of words" approach, stop words are removes,
# each word is scored and combined to a total score
# does not account for relationship between words

sia = SentimentIntensityAnalyzer()
# print(sia.polarity_scores(test_titles))

results = {}

# Run polarity score on the entire dataset
for i, row in df.iterrows():
    text = row["title"]
    if isinstance(text, float):  # Check if text is a float
        text = str(text)
    results[text] = sia.polarity_scores(text)

vaders = pd.DataFrame(results).T
vaders = vaders.reset_index().rename(columns={'index': 'title'})

# Plot vader results
ax = sns.lineplot(data=vaders, x='title', y='compound')
ax.set_title('Compound Score of Article Titles')
plt.xticks([])
plt.yticks([])
plt.show()
