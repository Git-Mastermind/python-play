import streamlit as st
import requests
import mysql.connector
import time
import sys


API_KEY = sys.argv[1]


if "show_buy" not in st.session_state:
    st.session_state.show_buy = False
if "sign_up_true_false" not in st.session_state:
    st.session_state.sign_up_true_false = False
if "log_in_true_false" not in st.session_state:
    st.session_state.log_in_true_false = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "balance_button" not in st.session_state:
    st.session_state.balance_button = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "portfolio" not in st.session_state:
    st.session_state.portfolio = False

connection = mysql.connector.connect(
    host="localhost",
    port = 3306,
    user="eshanjha",
    password="ILovebooks!@#123",
    database="stocks_db"
)

    

cursor = connection.cursor()

def sign_up(email, name):
    user_id = ""

    for i in range(len(email)):
        if email[i] != "@":
            user_id += email[i]
        else:
            break

    cursor.execute(f'INSERT INTO users (user_id, email, name, balance) VALUES ("{user_id}", "{email}", "{name}", 150000);')
    connection.commit()
    st.write("Signing up...")
    time.sleep(0.8)
    st.write("Adding finished touches...")
    time.sleep(0.4)
    st.write(f"✅ Successfully signed up! Your user id is {user_id}!")
    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    st.rerun()

def log_in(user_id):
    cursor.execute(f'SELECT name FROM users WHERE user_id = "{user_id}";')
    name = cursor.fetchall()

    if name != []:
        st.write("Getting data...")
        time.sleep(1)
        st.write(f"✅ Successfully logged in! Welcome {name[0][0]}")
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        time.sleep(0.8)
        st.rerun()
        return user_id
        
    else:
        st.write("❌ User Id not found")

def buy_stock(company_name, amount):
    response = requests.get(f"https://finnhub.io/api/v1/search?q={company_name}&token={API_KEY}")
    symbol_data = response.json()
    if symbol_data["result"] == []:
        st.write("❌ Company not found!")
    else:
        price = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol_data["result"][0]["displaySymbol"]}&token={API_KEY}')
        price_data = price.json() 
        ticker = symbol_data["result"][0]["displaySymbol"]
        buy_price = int(price_data["c"])
        quantity = int(amount) / buy_price
            
   
        st.write(f'✅ Bought ${amount} ({quantity} shares) of {ticker} at {buy_price}')
        cursor.execute(f'UPDATE users SET balance = balance - {amount} where user_id = "{st.session_state.user_id}";')
        cursor.execute(f'INSERT INTO stocks (user_id, ticker, buy_price, quantity, company_name) VALUES ("{st.session_state.user_id}", "{ticker}", {buy_price}, {quantity}, "{company_name}");')
        connection.commit()
        time.sleep(3)
        st.session_state.show_buy = False
        st.rerun()

def view_balance():
    cursor.execute(f'SELECT balance FROM users WHERE user_id = "{st.session_state.user_id}";')
    balance = cursor.fetchone()
    formatted_balance = f"💰 Balance: $150,000.00"
    uninvested_money = f"🪙 Uninvested Money: ${balance[0]:,.2f}"
    st.write(formatted_balance)
    st.write(uninvested_money)
    time.sleep(3)
    st.session_state.balance_button = False
    st.rerun()


def view_portfolio():
    cursor.execute(f'SELECT ticker, quantity FROM stocks WHERE user_id = "{st.session_state.user_id}";')
    portfolio = cursor.fetchall()
    portfolio_formatted = ""
    buy_price = cursor.execute(f'SELECT buy_price FROM stocks WHERE user_id = "{st.session_state.user_id}";')
    current_price_response = requests.get()
    for i in range (len(portfolio)):
        portfolio_formatted + portfolio[i][0] + "----> " + str(portfolio[i][1]) + " shares" + "\n"
    
    st.write(portfolio_formatted)

if not st.session_state.logged_in:
    log_in_button = st.button("Log In")
    sign_up_button = st.button("Sign Up")

    if sign_up_button:
        st.session_state.sign_up_true_false = True
    if st.session_state.sign_up_true_false:
        name = st.text_input("Full Name: ")
        email = st.text_input("Email: ")
        if name and email:
            sign_up_confirmation = st.button("Sign Up Confirmation")
            if sign_up_confirmation:
                sign_up(email, name)
    if log_in_button:
        st.session_state.log_in_true_false = True
    if st.session_state.log_in_true_false:
        user_id = st.text_input("User Id: ")
        if user_id:
            log_in_confirmation = st.button("Log In Confirmation")
            if log_in_confirmation:
                st.session_state.user_id = log_in(user_id)
                
else:

    buy_stock_button = st.button("Trade")
    sell_stock_button = st.button("Sell")
    view_balance_button = st.button("View Balance")
    portfolio_button = st.button("Portfolio")

    if buy_stock_button:
        st.session_state.show_buy = True

    if st.session_state.show_buy:
        company = st.text_input("Company: ")
        amount = st.text_input("Amount ($): ")
        if company and amount:
            buy = st.button("Buy")
            if buy:
                buy_stock(company, amount)
    
    if view_balance_button:
        st.session_state.balance_button = True
    if st.session_state.balance_button:
        view_balance()
    
    if portfolio_button:
        st.session_state.portfolio = True
    if st.session_state.portfolio:
        view_portfolio()
        

            






        





