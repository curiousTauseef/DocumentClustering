"""
Download articles from eventregistry.org using an API
"""

from eventregistry import QueryArticlesIter, EventRegistry

LANGUAGES = ["deu", "fra", "eng"]
NUM_ARTICLES = 20
APIKEY= None
er = EventRegistry(apiKey=APIKEY)

for lang in LANGUAGES:
    print("Downloading articles for {}".format(lang))
    query = QueryArticlesIter(lang=lang)
    articles = query.execQuery(er, sortBy="date", maxItems=NUM_ARTICLES)

    with open("files/metadata_{}.tsv".format(lang), 'w') as file:
        for i, article in enumerate(articles):
            with open("files/{}/article_{}.txt".format(lang, i), "w") as f:
                f.write(article["title"] + "\n" + article["body"])
                file.write("{}\n".format(article["title"]))
