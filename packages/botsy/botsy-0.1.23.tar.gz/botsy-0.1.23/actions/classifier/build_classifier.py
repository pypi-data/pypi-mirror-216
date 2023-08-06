#!/usr/bin/env python
import os
import warnings

import click
import openai
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from actions import ConverseAction, SearchWebAction, StockAnalyzeAction, WriteCodeAction

name = "actions_classifier.joblib"
models_dir = os.environ.get("MODELS_DIR", "/Users/jfurr/test_models")
model_name = os.path.join(models_dir, name)

available_actions = [
    ConverseAction,
    SearchWebAction,
    WriteCodeAction,
    StockAnalyzeAction,
]


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
    for action in available_actions:
        for td in action.training_data:
            training_data.append(td)
            training_labels.append(action.action_type)

    text_clf = Pipeline(
        [
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            ("clf", MultinomialNB()),
        ]
    )

    text_clf.fit(training_data, training_labels)

    directory = os.path.dirname(model_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("Saving...", model_name)
    dump(text_clf, model_name)


@click.command()
@click.argument("text", nargs=-1)
def predict(text):
    """Predict the category of a text."""
    print(get_prediction(text))


def get_prediction(text):
    try:
        text_clf = load(model_name)
    except Exception as e:
        warnings.warn("Model not found. Training model...")
        _train()
        text_clf = load(model_name)

    results = text_clf.predict(list(text))
    return results


@cli.command()
def new_data():
    """Add new data to the training data."""
    # TODO

    categories = [action.action_type for action in available_actions]
    categories = ", ".join(categories)
    prompt = (
        f"For each of these categories:  [ {categories} ] "
        "I'd like you to come up with 10 short english phrases, seperated by newlines that match each category. "
        "Please take your time and come up with good responses as this will be used for training data.  "
        "Lastly format your results like:\n"
        "[category] \n"
        "  [phrase]\n"
        "  [phrase]\n"
        "  ...     \n"
        "[category]\n"
        "  [phrase]\n"
        "  [phrase]\n"
        "  ...     \n"
    )
    messages = []
    messages.append(
        {
            "role": "system",
            "content": prompt,
        }
    )
    print(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        n=1,
        temperature=0.0,
        max_tokens=1000,
    )
    print(response.choices[0].message["content"])
    input()


cli.add_command(train)
cli.add_command(predict)
cli.add_command(new_data)

if __name__ == "__main__":
    cli()
