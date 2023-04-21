import json
from textblob import TextBlob
from collections import Counter

# Ouvrir le fichier JSON contenant les commentaires
with open('C:/Users/Sibylle Mathieu/Desktop/ESME/Projet Big Data/video_details.json','r') as f:
    data = json.load(f)

# Récupérer les commentaires
comments = []
for comment in data:
    comments.append(comment['text'])


# Concaténer tous les commentaires en un seul texte
text = " ".join(comments)

# Analyser les mots clés
analysis = TextBlob(text)
noun_phrases = analysis.noun_phrases
top_noun_phrases = Counter(noun_phrases).most_common(10)

# Afficher les mots clés les plus fréquents
print("Mots clés :")
for np, count in top_noun_phrases:
    print(f"{np} ({count} occurrences)")
