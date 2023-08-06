[![PyPI - Python](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8-blue.svg)](https://pypi.org/project/keystem/)
[![PyPI - License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/MaartenGr/keybert/blob/master/LICENSE)
[![PyPI - PyPi](https://img.shields.io/pypi/v/keyBERT)](https://pypi.org/project/keystem/)
<!-- [![Build](https://img.shields.io/github/actions/workflow/status/MaartenGr/keyBERT/testing.yml?branch=master)](https://pypi.org/keystem/) -->
<!-- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OxpgwKqSzODtO3vS7Xe1nEmZMCAIMckX?usp=sharing) -->

<img src="images/logo.png" width="35%" height="35%" align="right" />

# KeyStem

KeyStem is a minimal and easy-to-use keyword extraction technique that leverages BERT embeddings to
create keywords and keyphrases that are most similar to a document.

Corresponding medium post can be found [here](https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea).

<a name="toc"/></a>
## Table of Contents  
<!--ts-->  
   1. [About the Project](#about)  
   2. [Getting Started](#gettingstarted)  
        2.1. [Installation](#installation)  
        2.2. [Basic Usage](#usage)  
        2.3. [Max Sum Distance](#maxsum)  
        2.4. [Maximal Marginal Relevance](#maximal)  
        2.5. [Embedding Models](#embeddings)  
<!--te-->  


<a name="about"/></a>
## 1. About the Project
[Back to ToC](#toc)

Although there are already many methods available for keyword generation
(e.g.,
[Rake](https://github.com/aneesha/RAKE),
[YAKE!](https://github.com/LIAAD/yake), TF-IDF, etc.)
I wanted to create a very basic, but powerful method for extracting keywords and keyphrases.
This is where **KeyStem** comes in! Which uses BERT-embeddings and simple cosine similarity
to find the sub-phrases in a document that are the most similar to the document itself.

First, document embeddings are extracted with BERT to get a document-level representation.
Then, word embeddings are extracted for N-gram words/phrases. Finally, we use cosine similarity
to find the words/phrases that are the most similar to the document. The most similar words could
then be identified as the words that best describe the entire document.

KeyStem is by no means unique and is created as a quick and easy method
for creating keywords and keyphrases. Although there are many great
papers and solutions out there that use BERT-embeddings
(e.g.,
[1](https://github.com/pranav-ust/BERT-keyphrase-extraction),
[2](https://github.com/ibatra/BERT-Keyword-Extractor),
[3](https://www.preprints.org/manuscript/201908.0073/download/final_file),
), I could not find a BERT-based solution that did not have to be trained from scratch and
could be used for beginners (**correct me if I'm wrong!**).
Thus, the goal was a `pip install keystem` and at most 3 lines of code in usage.

<a name="gettingstarted"/></a>
## 2. Getting Started
[Back to ToC](#toc)

<a name="installation"/></a>
###  2.1. Installation
Installation can be done using [pypi](https://pypi.org/project/keystem/):

```
pip install keystem
```


<a name="usage"/></a>
###  2.2. Usage

The most minimal example can be seen below for the extraction of keywords:
```python
from keystem import KeyStem

doc = """
         Supervised learning is the machine learning task of learning a function that
         maps an input to an output based on example input-output pairs. It infers a
         function from labeled training data consisting of a set of training examples.
         In supervised learning, each example is a pair consisting of an input object
         (typically a vector) and a desired output value (also called the supervisory signal).
         A supervised learning algorithm analyzes the training data and produces an inferred function,
         which can be used for mapping new examples. An optimal scenario will allow for the
         algorithm to correctly determine the class labels for unseen instances. This requires
         the learning algorithm to generalize from the training data to unseen situations in a
         'reasonable' way (see inductive bias).
      """
ks_model = KeyStem()
keywords = ks_model.get_keygroups(doc)
```

You can set `keyphrase_ngram_range` to set the length of the resulting keywords/keyphrases:

```python
>>> ks_model.get_keygroups(doc, keyphrase_ngram_range=(1, 1), stop_words=None)

{'index': {0: 0, 2: 1, 26: 15, 28: 16, 20: 11}, 'keywords': {0: ('supervised learning', 0.7096), 2: ('supervised', 0.6735), 26: ('supervised learning', 0.613), 28: ('supervised', 0.6125), 20: ('supervised', 0.5554)}, 'features': {0: 'supervised learning', 2: 'supervised', 26: 'supervised learning', 28: 'supervised', 20: 'supervised'}, 'cluster': {0: 0.0, 2: 0.0, 26: 0.0, 28: 0.0, 20: 0.0}, 'score': {0: 0.7096, 2: 0.6735, 26: 0.613, 28: 0.6125, 20: 0.5554}, 'label': {0: 'supervised learning', 2: 'supervised learning', 26: 'supervised learning', 28: 'supervised learning', 20: 'supervised learning'}
```

To extract keyphrases, simply set `keyphrase_ngram_range` to (1, 2) or higher depending on the number
of words you would like in the resulting keyphrases:

```python
>>> kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words=None)

{'index': {0: 0, 2: 1, 26: 15, 28: 16, 20: 11}, 'keywords': {0: ('supervised learning', 0.7096), 2: ('supervised', 0.6735), 26: ('supervised learning', 0.613), 28: ('supervised', 0.6125), 20: ('supervised', 0.5554)}, 'features': {0: 'supervised learning', 2: 'supervised', 26: 'supervised learning', 28: 'supervised', 20: 'supervised'}, 'cluster': {0: 0.0, 2: 0.0, 26: 0.0, 28: 0.0, 20: 0.0}, 'score': {0: 0.7096, 2: 0.6735, 26: 0.613, 28: 0.6125, 20: 0.5554}, 'label': {0: 'supervised learning', 2: 'supervised learning', 26: 'supervised learning', 28: 'supervised learning', 20: 'supervised learning'}
```

<a name="maximal"/></a>
###  2.4. Maximal Marginal Relevance

To diversify the results, we can use Maximal Margin Relevance (MMR) to create
keywords / keyphrases which is also based on cosine similarity. The results
with **high diversity**:


The results with **low diversity**:



<a name="embeddings"/></a>
###  2.5. Embedding Models
KeyBERT supports many embedding models that can be used to embed the documents and words:

* Sentence-Transformers
* Flair
* Spacy
* Gensim
* USE

Click [here](https://maartengr.github.io/KeyBERT/guides/embeddings.html) for a full overview of all supported embedding models.

**Sentence-Transformers**  
You can select any model from `sentence-transformers` [here](https://www.sbert.net/docs/pretrained_models.html)
and pass it through KeyStem with `model`:

```python
from keystem import KeyStem
kw_model = KeyStem(model='all-MiniLM-L6-v2')
```

Or select a SentenceTransformer model with your own parameters:

```python
from keystem import KeyStem
from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyStem(model=sentence_model)
```

**Flair**  
[Flair](https://github.com/flairNLP/flair) allows you to choose almost any embedding model that
is publicly available. Flair can be used as follows:

```python
from keystem import KeyStem
from flair.embeddings import TransformerDocumentEmbeddings

roberta = TransformerDocumentEmbeddings('roberta-base')
ks_model = KeyStem(model=roberta)
```

You can select any 🤗 transformers model [here](https://huggingface.co/models).


## Citation
To cite KeyStem in your work, please use the following bibtex reference:

```bibtex
@misc{grootendorst2020keybert,
  author       = {Naga Kiran},
  title        = {KeyStem: Minimal keyword extraction with BERT and grouping to the stem of key.},
  year         = 2023,
  publisher    = {caspai},
  version      = {v0.0.1},
  url          = {http://caspai.in/}
}
```

## References
Below, you can find several resources that were used for the creation of KeyStem
but most importantly, these are amazing resources for creating impressive keyword extraction models:


**Github Repos**:
* https://github.com/MaartenGr/KeyBERT
* https://github.com/Nagakiran1/keystem
* https://github.com/thunlp/BERT-KPE
* https://github.com/ibatra/BERT-Keyword-Extractor
* https://github.com/pranav-ust/BERT-keyphrase-extraction
* https://github.com/swisscom/ai-research-keyphrase-extraction

**MMR**:
The selection of keywords/keyphrases was modeled after:
* https://github.com/swisscom/ai-research-keyphrase-extraction

