# rkarim

Hi!

Contents of this README:

- Problem Statement
- Project Structure
- Data Collection
- Downloading Libraries
- Running
- Notes

## Project Structure

```bash
├── README.md
├── requirements.txt
├── files
│   ├── deu
│   ├── eng
│   ├── fra
│   ├── deu.tsv
│   ├── eng.tsv
│   ├── fra.tsv
│   ├── metadata_deu.tsv
│   ├── metadata_eng.tsv
│   └── metadata_fra.tsv
│   ├── deu_clusters_pca.png
│   ├── eng_clusters_pca.png
│   ├── fra_clusters_pca.png
└── src
    ├── __init__.py
    ├── cluster.py
    ├── download_articles.py
    └── summary.py
```

To follow through this README, it is required that you be in the main project directory. You can also preview this README as a markup (recommended).

## Problem Statement

To group documents from a specified language.

## Data Collection

We retrieved data from EventRegistry.org using an API. 20 news articles from English, German and French were downloaded at random - this totals to 60 articles. The code can be found in `src/download_articles.py` and the data can be found in the `data` folder. There is no need to run anything on these files for pre-processing.

You can however find the metadata in the `file/metadata.tsv` file. The first column is the language of the article, the second column is the title of the article. The `file/metadata_<language>.tsv` file is just a breakdown of the metadata.tsv file, into the 3 different languages.

## Downloading Libraries

We used **spaCy** for NLP. We download the English, German and French models.
These models are general-purpose models trained for vocabulary, syntax and entities.

```bash
pip install spacy
python -m spacy download en
python -m spacy download de
python -m spacy download fr
```

We also used the **langdetect** library for detection of language in a document

```bash
pip install langdetect
```

For vectorising the tokens, we have used the **TfidfVectorizer** class from **sklearn**. The clustering of documents is done by **KMeans** from the same module.

```bash
pip install sklearn
```

The rest of the modules are standard Python modules.

## Running

### Summary

To get a summary from a randomly chosen article from the 60 articles, simply run

```bash
python -m src.summary
```

```bash
python -m src.summary
    --lang [eng,deu,fra]
    --article [0-19]
    --verbosity [0,1]
```

Run `python -m src.summary --help` for help.

### Vectorising and Clustering

```bash
python -m src.cluster
    --lang [eng,deu,fra]
    --num_clusters [no. of kmeans clusters]
```

Run `python -m src.cluster --help` for help.

## Notes

### Preprocessing

- We used the stop words that are provided by spaCy.
- We did not use regex to obtain the phone number but used logical rules instead (src/summary.py line 72). But even then, the rules we set are for numbers in Singapore. So it wouldn't work most of the time. Sorry!
- When removing irrelevant words, we also removed contractions, and numbers (src/summary.py line 102).

### Vectorising and Clustering

We used TF-IDF to vectorise the tokens. We then cluster these features using k-means clustering algorithm. The reason for this usage is that since clustering is a subjective matter, we leave it to the user to be able to define the number of clusters depending on what he/she is looking for.

We have also used PCA to visualise the documents. We made use of the feature vectors from TF-IDF and loaded the data (with the metadata) to https://projector.tensorflow.org. What this does is it takes the first 3 principal components, and project these into a 3D graph. You can see these visualisations in the `files` folder.
