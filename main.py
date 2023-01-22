import datetime as dt
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3
con = sqlite3.connect('data.db')
c = con.cursor()
c.execute("SELECT * FROM amount")
itm = c.fetchall()
st.header(f"🪙{itm[-1]}")
stock = st.text_input("ENTER SYMBOL OF THE STOCK TO BUY:")
no_stock = st.text_input("ENTER NO OF STOCKS:")
buy = st.button("BUY")
if buy:
    a =  yf.download(
        stock, dt.date(2022, 12, 1), dt.datetime.now())

    ca = yf.download(
        stock, period="1d", interval='1d')
    plo = a["Close"]
    b = ca["Close"]
    sp =round(np.average((b)))
    no_stock = int(no_stock)
    tpos = no_stock * sp

    c.execute(
     f"INSERT INTO stocks VALUES('{stock}','{tpos}','{no_stock}')")
    con.commit()
    c.execute("SELECT * FROM amount")
    it = c.fetchall()
    for k in it:
        camt = k[-1] - tpos
        c.execute(
            f"INSERT INTO amount VALUES('{camt}')")
        con.commit()



c.execute("SELECT * FROM stocks")
item = c.fetchall()
for i in item:
    plo = yf.download(
        i[0], dt.date(2020, 1, 1), dt.datetime.now())
    plo = plo["Close"]
    k = yf.download(
        i[0], period="1d", interval='1d')
    l = k["Close"]
    stp = round(np.average((l)))
    st.header(i[0])
    st.line_chart(plo)
    st.text(stp)
    for ma in range(len(i[0])): 
        ma = ma 

    sell = st.button("SELL",key = ma)
    if sell:
        c.execute("SELECT * FROM amount")
        it = c.fetchall()
        tspb = i[1]/i[2]
        for k in it:
            camt = k[-1] + (tspb-stp) +i[1]
            c.execute(
                f"INSERT INTO amount VALUES('{camt}')")
            con.commit()
        name = i[0]
        c.execute(f"DELETE FROM stocks where name = '{name}'")
        con.commit()
