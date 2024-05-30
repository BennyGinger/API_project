from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load the thesaurus
df = pd.read_csv("/home/API/dictionnary/data/dictionary.csv")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<word>")
def definition(word: str):
    
    # Get the definition of the word
    matches = df.word.str.lower() == word.lower().replace("_", " ").replace("-", " ")
    
    # Check if the word is in the thesaurus
    if matches.sum() == 0:
        return {"error": f"Word {word} not found"}, 404
    
    # Get the definition
    definition = df[matches].definition.iloc[0]
    
    return {'definition': definition,'word': word}

if __name__ == "__main__":
    app.run(debug=True, port=5010)