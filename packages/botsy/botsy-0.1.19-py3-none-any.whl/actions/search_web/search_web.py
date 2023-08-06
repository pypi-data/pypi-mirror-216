import nltk
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from newspaper import Article

from actions.base_action import BaseAction


class SearchWebAction(BaseAction):
    action_type = "search web"
    training_data = [
        "Find a recipe for spaghetti bolognese.",
        "Search for the latest news about cryptocurrency.",
        "Who won the NBA finals last year?",
        "Find the nearest pizza restaurant.",
        "Look up the release date for the new Star Wars movie.",
        "Search for the highest mountain in the world.",
        "Who is the current President of the United States?",
        "Find me a good horror movie to watch.",
        "Search for popular holiday destinations in Europe.",
        "Find the lyrics for the song 'Imagine'.",
        "Summarize Recent",
        "Recent News",
        "Get recent news",
    ]
    model = "gpt-3.5-turbo"
    # Set up the Google Custom Search API
    api_key = "AIzaSyCpTeL7j4XSawmgcZHQw0WpwEBlMeXutfY"
    cse_id = "428c174c922a94b87"

    def generate_overview(self, summary_text: str) -> str:
        prompt = f"You are a researcher tasked with investigating the following summaries.  Please correct the best summary and modify as you see fit. : {summary_text}"
        self.messages.append({"role": "user", "content": prompt})
        return self.chat_completion(model="gpt-3.5-turbo")

    def generate_google_search_query(self, query: str) -> list:
        prompt = f"rephrase the statement as a google search query: {query}"
        self.messages.append({"role": "user", "content": prompt})
        return self.chat_completion(model="text-davinci-003")

    def execute(self, input_text: str, rephrase_as_google=True) -> str:
        nltk.download("punkt")
        from actions import ConverseAction

        if rephrase_as_google:
            input_text = self.generate_google_search_query(input_text)

        ConverseAction.speak(
            f"Searching the web for the following query: {input_text}."
        )

        query = input_text
        num_results = 10
        summary = ""

        service = build("customsearch", "v1", developerKey=self.api_key)

        # Search the web using the Google Custom Search API
        try:
            result = (
                service.cse().list(q=query, cx=self.cse_id, num=num_results).execute()
            )
        except HttpError as e:
            print(f"Error during API call: {e}")
            return None

        items = result.get("items", [])

        # Extract and summarize the articles
        for item in items:
            try:
                url = item["link"]
                print(f"\n\nProcessing article: {url}")
                article = Article(url)
                article.download()
                article.parse()

                # Check if the article content exists before performing NLP
                if article.text:
                    article.nlp()
                    print(article.summary)
                    summary += f"\n\n{article.title}\n{article.summary}"
                else:
                    print(f"Error processing article: {url}\nEmpty article content")
            except Exception as e:
                print(f"Error processing article: {url}\n{e}")

        # Speak the summarized results
        overview = self.generate_overview(summary)
        print("---------------- overview ----------------")
        print(overview)
        ConverseAction.speak(overview)
        return summary
