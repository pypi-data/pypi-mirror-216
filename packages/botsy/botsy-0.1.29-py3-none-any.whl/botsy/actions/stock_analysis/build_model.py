#!/usr/bin/env python
import io
import json
import os
import warnings
import zipfile

import click
import requests
from dotenv import load_dotenv
from joblib import dump, load
from jprint import jprint  # noqa
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

name = "ticker_classifier.joblib"
models_dir = os.environ.get("MODELS_DIR", "/Users/jfurr/test_models")
model_name = os.path.join(models_dir, name)


def download_and_extract_github_repo(repo_url, extract_to="."):
    """
    Download and extract github repository

    :param repo_url: Github repository URL
    :param extract_to: Location to extract
    :return: None
    """
    print(f"Fetching new stock data from: {repo_url}")
    # Change the repository url to the url of the zip file
    zip_url = (
        repo_url.replace("github.com", "codeload.github.com") + "/zip/refs/heads/main"
    )

    # Get the zip file
    response = requests.get(zip_url)
    z = zipfile.ZipFile(io.BytesIO(response.content))

    # Extract the zip file
    z.extractall(extract_to)

    print("Extract to...", extract_to)


@click.group()
def cli():
    pass


@click.command()
def train():
    """Train the model."""
    _train()


def _train():
    training_data = []
    training_labels = []

    dirname = os.path.dirname(__file__)
    # Usage
    download_and_extract_github_repo(
        "https://github.com/rreichel3/US-Stock-Symbols", dirname
    )
    for subdir in ["amex", "nasdaq", "nyse"]:
        path = os.path.join(
            dirname, "US-Stock-Symbols-main", subdir, f"{subdir}_full_tickers.json"
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
def get_prediction(text):
    _get_prediction(text)


def _get_prediction(text):
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


cli.add_command(train)
cli.add_command(get_prediction)

if __name__ == "__main__":
    cli()
