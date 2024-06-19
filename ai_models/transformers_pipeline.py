from transformers import pipeline

sent_pipeline = pipeline("sentiment-analysis")

print(sent_pipeline("Canada to launch inquiry into missing, murdered Aboriginal women | Daily Sabah"))
