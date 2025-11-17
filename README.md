# Avellaneda-Stoikov Market Maker Simulator

A professional-grade simulation of the Avellaneda-Stoikov (2008) market making strategy. This application simulates high-frequency trading (HFT) dynamics, allowing users to visualize how inventory risk and volatility impact bid-ask spreads and profitability.

Built with **Python**, **Streamlit**, and **Plotly**.

## Overview

Market makers provide liquidity by quoting buy (bid) and sell (ask) prices. Their main risks are:
1.  **Inventory Risk:** Holding too much asset when the price drops.
2.  **Adverse Selection:** Trading against informed traders.

This simulator implements the classic solution to these problems derived by Marco Avellaneda and Sasha Stoikov. It adjusts the market maker's prices based on their current inventory level and market volatility to maximize the probability of profit.

## Features

* **Vectorized Simulation:** Uses NumPy for fast generation of Brownian motion price paths and trade simulation.
* **Interactive Parameters:** Adjust Volatility ($\sigma$), Risk Aversion ($\gamma$), and Order Intensity ($k$) in real-time.
* **Professional Visualizations:**
    * **Quote Chart:** Overlays Bid/Ask quotes against the Mid-Price.
    * **Inventory Tracking:** Visualizes stock accumulation over time.
    * **Equity Curve:** Tracks Profit and Loss (PnL) accounting for cash and asset value.
* **Metric Analysis:** Calculates Final PnL, Maximum Inventory held, and Average Spread width.

## Mathematical Model

The simulation relies on three core formulas:

### 1. Mid-Price (Brownian Motion)
The asset price follows an arithmetic random walk:
$$dS_t = \sigma dW_t$$

### 2. Reservation Price ($r$)
The price at which the market maker is indifferent between buying and selling. It adjusts based on inventory ($q$):
$$r(s, q, t) = s - q \gamma \sigma^2 (T - t)$$
* *Interpretation:* If inventory $q$ is positive (we hold stock), the reservation price lowers, incentivizing selling.

### 3. Optimal Spread ($\delta$)
The distance between the bid and ask quotes:
$$\delta = \gamma \sigma^2 (T - t) + \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{k}\right)$$
* *Interpretation:* Higher volatility ($\sigma$) or risk aversion ($\gamma$) leads to a wider spread.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HarshalGunjalOp/avellaneda-stoikov-sim.git](https://github.com/HarshalGunjalOp/avellaneda-stoikov-sim.git)
    cd avellaneda-stoikov-sim
    ```

2.  **Install dependencies:**
    ```bash
    pip install streamlit numpy pandas plotly
    ```

3.  **Run the application:**
    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

1.  Launch the app using the command above.
2.  Use the **Sidebar** to configure the simulation:
    * **Volatility ($\sigma$):** Controls how wild the price swings are.
    * **Risk Aversion ($\gamma$):** Controls how aggressively the algorithm sheds inventory. Higher values = tighter inventory control but potentially lower profit.
    * **Order Intensity ($k$):** Represents market liquidity.
3.  Click **Run Market Maker Simulation** to generate a new trading session.