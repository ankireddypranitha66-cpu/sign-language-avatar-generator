import spacy

nlp = spacy.load("en_core_web_sm")

def to_gloss(sentence, drop_prepositions=True):
    doc = nlp(sentence)
    gloss_words = []

    for token in doc:
        # Drop determiners and auxiliary verbs
        if token.pos_ in ("DET", "AUX"):
            continue
        # Optionally drop prepositions
        if drop_prepositions and token.pos_ in ("ADP", "PART"):
            continue

        word = token.text.upper()

        # Strip "-ING" from verbs (simple approach: use base form via lemma)
        if token.pos_ == "VERB":
            word = token.lemma_.upper()

        gloss_words.append(word)

    return " ".join(gloss_words)

test_sentences = [
    "The dog is running in the park",
    "I want to eat pizza",
    "Can you help me please",
    "What is your name",
    "I love learning new things"
]

for sentence in test_sentences:
    print(f"English: {sentence}")
    print(f"Gloss:   {to_gloss(sentence)}")
    print()