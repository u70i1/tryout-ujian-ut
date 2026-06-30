import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python scrape.py <url>")
    sys.exit()

req = requests.get(sys.argv[1])
doc = req.text
soup = BeautifulSoup(doc, "html.parser")

cards = soup.find_all("div", class_="question-card")

for idx, card in enumerate(cards):
    correct = card.get("data-correct")
    question = card.find("p", class_="question-text").get_text()
    options = card.find_all("li", class_="option-item")
    correct_explanation = card.find("span", class_="answer-reason")

    print(f"{idx+1}. {question}")
    for option in options:
        print(option.get_text())
    print()

