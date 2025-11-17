import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AS Market Maker", layout="wide")
st.title("Avellaneda-Stoikov Professional Simulation")

with st.sidebar:
    st.header("Model Inputs")
    s0 = st.number_input("Starting Price", value=100.0)
    sigma = st.sidebar.slider("Volatility (sigma)", 0.1, 5.0, 2.0)
    gamma = st.sidebar.slider("Risk Aversion (gamma)", 0.01, 1.0, 0.1)
    k = st.sidebar.slider("Order Intensity (k)", 0.5, 3.0, 1.5)
    A = st.number_input("Order Density (A)", value=140)
    steps = 1000
    dt = 1.0 / steps

def run_simulation():
    # Generate price path using Brownian Motion
    increments = np.random.normal(0, sigma * np.sqrt(dt), steps)
    prices = s0 + np.cumsum(increments)
    times = np.linspace(0, 1, steps)

    inventory = np.zeros(steps)
    wealth = np.zeros(steps)
    bids, asks = np.zeros(steps), np.zeros(steps)

    for t in range(1, steps):
        time_left = 1.0 - times[t]
        
        # Avellaneda-Stoikov formulas for price and spread
        res_price = prices[t] - (inventory[t-1] * gamma * (sigma**2) * time_left)
        spread = (gamma * (sigma**2) * time_left) + (2/gamma) * np.log(1 + (gamma/k))
        
        bids[t], asks[t] = res_price - spread/2, res_price + spread/2
        
        # Calculate probability of fill using Poisson intensity
        lambda_bid = A * np.exp(-k * (prices[t] - bids[t]))
        lambda_ask = A * np.exp(-k * (asks[t] - prices[t]))
        
        inventory[t], wealth[t] = inventory[t-1], wealth[t-1]
        
        # Execute trades based on simulated arrivals
        if np.random.random() < (lambda_bid * dt):
            inventory[t] += 1
            wealth[t] -= bids[t]
        if np.random.random() < (lambda_ask * dt):
            inventory[t] -= 1
            wealth[t] += asks[t]

    return pd.DataFrame({
        "Time": times, "Price": prices, "Bid": bids, "Ask": asks,
        "Inventory": inventory, "Wealth": wealth,
        "Equity": wealth + (inventory * prices)
    })

if st.button("Run Market Maker Simulation"):
    df = run_simulation()

    m1, m2, m3 = st.columns(3)
    m1.metric("Final PnL", f"${df['Equity'].iloc[-1]:.2f}")
    m2.metric("Max Inventory", f"{df['Inventory'].abs().max():.0f} units")
    m3.metric("Avg Spread", f"${(df['Ask'] - df['Bid']).mean():.4f}")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Time"], y=df["Price"], name="Mid Price", line=dict(color='gray', dash='dash')))
    fig1.add_trace(go.Scatter(x=df["Time"], y=df["Bid"], name="Bid", line=dict(color='green')))
    fig1.add_trace(go.Scatter(x=df["Time"], y=df["Ask"], name="Ask", line=dict(color='red')))
    fig1.update_layout(title="Market Maker Quotes", xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Inventory Risk")
        st.bar_chart(df.set_index("Time")["Inventory"])
    with col_b:
        st.subheader("Total Equity (PnL)")
        st.line_chart(df.set_index("Time")["Equity"])