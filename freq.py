import csv
import re
import traceback
import os
from collections import Counter
import spacy

data_dir = './data'
spacy.require_gpu()
nlp = spacy.load("ru_core_news_lg")
the_great_counter = Counter()
total_files = len(os.listdir(data_dir))
i = 0

for file in os.listdir(data_dir):
    i = i + 1
    with open(f'{data_dir}/{file}', 'r') as opened_file:        
        progress = int((i * 100) / total_files)
        print(f"Progress: {progress}%")
        print(f"Loading {opened_file.name}...")
        try:
            txt = opened_file.read()
            print("Sanitizing...")
            # keep only russian characters and hyphens
            c01 = re.sub(r"[\\\/()]", " ", txt)
            # keep only russian characters and hyphens
            c1 = re.sub(r"[^\u0400-\u04FF\-\s]+", " ", c01)
            # replace multiple hyphens to single hyhpens
            c2 = re.sub(r"[\-]{2,}", "-", c1)
            # remove hyphens which appear in the begging of words
            c3 = re.sub(r"([^\u0400-\u04FF])\-([\u0400-\u04FF])", "\g<1> \g<2>", c2)
            # remove hyphens which appear in the end of words
            c4 = re.sub(r"([\u0400-\u04FF])\-([^\u0400-\u04FF])", "\g<1> \g<2>", c3)
            c5 = re.sub("\n", " ", c4)
            # reducing multiple spaces to single spaces
            clean_text = re.sub(r"[\s]{2,}", " ", c5)
            print("Running NLP...")
            # Let spaCy do its magic
            doc = nlp(clean_text)
            # all tokens that arent stop words or punctuations
            print("Counting...")
            words = [(token.lemma_, token.pos_)
                    for token in doc
                    if not token.is_stop and not token.is_punct and not token.is_space]
            word_cnt = Counter(words)
            the_great_counter.update(word_cnt)
        except Exception as err:
            print(f"Skipping {opened_file.name} due to {err}")
            print(traceback.format_exc())

print("Sorting...")
sorted_freqs = the_great_counter.most_common(25000)
print("Writing result...")
with open('freq.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    for key, count in sorted_freqs:
        lemma, pos = key
        csv_writer.writerow([lemma, pos, count])