import os

import openai
from dotenv import load_dotenv

from actions.converse import ConverseAction
from actions.search_web import SearchWebAction
from actions.stock_analysis.stock_analyze import StockAnalyzeAction
from actions.write_code import WriteCodeAction

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


class ActionClassifier:
    actions = {
        ConverseAction.action_type: ConverseAction(),  # This gets reinitialized with name=Botsy
        SearchWebAction.action_type: SearchWebAction(),
        WriteCodeAction.action_type: WriteCodeAction(),
        StockAnalyzeAction.action_type: StockAnalyzeAction(),
    }

    action_types = list(actions.keys())

    @classmethod
    def classify_action(self, input_text: str) -> str:
        # TODO Fix this.
        from actions.classifier.build_classifier import get_prediction

        # Check if we are using the SVM classifier or GPT-3.5
        use_svm: bool = os.environ.get("SVM_ACTIONS_CLASSIFIER", "").lower() in [
            "true",
            "yes",
            "1",
        ]

        if use_svm:
            action = get_prediction([input_text])[0]
            print(f"SVM classifier.  action:={action}")
            self.actions[action].execute(input_text)
            return action.lower()
        else:
            # classify using GPT-3.5
            messages = [
                {
                    "role": "system",
                    "content": ". ".join(
                        [
                            f"You are an AI that classifies user inputs into available actions: {','.join(self.action_types)}"
                        ]
                    ),
                },
                {
                    "role": "user",
                    "content": ". ".join(
                        [
                            f"You are ONLY allowed to responsd with one of the following options: {','.join(self.action_types)}",
                            f"Pleaes classify the following input: {input_text}",
                        ]
                    ),
                },
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=20,
                    n=1,
                    temperature=0.0,
                )

                action = response.choices[0].message["content"].strip().lower()

                if action not in self.action_types:
                    print(f"Invalid action: {action}")
                    input()
                else:
                    self.actions[action].execute(input_text)

                return action.lower()

            except openai.error.InvalidRequestError as e:
                print(f"Error: {str(e)}")
                return None
