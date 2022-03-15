import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    # Get all owned stocks
    inventory = db.execute("SELECT * FROM inventories WHERE userid LIKE ?",  session["user_id"])
    # get and extract cash
    cashAmount = db.execute("SELECT cash FROM users WHERE id LIKE ?",  session["user_id"])
    cashAmount = cashAmount[0]["cash"]

    # get price and TOTAL value of each stock
    prices = []
    # keep track of stock value
    value = cashAmount
    # sham i counter to keep benefits of in loop
    i = 0
    for stock in inventory:
        # get live stock data
        stockDats = lookup(stock["symbol"])

        thisStock = {
            "price": stockDats["price"],
            "total": stockDats["price"] * inventory[i]["shares"]
        }
        value += (stockDats["price"] * inventory[i]["shares"])

        prices.append(thisStock)
        i += 1
    return render_template("index.html", inventory=inventory, cashAmount=cashAmount, prices=prices, value=value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        if not shares.isInteger() and shares < 0:
            return apology("WHAT")

        # get data
        symbolData = lookup(symbol)

        if symbolData:
            # after validating input grab cost
            cost = symbolData["price"]

            # get user cash amount
            userMoney = db.execute("SELECT cash FROM users WHERE id LIKE ?", session["user_id"])
            userMoney = userMoney[0]["cash"]
            # make a var for cashSpent calc
            cashLeft = userMoney - (cost * float(shares))

            if cashLeft >= 0:
                # reduce person's cash
                db.execute("UPDATE users SET cash = ? WHERE id LIKE ?", cashLeft, session["user_id"])

                # get date and time using external lib
                time = datetime.now()
                dtString = time.strftime("%Y/%m/%d %H:%M:%S")

                # keep track of purchase data, THIS IS FOR HISTORY
                db.execute("INSERT INTO purchases (userid, shares, price, date, symbol) VALUES(?,?,?,?,?)",
                           session["user_id"], shares, cost, dtString, symbolData["symbol"])

                # Change stock inventory for this user, THIS IS FOR INDEX
                stockCheck = db.execute("SELECT * FROM inventories WHERE userid LIKE ? AND symbol LIKE ?",
                                        session["user_id"], symbolData["symbol"])
                companyName = symbolData["name"]

                if len(stockCheck) <= 0:
                    # user does not yet have any of this stock, create a new inventory
                    db.execute("INSERT INTO inventories (userid, symbol, name, shares) VALUES (?,?,?,?)",
                               session["user_id"], symbolData["symbol"], companyName, shares)
                else:
                    # user already has some stock for this symbol, add to it
                    db.execute("UPDATE inventories SET shares = shares + ? WHERE userid LIKE ? AND symbol LIKE ?",
                               shares, session["user_id"], symbolData["symbol"])
                # send to home page
                return redirect("/")
            else:
                return apology("LOL U BROKE")
        else:
            return apology("INVALID SYMBOL")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # get sql stuff
    history = db.execute("SELECT * FROM purchases WHERE userid LIKE ?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
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

        # get data from IEX
        symbolData = lookup(symbol)

        if symbolData:
            # grab cost once input is validated
            cost = symbolData["price"]
            return render_template("quoted.html", symbol=symbolData["symbol"], cost=cost)
        else:
            return apology("Invalid Symbol")

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # get site data
        user = request.form.get("username")
        password = request.form.get("password")
        passConf = request.form.get("confirmation")

        # check unique userName
        if len(db.execute("SELECT * FROM users WHERE username LIKE ?", user)) > 0:
            return apology("USERNAME USED")
        # check both passwords ok
        if(password != passConf):
            return apology("INCONSISTENT PASSWORD")
        # check if passworfd secure
        specialChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        for char in specialChars:
            if char in password:
                break
            if char == ')':
                return apology("PLEASE MAKE A STRONG PASSWORD, ADD ANY OF THE FOLLOWING CHARACTERS !@#$%^&*()")

        # add to users db
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", user, password)

        # Redirect user to login form
        return redirect("/login")
    else:
        return render_template("/register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        # get SQL shares, check if number of shares inputted agrees with shares owned
        SQLshares = db.execute("SELECT shares FROM inventories WHERE userid LIKE ? AND symbol LIKE ?", session["user_id"], symbol)

        # since you are only allowed one inventory of a stock at a time based on boolean logic in /BUY, only one row should meet the above requirements
        if int(shares) > SQLshares[0]["shares"]:
            return apology("TOO MANY SHARES DOOD")

        # else shares are viable, so get stock price, multiply by shares and to cash amount
        priceData = lookup(symbol)
        priceData = priceData["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id LIKE ?", priceData*float(shares), session["user_id"])

        # update inventory shares
        if int(shares) == int(SQLshares[0]["shares"]):
            # kill the row, since all shares are sold
            db.execute("DELETE FROM inventories WHERE symbol LIKE ? AND userid LIKE ?", symbol, session["user_id"])
        else:
            # reduce shares
            db.execute("UPDATE inventories SET shares = shares - ? WHERE symbol LIKE ? AND userid LIKE ?",
                       shares, symbol, session["user_id"])

        # add to purchases (HISTORY TABLE)
        time = datetime.now()
        dtString = time.strftime("%Y/%m/%d %H:%M:%S")
        # keep track of purchase data, THIS IS FOR HISTORY
        db.execute("INSERT INTO purchases (userid, shares, price, date, symbol) VALUES(?,? * -1,?,?,?)",
                   session["user_id"], shares, priceData, dtString, symbol)

        return redirect("/")
    else:
        # get all symbols of owned stock
        symbols = db.execute("SELECT symbol FROM inventories WHERE userid LIKE ?", session["user_id"])
        return render_template("sell.html", symbols=symbols)

