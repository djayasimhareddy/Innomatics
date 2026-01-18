from flask import Flask, request

app = Flask(__name__)

@app.route("/upper")
def show_upper():
    value = request.args.get("name")

    if value is None or value == "":
        return "<h2>Please provide name in URL like: /upper?name=yourname</h2>"

    out = ""
    for ch in value:
        if 'a' <= ch <= 'z':
            out += chr(ord(ch) - 32)
        else:
            out += ch

    return f"<h1>Converted Output: {out}</h1>"

@app.route("/reverse")
def show_reverse():
    text = request.args.get("text", "")

    rev = ""
    i = len(text) - 1
    while i >= 0:
        rev += text[i]
        i -= 1

    return f"<h2>Reversed Text: {rev}</h2>"

@app.route("/")
def home():
    return """
    <h1>Flask String Tools</h1>
    <p>Use like this:</p>
    <ul>
        <li>/upper?name=jayasimha</li>
        <li>/reverse?text=python</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True)
