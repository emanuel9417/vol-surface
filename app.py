import streamlit as st
import yfinance as yf
from src.black_scholes import bs_pricer
from src.option_chain import OptionChain
from src.implied_vol import ImpliedVol
from src.vol_surface import VolSurface

st.title("Volatility Surface")
st.write("Enter the ticker of your choice from Yahoo Finance and click the button to generate the volatility smile and the volatility surface.")

@st.cache_resource
def load_smile(ticker, r):

    available = yf.Ticker(ticker).options
    if len(available) == 0:
        st.error("No options data available for this ticker on Yahoo Finance.")
        st.stop()

    expiry_index = min(5, len(available) - 1)

    example_chain = OptionChain(ticker, expiry_index=expiry_index)
    example_chain.fetch()
    example_chain.clean()

    example_iv = ImpliedVol(example_chain, r, max_iv=0.5)
    example_iv.compute_iv()
    example_iv.build_dataframe()

    return example_iv, example_chain.expiry

@st.cache_resource
def load_surface(ticker, r):

    vs = VolSurface(ticker, r)
    vs.collect_data()
    vs.pivot()
    return vs

col1, col2 = st.columns(2)
ticker = col1.text_input("Ticker", value = "AAPL")
r = col2.number_input("Risk-free rate:", min_value = 0.0, value = 0.05, step = 0.05)

if st.button("Go"):
        
        with st.spinner("In progress", show_time=True):

            iv, expiry = load_smile(ticker, r)
            st.plotly_chart(iv.plot_smile()) 
            st.caption(f"Smile example for the following maturity: {expiry}")

            vs = load_surface(ticker, r)
            st.plotly_chart(vs.surface_plot())            