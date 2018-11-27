"""
Processing the text
"""

import argparse
import random

import spacy
from langdetect import detect

# Pipelines
# - Determining the language
# - Using pattern matching, find phone numbers
# - Part of speech tagging
# - Removing irrelevant words
# - Shrink the vector space of words
# - Cluster documents into logical groups
# - Produce a basic analysis of the result


# Debug
# text = "Bitte rufen Sie Anna bei den Nummern 88764323 oder 6457 8874 an, ob du Zeit hast."
# text = """Singapore (/ˈsɪŋ(ɡ)əpɔːr/ (About this sound listen)), officially the Republic of Singapore, is a sovereign city-state and island country in Southeast Asia. It lies one degree (137 kilometres or 85 miles) north of the equator, at the southern tip of the Malay Peninsula, with Indonesia's Riau Islands to the south and Peninsular Malaysia to the north. Singapore's territory consists of one main island along with 62 other islets. Since independence, extensive land reclamation has increased its total size by 23% (130 square kilometres or 50 square miles). The country is known for its transition from third world to first world in a single generation, under the leadership of its founding father, Lee Kuan Yew.
# Stamford Raffles founded colonial Singapore in 1819 as a trading post of the British East India Company. After the company's collapse in 1858, the islands were ceded to the British Raj as a crown colony. During the Second World War, Singapore was occupied by Japan :( It gained independence from the UK in 1963 with other former British territories to form the Federation of Malaya, but separated two years later over ideological differences, becoming a sovereign nation in 1965. After early years of turbulence and despite lacking natural resources and a hinterland, the nation developed rapidly as an Asian Tiger economy (define what an Asian Tiger economy means and who are the other 3 Asian Tigers), based on external trade and its workforce.
# Singapore is a global hub for finance, trade, transport,[10][11] education,[12][13] healthcare,[14] human capital,[15] innovation,[16] logistics,[17] manufacturing,[18] technology,[19] and tourism.[20] The city ranks highly in numerous international rankings, and has been recognized as the most "technology-ready" nation (WEF), top International-meetings city (UIA),[21][22] city with "best investment potential" (BERI), world's smartest city,[23] world's safest country,[24][25] third-most competitive country, third-largest foreign exchange market, third-largest financial centre, third-largest oil refining and trading centre, fourth-healthiest country,[26] fifth-most innovative country, and the second-busiest container port.[27] The country has also been identified as a tax haven. In 2018, the Economist Intelligence Unit (EIU) ranked Singapore for the fifth year in a row as the most expensive city to live in the world.[28] Singapore is the only country in Asia with an AAA sovereign rating from all major rating agencies, and one of only a few countries worldwide. Globally, the Port of Singapore and Changi Airport have held the titles of leading "Maritime Capital" and "Best Airport" respectively for consecutive years, while its national airline Singapore Airlines is the 2018 "World's Best Airline".
# Singapore ranks 5th on the UN Human Development Index with the 3rd highest GDP per capita. It is placed highly in key social indicators: education, healthcare, life expectancy, quality of life, personal safety and housing. As of 1 July 2018, Singaporean citizens had visa-free or visa-on-arrival access to 188 countries and territories, ranking the Singapore passport joint second in the world with Germany for lack of visa restrictions.[31] Although income inequality is high, 90% of homes are owner-occupied. 39% of Singapore's 5.6 million residents are not citizens. There are four official languages: English (common and first language), Malay, Mandarin Chinese and Tamil; almost all Singaporeans are bilingual.
# Singapore is a unitary multiparty parliamentary republic with a Westminster system of unicameral parliamentary government. The People's Action Party (PAP) has won every election since self-governmence in 1959. The dominance of the PAP, coupled with a low level of press freedom and restrictions on civil liberties and political rights, has led to Singapore being classified by the Economist Intelligence Unit as a flawed democracy. (sad :( ) As one of the five founding members of the Association of South-East Asian Nations (ASEAN), Singapore is the host of the Asia-Pacific Economic Cooperation (APEC) Secretariat, as well as many international conferences and events. It is also a member of the East Asia Summit, Non-Aligned Movement and the Commonwealth of Nations.
# The English name of Singapore is an anglicisation of the native Malay name for the country, Singapura, which was in turn derived from Sanskrit[33] (सिंहपुर, IAST: Siṃhapura; siṃha is "lion", pura is "town" or "city"), hence the customary reference to the nation as the Lion City, and its inclusion in many of the nation's symbols (e.g., its coat of arms, Merlion emblem). However, it is unlikely that lions ever lived on the island; Sang Nila Utama, the Srivijayan prince said to have founded and named the island Singapura, perhaps saw a Malayan tiger. There are however other suggestions for the origin of the name and scholars do not believe that the origin of the name is firmly established.[34][35] The central island has also been called Pulau Ujong as far back as the third century CE, literally "island at the end" (of the Malay Peninsula) in Malay.
# Singapore is also referred to as the Garden City for its tree-lined streets and greening efforts since independence,[38][39] and the Little Red Dot for how the island-nation is depicted on many maps of the world and Asia, as a red dot.[40][41][42] Also referred to as the "Switzerland of Asia" in 2017 due to its neutrality on international and regional issues.
# Good effort despite some rooms for improvements.
# 21/25
# """

NUM_ARTICLES = 20
LANGUAGES = ["deu", "fra", "eng"]


def get_vector(debug=False, text=None, sprache=None, article=None, verbosity=None):

    if debug:
        if sprache is None:
            sprache = random.choice(LANGUAGES)
        if article is None:
            article = random.choice(range(NUM_ARTICLES))
        with open('files/{}/article_{}.txt'.format(sprache, article), 'r') as f:
            text = f.read()

    # Determining the language
    lang = detect(text)
    if lang == 'en':
        nlp = spacy.load('en')
        lang_ = 'English'
        from spacy.lang.en.stop_words import STOP_WORDS
    elif lang == 'de':
        nlp = spacy.load('de')
        lang_ = 'German'
        from spacy.lang.de.stop_words import STOP_WORDS
    elif lang == 'fr':
        nlp = spacy.load('fr')
        lang_ = 'French'
        from spacy.lang.fr.stop_words import STOP_WORDS
    else:
        FileNotFoundError(
            'Language ({}) detected is not supported.'.format(lang))

    # Remove spaces
    text = text.strip().replace("\n", " ").replace("\r", " ").replace(
        "a.m.", "am").replace("p.m.", "pm").replace(".\"", ". \"")

    # Parse the text with spaCy.
    doc = nlp(text)

    # Using pattern matching, find phone numbers
    # If phone numbers are not separated by a space
    mobile_numbers_simple = [token.text
                             for token in doc
                             if token.like_num and len(token) == 8]
    # If phone numbers are separated by a space
    mobile_numbers_sep = [token.text + doc[idx-1].text
                          for idx, token in enumerate(doc)
                          if (token.like_num and len(token) == 4) and (doc[idx-1].like_num and len(doc[idx-1]) == 4) and idx != 0]
    mobile_numbers = mobile_numbers_simple + mobile_numbers_sep

    # Part of speech tagging
    proper_nouns = [token.text for token in doc if token.pos_ == 'PROPN']
    proper_nouns = list(set(proper_nouns))

    # Removing irrelevant words
    # Set stop words
    for w in STOP_WORDS:
        nlp.vocab[w].is_stop = True
    important_tokens = [
        token
        for token in doc
        if not token.text.lower() in STOP_WORDS and
        not token.is_punct and
        not token.is_space and
        token.pos_ not in ['ADP', 'SYM', 'NUM'] and
        token.text not in ["'s", "n't", "'m", "'d", "'ll"] and
        token.text not in ["|"]
    ]

    # Shrink the vector space of words
    lemmatized = [
        token.lemma_
        for token in doc
        if not token.like_num and
        token in important_tokens
    ]

    if debug:

        if verbosity == 1:
            summary = """
Article: files/{}/article_{}.txt

Language: {}

Phone numbers: {}

Proper nouns: {}

Important words: {}

Lemmatized words: {}
""".format(sprache, article, lang_, mobile_numbers, proper_nouns, important_tokens, lemmatized)

        else:
            summary = """
Article: files/{}/article_{}.txt

Language: {}

Proper nouns: {}
""".format(sprache, article, lang_, proper_nouns)

        print(summary)

    else:
        return lemmatized


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates summary of an article.')
    parser.add_argument('--lang',
                        type=str,
                        help='Language of article. One of eng, deu, fra. If none chosen, a language will be picked at random.')
    parser.add_argument('--article',
                        type=int,
                        help='Pick an article number from 0 to 19 inclusive. If no number specified, a random article will be picked.')
    parser.add_argument('--verbosity',
                        type=int,
                        default=0,
                        help='0 for the requirement of this assignment (displays language and proper noun). 1 to print entire summary. Defaults to 0.')
    args = parser.parse_args()
    get_vector(
        debug=True,
        sprache=args.lang,
        article=args.article,
        verbosity=args.verbosity
    )
