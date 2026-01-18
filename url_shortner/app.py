import sqlite3
import string
import random
import re
from flask import Flask, render_template, request, redirect, abort

app = Flask(__name__)
DB_NAME = "urls.db"


# ---------------- DATABASE ----------------

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()


# ---------------- HELPERS ----------------

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def is_valid_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)'
        r'([\w\-]+\.)+[\w\-]+'
        r'(\/[\w\-._~:\/?#[\]@!$&\'()*+,;=%]*)?$'
    )
    return re.match(pattern, url) is not None


def generate_unique_code():
    conn = get_db_connection()
    while True:
        code = generate_code()
        row = conn.execute(
            "SELECT id FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if row is None:
            conn.close()
            return code



@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form.get("original_url").strip()

        if not is_valid_url(original_url):
            error = "Enter valid URL including http:// or https://"
        else:
            conn = get_db_connection()

            row = conn.execute(
                "SELECT short_code FROM urls WHERE original_url = ?",
                (original_url,)
            ).fetchone()

            if row:
                short_code = row["short_code"]
            else:
                short_code = generate_unique_code()
                conn.execute(
                    "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                    (original_url, short_code)
                )
                conn.commit()

            conn.close()
            short_url = request.host_url + short_code

    return render_template("index.html", short_url=short_url, error=error)


@app.route("/history")
def history():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM urls ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("history.html", urls=rows, host=request.host_url)


@app.route("/<code>")
def redirect_to_original(code):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (code,)
    ).fetchone()
    conn.close()

    if row is None:
        abort(404)

    return redirect(row["original_url"])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
