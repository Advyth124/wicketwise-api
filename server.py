from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_matches():
    url = "https://www.espncricinfo.com/live-cricket-score"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Example: Extract match details (update based on ESPN structure)
    matches = []
    for match in soup.find_all("div", class_="match-info"):
        title = match.find("h3").text if match.find("h3") else "Unknown Match"
        score = match.find("span", class_="score").text if match.find("span", class_="score") else "No score"
        matches.append({"title": title, "score": score})

    return {"matches": matches}

@app.route("/live-matches", methods=["GET"])
def get_live_matches():
    data = scrape_matches()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
