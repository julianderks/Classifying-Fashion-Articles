## About

This directory holds all the scraped and model training data

## Usage

The [data directory](https://github.com/julianderks/Classifying-Fashion-Articles/tree/main/code/data/data) should contain the `zalando_articles_raw.csv` that holds all the scraped article data. The data can be preprocessed by running the following code from the current directory:

```bash
python preprocess.py
```

A new `zalando_articles_cleaned.csv` holding the preprocessed data is created in the data directory, associated preprocessed images which are used as input for the CNN are stored in the [image directory](https://github.com/julianderks/Classifying-Fashion-Articles/tree/main/code/data/data/img).
