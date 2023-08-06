import abc
import os
import typing as T
from time import time

import openai


class BaseAction(abc.ABC):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_key = openai_api_key

    messages = []

    @abc.abstractmethod
    def execute(self, input_text: str) -> str:
        pass

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 15:
            self.messages.pop(2)  # Remove the third item..aka leave fir

    def chat_completion(
        self,
        max_tokens: int = 1500,
        n: int = 1,
        temperature: float = 0.0,
        model: T.Union[str, None] = None,
    ):
        if not model:
            model = self.model

        if "gpt" in model:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=self.messages,
                    n=n,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            except openai.error.RateLimitError as e:
                print(str(e))
                print("Switching to GPT-4 model instead")
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=self.messages,
                    n=n,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except (openai.error.ServiceUnavailableError, openai.error.APIError):
                """wait 3 seconds and retry"""
                time.sleep(3)
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=self.messages,
                    n=n,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            if n > 1:
                from jprint import jprint

                print("Before")
                jprint(response)

                # we will have gpt analyzze each response and choose the beest one.
                messages = self.messages.copy()
                messages.append(
                    {
                        "role": "system",
                        "content": (
                            "Analyze the following responses and choose the best one based on prior instructions. "
                            "Alway's make a decision even if data is incomplete and respond with the exact text of the chosen response "
                            f"respnses={response['choices']}"
                        ),
                    }
                )
                for i, choice in enumerate(response["choices"]):
                    messages.append(
                        {"role": "assistant", "content": choice["message"]["content"]}
                    )

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    n=1,
                    messages=messages,
                    temperature=0.0,
                )

                from jprint import jprint

                jprint(response)
                print("The chosen resonse")

            if response:
                response = response["choices"][0]["message"]["content"].strip()
                self.add_message({"role": "assistant", "content": response})
                return response
            else:
                return ""

        else:
            text = "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])
            print("input text\n", text)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=text,
                temperature=0.6,
                max_tokens=max_tokens,
            )
            print("YOYOYOYOYOYOYOYOYOYOYO")

            if response:
                response_text = response["choices"][0]["text"].strip()

                # Clean up response
                response_text = response_text.replace("?\n", "")
                text = "\n".join(
                    line for line in response_text.splitlines() if line.strip()
                )

                # Remove ay leading things we don't want.
                text = text.replace("assistant:", "")
                text = text.replace("System:", "")
                text = text.replace("system:", "")

                if hasattr(self, "name"):
                    text = text.replace(f"{self.name}:", "")
                    text = text.replace(f"{self.name.title()}:", "")

                self.add_message({"role": "assistant", "content": text})
                print(f"text -{text}-")

                return text
            else:
                return ""
