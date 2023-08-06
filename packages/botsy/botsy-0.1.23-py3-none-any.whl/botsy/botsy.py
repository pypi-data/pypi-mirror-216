#!/usr/bin/env python
import asyncio
import contextlib
import os

import click
import pkg_resources

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import boto3
import openai
import pygame
import speech_recognition as sr
from colorama import Fore, init
from dotenv import load_dotenv

from actions import ActionClassifier, ActionRegistry, ConverseAction
from actions.classifier.build_classifier import _train as train_classifier
from actions.classifier.build_classifier import get_prediction as predict_classifier
from actions.stock_analysis.build_model import _train as train_stock_analysis
from actions.utils import listen_to_mic

init(
    autoreset=True
)  # This line is used to revert terminal color back to original after each print

polly_client = boto3.client("polly", region_name="us-west-2")

# Set the OpenAI API endpoint
openai.api_base = "https://api.openai.com/v1/"

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
if os.environ.get("DEBUG"):
    print(Fore.GREEN + "Environment Variables")
    for key in sorted(list(os.environ.keys())):
        print(f"{key}: {os.environ[key]}")

init(
    autoreset=True
)  # This line is used to revert terminal color back to original after each print


class Botsy:
    def __init__(self, name=1):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.name = name
        self.debug = False

        registry = ActionRegistry()
        print("Registered actions", registry.list_actions())

    def text_from_mic(
        self,
        non_speaking_duration=0.75,
        pause_threshold=1.5,
        phrase_time_limit=8,
    ):
        return listen_to_mic(
            non_speaking_duration=non_speaking_duration,
            pause_threshold=pause_threshold,
            phrase_time_limit=phrase_time_limit,
        )

    async def listen(self):
        ConverseAction.speak(f"{self.name} online.")

        while True:
            with contextlib.suppress(sr.UnknownValueError):
                text = self.text_from_mic()
                if text is not None:
                    text = text.lower()
                    text_to_classify = None

                    if text.endswith(self.name):
                        ConverseAction.speak("How may I help you?")
                        text_to_classify = self.text_from_mic()
                    elif text.startswith(self.name.lower()):
                        text_to_classify = text.lstrip(self.name.lower())
                    elif text.startswith(f"hey {self.name.lower()}"):
                        text_to_classify = text.lstrip(f"hey {self.name.lower()}")
                    elif text.startswith(f"hey, {self.name.lower()}"):
                        text_to_classify = text.lstrip(f"hey, {self.name.lower()}")

                    if text_to_classify is not None:
                        ActionClassifier.classify_action(text_to_classify)

    async def run(self):
        pygame.mixer.init()
        await self.listen()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--version", "-v", is_flag=True, help="Show Version and exit")
@click.option("--name", "-n", default="Botsy", help="Name of bot")
@click.option("--prompt", "-p", default="", help="Prompt for bot")
def cli(ctx, version, name, prompt):
    if version:
        bot_version = pkg_resources.get_distribution("botsy").version
        print(f"Botsy version: {bot_version}")
        return

    elif ctx.invoked_subcommand is None:
        ctx.invoke(run_bot, name=name, prompt=prompt)


@click.command()
@click.option("--name", "-n", default="Botsy", help="Name of bot")
@click.option("--prompt", "-p", default="", help="Prompt for bot")
def run_bot(name, prompt):
    bot_version = pkg_resources.get_distribution("botsy").version
    print(Fore.GREEN + f"Starting Botsy v{bot_version}")
    botsy = Botsy(name=name)

    if prompt:
        pygame.mixer.init()
        ActionClassifier.classify_action(prompt)
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(botsy.run())


@click.group()
def actions():
    """Commands related to actions"""
    pass


@actions.command()
def train():
    """Train the modes."""

    # Train the base classifier
    train_classifier()

    # Train other actions
    train_stock_analysis()


@actions.command()
@click.argument("text", nargs=-1)
def predict(text):
    """Predict the category of a text."""
    result = predict_classifier(text)
    click.echo(result)


# cli.add_command(run_bot)
cli.add_command(actions)

if __name__ == "__main__":
    cli()
