#!/usr/bin/env python
import json
import os
import warnings

import click
from dotenv import load_dotenv
from joblib import dump, load
from jprint import jprint  # noqa
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

dotenv_path = os.path.join(os.getcwd(), ".env")
print("dotenv_path", dotenv_path)
load_dotenv(dotenv_path)

print(os.environ)

model_name = os.path.join(
    os.environ.get("PROJECT_ROOT"), os.environ.get("TICKER_CLASSIFIER")
)


@click.group()
def cli():
    pass


@click.command()
def _train():
    """Train the model."""
    train()


def train():
    training_data = []
    training_labels = []

    dirname = os.path.dirname(__file__)
    for subdir in ["amex", "nasdaq", "nyse"]:
        path = os.path.join(
            dirname, "US-Stock-Symbols", subdir, f"{subdir}_full_tickers.json"
        )
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)

                for ticker in data:
                    training_data.append(ticker["symbol"])
                    training_labels.append(ticker["symbol"])

                    training_data.append(ticker["name"])
                    training_labels.append(ticker["symbol"])

    text_clf = Pipeline(
        [
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            ("clf", MultinomialNB()),
        ]
    )

    # Train the model
    text_clf.fit(training_data, training_labels)

    # Save the model
    dump(text_clf, model_name)


@click.command()
@click.argument("text", nargs=-1)
def _get_prediction(text):
    get_prediction(text)


def get_prediction(text):
    """Predict the category of a text."""
    try:
        print("Loading", model_name)
        text_clf = load(model_name)
    except Exception as e:
        warnings.warn("Model not found. Training model...")
        train()
        text_clf = load(model_name)

    # Classify new text
    results = text_clf.predict(list(text))
    if results:
        return results[0]


cli.add_command(_train)
cli.add_command(_get_prediction)

if __name__ == "__main__":
    cli()
