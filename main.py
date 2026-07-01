import requests
import re
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/{slug}")
def scrape(slug: str):
    url = f"https://soalut.com/{slug}/"
    req = requests.get(url)

    document = req.text
    soup = BeautifulSoup(document, "html.parser")

    cards = soup.find_all("div", class_="question-card")

    all_questions = []

    for card in cards:
        correct = card.get("data-correct")
        question = card.find("p", class_="question-text").get_text()
        options = card.find_all("li", class_="option-item")
        explanation_tag = card.find("span", class_="answer-reason")

        # sometimes there's no explanation for the answer
        answer_explanation = explanation_tag.get_text() if explanation_tag else None

        question = {
            "questionText": question,
            # correct answer is presented by the letter index
            # and if for some reason there's no correct answer, return -1
            "correctAnswerIndex": ord(correct) - ord("A") if correct else -1,
            # regex here removes
            "options": [re.sub(r"[A-Z]\. ", "", option.get_text()) for option in options],
            "answerExplanation": answer_explanation
        }

        all_questions.append(question)

    # with open("questions.json", "w", encoding="utf-8") as f:
    #     json.dump(all_questions, f, indent=2, ensure_ascii=False)

    return all_questions
    # return json.dumps(all_questions, indent=2, ensure_ascii=False)
