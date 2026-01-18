from flask import Flask, request, render_template
import re

server = Flask(__name__)

@server.route("/", methods=["GET", "POST"])
def main_page():
    found = []
    message = ""
    s = ""
    p = ""

    if request.method == "POST":
        s = request.form.get("input_text", "")
        p = request.form.get("pattern", "")

        if s != "" and p != "":
            try:
                engine = re.compile(p)
                pos = 0
                while True:
                    m = engine.search(s, pos)
                    if not m:
                        break
                    found.append(m.group())
                    pos = m.end()
            except:
                message = "Invalid pattern! Please check your regex."

    return render_template(
        "tool.html",
        output=found,
        error_msg=message,
        text_value=s,
        pattern_value=p
    )

if __name__ == "__main__":
    server.run(debug=True)
