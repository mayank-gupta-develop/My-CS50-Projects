import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Get current user's stocks
    rows = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    portfolio = []
    total_stock_value = 0

    for row in rows:
        stock = lookup(row["symbol"])
        price = stock["price"]
        total = price * row["total_shares"]

        portfolio.append({
            "symbol": row["symbol"],
            "shares": row["total_shares"],
            "price": price,
            "total": total
        })

        total_stock_value += total

    # Get user's cash
    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        session["user_id"]
    )[0]["cash"]

    grand_total = total_stock_value + cash

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be a positive integer")
        except:
            return apology("shares must be a positive integer")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        price = stock["price"]
        total_cost = price * shares

        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]["cash"]

        if total_cost > cash:
            return apology("can't afford")

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            stock["symbol"],
            shares,
            price,
            "BUY"
        )

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost,
            session["user_id"]
        )

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)


@app.route("/history")
@login_required
def history():

    rows = db.execute("""
        SELECT symbol, shares, price, type, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, session["user_id"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        if not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("missing symbol")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not username or not password or not confirmation:
            return apology("must provide username and password")

        if password != confirmation:
            return apology("passwords do not match")

        # Hash password
        hash = generate_password_hash(password)

        # Insert into database
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash
            )
        except ValueError:
            return apology("username already exists")

        # Redirect to login
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "GET":

        # Get stocks the user owns
        rows = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, session["user_id"])

        return render_template("sell.html", stocks=rows)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol")

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be a positive integer")
        except:
            return apology("shares must be a positive integer")

        # How many shares user owns
        owned = db.execute("""
            SELECT SUM(shares) AS total
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol)[0]["total"]

        if owned is None or shares > owned:
            return apology("not enough shares")

        stock = lookup(symbol)
        price = stock["price"]
        total_value = price * shares

        # Record SELL transaction (negative shares)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, ?)
        """, session["user_id"], symbol, -shares, price, "SELL")

        # Add cash back
        db.execute("""
            UPDATE users SET cash = cash + ?
            WHERE id = ?
        """, total_value, session["user_id"])

        return redirect("/")
