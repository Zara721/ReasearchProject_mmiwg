"""
Sources: https://www.youtube.com/watch?v=QpzMWQvxXWk
"""
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from nltk.sentiment import SentimentIntensityAnalyzer

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch.nn.functional as F

plt.style.use('ggplot')

# Read in data
df = pd.read_excel("../visualize_data/data/mmiwg_urls.xlsx")
test_title = df['title'][50]


def preprocess_text(text):
    # Replace the phrase "missing, murdered indigenous women" with "indigenous women"
    text = text.replace("missing, murdered indigenous women", "indigenous women")
    return text


# test_title = preprocess_text(test_title)
# print(test_title)
# sia = SentimentIntensityAnalyzer()
# print(sia.polarity_scores(test_title))

article_title = "Missing and murdered Aboriginal children: apologies offer little in the face of systemic police failures | Amanda Porter and Alison Whittaker | The Guardian"
article_title2 = "Canada to launch inquiry into missing, murdered Aboriginal women | Daily Sabah"
article_title3 = "Missing and murdered Indigenous women honoured at vigil | Calgary Sun"

artcle_body = """
Skip to main content
Skip to navigation
Skip to navigation
Print subscriptions
Sign in
Search jobs
Search
International edition
The Guardian - Back to home
The Guardian
News
Opinion
Sport
Culture
Lifestyle
Show
More
Australia
World
AU politics
Environment
Climate crisis
Indigenous Australia
Immigration
Media
Business
Science
Tech
Podcasts
Newsletters
View image in fullscreen
A rally will be held for all Aboriginal and Torres Strait Islander people who have died in custody, as well as all unsolved murders and missing persons. Photograph: Glenn Hunt/Getty Images
Opinion
Deaths in custody
 This article is more than 4 years old
Missing and murdered Aboriginal children: apologies offer little in the face of systemic police failures
This article is more than 4 years old
Amanda Porter and Alison Whittaker

They won’t console families of victims who were likely to have been targeted for being young and Black


Tue 20 Aug 2019 06.38 BST
Share

The families of 15 missing Aboriginal children are uniting to raise public awareness of Aboriginal deaths in custody, unsolved murders and missing person cases.

The state-wide rally will bring together the families of Colleen Walker-Craig, Clinton Speedy-Duroux, Evelyn Greenup, TJ Hickey, Jaylen Close-Armstrong, Lewis “Buddy” Kelly Jnr, David Dungay Jnr, Mark Haines, Theresa Binge, Rayshaun Carr, Kamahl Bamblett, Tane Chatfield and Steven Smith.

The names of some of these young people – such as TJ Hickey, a 14-year-old Kamilaroi boy who died in February 2004 after being the target of a police pursuit in Redfern, Sydney – are already known to the Australian public.

‘Police shouldn’t be investigating police’: family anger over death in custody inquest
Read more

The names of other children will be less familiar. This is the case for Lewis “Buddy” Kelly Jnr, a young Aboriginal boy from Kempsey whose body was found in highly suspicious circumstances on a railway line south of Kempsey on New Year’s Eve in 1983.

Some of the young people have died as the result of the practices of state officials while in custody. This has been the case for David Dungay Jnr, a 26-year old Dunghutti man who died in December 2015 while being restrained by five prison officers while screaming “I can’t breathe”.

Others have been the victim of serious crime, but the police investigation into the victim’s death has been severely impacted by systemic oversights and shortcomings, and indifference by the police. This has been the case in the death of Mark Haines, a Gomeroi teenager who died in suspicious circumstances in January 1988.

As with the cases of the Bowraville murders – involving the deaths of Colleen Walker-Craig, Clinton Speedy-Duroux and Evelyn Greenup – the initial police investigation into these deaths was characterised by various failures and shortcomings. This included failure to follow up on crucial leads and the delay in collection of evidence due to racial assumptions made by investigating police officers because of the victim’s Aboriginality.

The rate of incarceration and the correlated risk of death in police or prison custody remains unacceptably high

In August 2016, then-NSW police commissioner Andrew Scipione delivered a formal apology to the Bowraville families for inadequacies in the initial police investigation.

But apologies offer little in the face of systemic police failures, especially in circumstances where failures in the initial police investigation directly impede chances of receiving a fair trial and the quality of evidence necessary in securing an eventual conviction. This was the case for the Bowraville families who in March this year had their appeal for special leave rejected by the high court of Australia.

Nor do apologies go far in consoling families whose loved ones were the victim of racially motivated violence, in circumstances where the victims were likely to have been targeted for being young and Black.

T
hese are not isolated cases. They reflect but 15 of innumerable deaths in which the perpetrator remains at large and for which justice has never been secured. The stories of Bowraville and Kempsey bear similarities to countless other regional and remote townships.

In the community of Borroloola, for example, a young boy was found dead in suspicious circumstances in 2007. A young Aboriginal woman was found dead in 2013 in eerily similar circumstances. In 2018 coroner Greg Cavanagh delivered an inquest with scathing comments about the substandard investigation carried out by the Northern Territory police. No one has been charged in relation to either death.

In the township of Bourke, two teenage Aboriginal girls – Mona Smith and Jacinta Smith – died in horrific circumstances while in the company of a middle-aged non-Indigenous man, who was later acquitted of allegations he had killed the two Aboriginal girls by driving while drunk. A charge of sexual misconduct with a corpse was withdrawn.

In Maclean on the far-north coast of NSW, 33-year-old Aboriginal woman Lynette Daley was brutally murdered by non-Indigenous men Adrian Attwater and Paul Maris. The investigation and decision to prosecute was initially marred by the same formula of political inaction and indifference that has characterised public officials’ responses in these 15 cases. Although the NSW director of public prosecutions twice declined to prosecute in relation to Daley’s death, an investigation into the circumstances of her death in May 2016 promoted public awareness of the issue and eventually led to a review of the decision.

I
n June the Final Report of the Canadian National Inquiry into Missing and Murdered Indigenous Women and Girls, “Reclaiming Power and Place”, was delivered to the Canadian federal government. It included the testimonies of 2,380 family members, consisting of two volumes and 231 recommendations. The national inquiry revealed persistent and deliberate pattern of human rights abuses and characterised the issue of missing and murdered Aboriginal women and children in terms of genocide.

The report follows a series of inquiries and systemic reviews into substandard police investigations into missing persons cases. A recent example includes the final report into the Thunder Bay police service which found that the police consistently “devalued Indigenous lives, reflected differential treatment and were based on racist attitudes and stereotypical preconceptions about Indigenous people”.

On this side of the globe, the issue of national inquiries and royal commissions has tended to focus on Aboriginal deaths in police and prison custody, or include Aboriginal people as an intersecting experience of other kinds of violence like violence in care, institutions or in family settings. This is not to deny the reality of substandard police investigations into Aboriginal missing persons and murdered Aboriginal young people, which represents the other side of the genocidal coin.

'Dragged like a dead kangaroo': why language matters for deaths in custody | Alison Whittaker
Read more

This year marks the 28th anniversary since the tabling in parliament of the royal commission into Aboriginal deaths in custody, which remains to date the most extensive and systematic investigation into Aboriginal and Torres Strait Islander deaths in police and prison custody. The royal commission examined the individual circumstances of 99 Aboriginal deaths in custody and made 339 recommendations in relation to state reform.

Since this time, at least 410 further deaths have occurred in police or prison custody. Despite the recommendations of the royal commission and countless subsequent national inquiries, royal commissions and coronial inquests, the rate of incarceration and the correlated risk of death in police or prison custody remains unacceptably high.

The reaction on the part of successive state and federal governments can only be described as one of political inaction and callous indifference.

A state-wide rally will take place on Wednesday at Sydney’s Town Hall at 12:30 for all Aboriginal and Torres Strait Islander people who have died in custody, as well as all unsolved murders and missing persons.

 Amanda Porter is an independent researcher and volunteer; Alison Whittaker is a Gomeroi poet and law scholar

Explore more on these topics
Deaths in custody
Opinion
Indigenous Australians
Indigenous incarceration
Law (Australia)
David Dungay
comment
Share
Reuse this content
Most viewed
Australia
World
AU politics
Environment
Climate crisis
Indigenous Australia
Immigration
Media
Business
Science
Tech
Podcasts
Newsletters
News
Opinion
Sport
Culture
Lifestyle
Original reporting and incisive analysis, direct from the Guardian every morning
Sign up for our email
Help
Complaints & corrections
SecureDrop
Work for us
 
Privacy policy
Cookie policy
Terms & conditions
Contact us
All topics
All writers
Digital newspaper archive
Facebook
YouTube
Instagram
LinkedIn
X
Newsletters
Advertise with us
Search UK jobs
Back to top
© 2024 Guardian News & Media Limited or its affiliated companies. All rights reserved. (dcr)
"""

# Using Roberta Pretrained Model, transformer model accounts for the words but also the context related to other words

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


def polarity_scores_roberta(text):
    encoded_text = tokenizer(text, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach()
    softmax_scores = F.softmax(scores, dim=0)
    # print(scores)

    scores_dict = {
        'roberta_neg': scores[0],
        'roberta_neutral': scores[1],
        'roberta_pos': scores[2],
    }
    return scores_dict


sia = SentimentIntensityAnalyzer()
results = {}

# Run polarity score on the entire dataset
for i, row in df.iterrows():
    text = row["title"]
    if isinstance(text, float):  # Check if text is a float
        text = str(text)
    vader_result = sia.polarity_scores(text)
    vader_results_rename = {}
    for key, value in vader_result.items():
        vader_results_rename[f"vader_{key}"] = value
    roberta_result = polarity_scores_roberta(text)
    both = {**vader_results_rename, **roberta_result}

    results[text] = both

results_df = pd.DataFrame(results).T
results_df = results_df.reset_index().rename(columns={'index': 'title'})

# Compare results across models

# TypeError: len() of a 0-d tensor
# sns.pairplot(data=results_df, vars=['vader_neg', 'vader_neu', 'vader_pos',
#                                     'roberta_neg', 'roberta_neutral', 'roberta_pos',
#                                     ])
# plt.show()


