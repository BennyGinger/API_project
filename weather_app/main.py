from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def weather(station: str, date: str):
    if station == "10" and date == "19881025":
        temperature = 20
    else:
        temperature = 0
    
    if station == "10":
        station = "Stockholm"
    else:
        station = "Unknown"
    return {'station': station, 'date': date, 'temperature': temperature}

if __name__ == "__main__":
    app.run(debug=True)