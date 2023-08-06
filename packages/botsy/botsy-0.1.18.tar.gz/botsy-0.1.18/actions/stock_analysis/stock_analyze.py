import json
import os
import shutil
import typing as T

import pytesseract
from bson import json_util
from dotenv import load_dotenv
from jprint import jprint  # noqa
from PIL import Image
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from actions.base_action import BaseAction
from actions.stock_analysis.build_model import get_prediction

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)


class StockAnalyzeAction(BaseAction):
    action_type = "stock analyze"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/training_data.txt") as f:
        training_data = f.read().splitlines()

    model = "gpt-3.5-turbo"
    api_key = os.environ.get("GOOGLE_CUSTOME_SEARCH_API_KEY")
    cse_id = os.environ.get("GOOGLE_CUSTOME_CSE_ID")

    def setup_mongo(self, collection: str) -> None:
        # Create a client
        user = os.environ.get("MONGO_USERNAME")
        password = os.environ.get("MONGO_PASSWORD")
        host = os.environ.get("MONGO_HOST")
        port = os.environ.get("MONGO_PORT")
        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")

        # Access a database
        self.db = self.client["stocks"]

        # Access a collection
        self.collection = self.db[collection]

    def get_ticker(self, input_text: str) -> str:
        """
        Use support vector machine to classify the input_text into a valid ticker
        """
        ticker = get_prediction([input_text])
        return ticker

    def execute(self, input_text: str) -> str:
        self.ticker = self.get_ticker(input_text)
        print("Analyzing Ticker: ", self.ticker)

        # TODO This seems sketchy to have this here
        self.setup_mongo(self.ticker)

        summaries = self.yahoo_stats(self.ticker)

        summaries = []
        report = self.final_report(summaries)

        self.collection.insert_one(
            {
                "ticker": self.ticker,
                "description": "Final Report",
                "formatted": [l for l in report.split("\n") if l],
            }
        )

        print(report)

    def final_report(self, summaries: str) -> str:
        # Find everything but the final report
        results = self.collection.find(
            {
                "ticker": self.ticker,
                "description": {"$ne": "Final Report"},
                "formatted": {"$exists": True},
            },
            {"_id": 0, "unformatted": 0, "url": 0, "ticker": 0},
        )

        json_docs = [json.loads(json_util.dumps(doc)) for doc in results]
        jprint(json_docs)
        # input()

        summaries = ""
        for doc in json_docs:
            formatted = "\n".join(doc.get("formatted", []))
            summaries += f"{doc['description']}\n{formatted}\n\n"

        prompt = (
            f"You are a stock analyst.  "
            f"Please analyze the following data for {self.ticker} and provide "
            f"a detailed report with ascii tables if helpful.  "
            "Make sure to give a final recommendation of Buy, Sell, or Hold."
            # f"Also provide an index.html version of your report."
            "Please review your work to ensure it's of high quality."
            f"\ndata=\n{summaries}"
        )
        print(prompt)
        print("Submitted... please hold")

        self.messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        try:
            # results = self.chat_completion(model="gpt-3.5-turbo", max_tokens=5000)
            results = self.chat_completion(model="gpt-4", max_tokens=5000)
        except Exception as e:
            print(f"Error: {e}")
            results = self.chat_completion(model="gpt-4")

        return results

    # def stock_analysis(self, ticker: str) -> str:
    #     # https://stockanalysis.com/stocks/tsla/company/

    def yahoo_stats(self, ticker: str) -> T.List[str]:
        # TODO You may not need the xpath any more
        pages: T.List[T.Tuple[str, str]] = [
            (
                "Income Statement",
                f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}",
            ),
            (
                "Balance Sheet",
                f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}",
            ),
            (
                "Cash Flow",
                f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}",
            ),
            (
                "Valuations and other Key Financial Metrics",
                f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}",
            ),
            (
                "Summary",
                f"https://finance.yahoo.com/quote/{ticker}?p={ticker}",
            ),
            (
                "Financials",
                f"https://stockanalysis.com/stocks/{ticker}/financials/",
            ),
        ]

        return self.extract_all_data(pages, ticker)

    def extract_all_data(
        self, pages: T.List[T.Tuple[str, str]], ticker: str
    ) -> T.List[str]:
        # Create directory 'ticker' if it doesn't exist
        if os.path.exists(f".images/{ticker}"):
            shutil.rmtree(f".images/{ticker}")
        os.makedirs(f".images/{ticker}")

        summaries = []
        for description, url in pages:
            data = self.extract_data(ticker, url, description)
            summaries.append({description: data})

        return summaries

    def extract_data(self, ticker, url, description):
        display_desc = description.replace(" ", "_")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
            executable_path="/Users/jfurr/botsy/botsy/chromedriver",
            options=chrome_options,
        )
        driver.get(url)

        # Increase the window size for capturing more content
        driver.set_window_size(1920, 2500)
        image_name = f".images/{ticker}/{ticker}_{display_desc}.png"
        driver.save_screenshot(image_name)

        driver.quit()

        image = Image.open(image_name)
        text = pytesseract.image_to_string(image)

        self.collection.update_one(
            {
                "ticker": ticker,
                "description": description,
            },
            {
                "$set": {
                    "url": url,
                    "unformatted": [l for l in text.split("\n") if l],
                }
            },
            upsert=True,
        )

        print(f"\n\n{description}")

        prompt = (
            f"Extract the {description} data for {ticker} and reformat into headers with ascii tables of equal width cells. "
            "Make sure to first remove data from any company not related to {ticker} "
            f"data={text}"
        )
        print(f"prompt length", len(prompt))
        prompt = prompt[:5000]

        self.messages = [{"role": "user", "content": prompt}]
        results = self.chat_completion(
            model="gpt-3.5-turbo",
            n=1,
            temperature=0.0,
        )

        print(results)

        self.collection.update_one(
            {"ticker": ticker, "description": description},
            {"$set": {"formatted": [l for l in results.split("\n") if l]}},
        )

        # Summarize interesting data
        prompt = f"Summarize the interesting data for {ticker} and {description} data={results}"
        self.messages = [{"role": "user", "content": prompt}]
        results = self.chat_completion(
            model="gpt-3.5-turbo",
            n=1,
            temperature=0.0,
        )
        results = "\n".join([results[i : i + 80] for i in range(0, len(results), 80)])
        print(results)

        self.collection.update_one(
            {"ticker": ticker, "description": description},
            {"$set": {"summary": [l for l in results.split(". ") if l]}},
        )
        print("Summary: ", results)
        return results
