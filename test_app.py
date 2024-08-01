import subprocess
import time
import pandas as pd
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest.mock import patch
import streamlit as st

def build_sidebar():
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    prices = pd.DataFrame({
        'AAPL': [150, 152, 153],
        'GOOGL': [2800, 2820, 2830],
        'MSFT': [300, 305, 310]
    })
    return tickers, prices

def build_main(tickers, prices):
    average_prices = prices.mean()
    st.title('Portifolio e Analises de Ações')
    st.write(average_prices)

@patch('streamlit.title')
def test_title(mock_title):
    tickers, prices = build_sidebar()
    build_main(tickers, prices)
    mock_title.assert_called_once_with('Portifolio e Analises de Ações')

def test_end_to_end():
    process = subprocess.Popen(['streamlit', 'run', 'app.py'])
    time.sleep(5)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://localhost:8501')

    try:
       
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        assert title_element.text == 'Portifolio e Analises de Ações'

    
        table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )
        assert table_element is not None

       
        header_cells = table_element.find_elements(By.TAG_NAME, 'th')
        assert len(header_cells) == 2  

        # Verificar a presença de pelo menos uma linha de dados
        data_rows = table_element.find_elements(By.TAG_NAME, 'tr')
        assert len(data_rows) > 1  

    finally:
        driver.quit()
        process.terminate()