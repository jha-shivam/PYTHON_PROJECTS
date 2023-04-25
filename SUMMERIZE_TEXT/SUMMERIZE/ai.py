import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# Load the English language model for sp

nlp = spacy.load('en_core_web_lg')

# Define a function to summarize text
def summarize(text):
    # Parse the text using spaCy
    doc = nlp(text)

    # Remove stop words and punctuation
    sentences = [sent for sent in doc.sents]
    clean_sentences = []
    for sent in sentences:
        words = [
            token.text for token in sent if not token.is_stop and not token.is_punct]
        clean_sentences.append(' '.join(words))

    # Calculate the importance of each sentence
    sentence_scores = {}
    for sent in clean_sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            # only consider entities that are people or organizations
            if ent.label_ == 'PERSON' or ent.label_ == 'ORG':
                sentence_scores[sent] = sentence_scores.get(sent, 0) + 1
        for token in doc:
            if token.pos_ == 'VERB' or token.pos_ == 'NOUN':  # only consider verbs and nouns
                sentence_scores[sent] = sentence_scores.get(sent, 0) + 1

    # Sort the sentences by importance and select the top 3
    summary_sentences = sorted(
        sentence_scores, key=sentence_scores.get, reverse=True)[:3]

    # Return the summary as a string
    summary = ' '.join(summary_sentences)
    return summary


text = "The COVID-19 pandemic has had a significant impact on the global economy, with many businesses forced to " \
       "close or reduce their operations. Governments around the world have implemented various measures to mitigate " \
       "the economic impact, including stimulus packages, tax relief, and loan guarantees. However, the effectiveness " \
       "of these measures has been limited by the duration and severity of the pandemic, as well as by other factors " \
       "such as the availability of vaccines and the effectiveness of public health measures. Despite these " \
       "challenges, there are signs of economic recovery in some regions, with industries such as technology, " \
       "healthcare, and e-commerce experiencing growth. The long-term economic impact of the pandemic remains " \
       "uncertain, but it is clear that businesses will need to adapt and innovate in order to survive and thrive in " \
       "the post-pandemic world."
summary = summarize(text)
print(summary)
