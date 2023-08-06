from actions.base_action import BaseAction


class WriteCodeAction(BaseAction):
    action_type = "write code"
    training_data = [
        "Can you help me write a function in Python?",
        "Show me how to declare a variable in JavaScript.",
        "Write a SQL query to select all records from a table.",
        "Write a simple Hello World program in Java.",
        "Help me code a quicksort algorithm.",
        "Show me how to use a for loop in Python.",
        "Can you write a recursive function to compute factorial?",
        "How do I define a class in C++?",
        "Write a Python script to read a CSV file.",
        "Help me code a binary search algorithm in Java.",
    ]

    def execute(self, input_text: str) -> str:
        print("write_code execute")
        # Implement the logic for the "write code" action
        from actions import ConverseAction

        response = ConverseAction().execute(
            input_text + ".  Please only show the python code without explanation",
            single_shot=True,
        )
        print(response)
        response = response.replace("\n", "")
        response = response.replace("`", "")
        response = response.replace("'", "")

        ans = eval(response)
        print("The answer is", ans)
