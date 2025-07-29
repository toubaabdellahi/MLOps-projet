from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

# Charger le modèle et le vectorizer
model = joblib.load("name_gender_model.pkl")
vectorizer = joblib.load("name_gender_vectorizer.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    name = ""
    if request.method == "POST":
        name = request.form["name"]
        X = vectorizer.transform([name])
        prediction = model.predict(X)
        result = prediction[0]
    return render_template("form.html", name=name, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


