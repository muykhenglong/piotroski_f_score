#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:22:59 2024

Piotroski F-Score 

@author: Muykheng Long

"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dow Jones Industrial Average's components as of June 11, 2024
# https://en.wikipedia.org/wiki/Historical_components_of_the_Dow_Jones_Industrial_Average
tickers = ['MMM','AXP','AAPL','BA','CAT','CVX','CSCO','KO','DOW','XOM','GS',
           'HD','INTC','IBM','JNJ','JPM','MCD','MRK','MSFT','NKE',
           'PFE','PG','TRV','UNH','RTX','VZ','V','WBA','WMT','DIS'] 

# List of tickers where financial data need to be extracted
financial_dir_cy = {} # directory to store current year (t) data
financial_dir_py = {} # directory to store previous year (t-1) data
financial_dir_py2 = {} # directory to store t-2 year data

for ticker in tickers:
    
    # Extract Income Statement
    
    url = f"https://finance.yahoo.com/quote/{ticker}/financials/"
    
    driver = webdriver.Safari()
    driver.get(url)
    driver.implicitly_wait(3)
    
    buttons = driver.find_elements(By.XPATH,"//article[@class='svelte-k66eqn']//button")
        
    for button in buttons:
        if button.accessible_name in ['']:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(button)).click()
        else:
            pass
    
    ## Convert HTML data
    table = driver.find_element(By.XPATH,"//div[@class='table svelte-1pgoo1f']").text
    table_text = table.strip().split('   ')
    
    temp_dir_cy = {} # To store values of the financial statement for the t year data
    temp_dir_py = {} # To store values of the financial statement for the t year data
    temp_dir_py2 = {} # To store values of the financial statement for the t year data
    
    
    no_period = len(table_text[0].split(' '))
        
    for row in table_text[1:]:
        temp_dir_cy[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][1]
        temp_dir_py[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][2]
        temp_dir_py2[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][3]
    
    driver.quit()
    
    # Extract Balance Sheet

    url = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet/"
    
    driver = webdriver.Safari()
    driver.get(url)
    driver.implicitly_wait(3)
    
    buttons = driver.find_elements(By.XPATH,"//article[@class='svelte-k66eqn']//button")
        
    for button in buttons:
        if button.accessible_name in ['']:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(button)).click()
        else:
            pass

    ## Convert HTML data
    table = driver.find_element(By.XPATH,"//div[@class='table svelte-1pgoo1f']").text
    table_text = table.strip().split('   ')
     
    no_period = len(table_text[0].split(' '))
        
    for row in table_text[1:]:
        temp_dir_cy[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][1]
        temp_dir_py[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][2]
        temp_dir_py2[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][3]
    
    driver.quit()


    # Extract Cash Flow Statement

    url = f"https://finance.yahoo.com/quote/{ticker}/cash-flow/"
    
    driver = webdriver.Safari()
    driver.get(url)
    driver.implicitly_wait(3)
    
    buttons = driver.find_elements(By.XPATH,"//article[@class='svelte-k66eqn']//button")
        
    for button in buttons:
        if button.accessible_name in ['']:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(button)).click()
        else:
            pass
    
    ## Convert HTML data
    table = driver.find_element(By.XPATH,"//div[@class='table svelte-1pgoo1f']").text
    table_text = table.strip().split('   ')
    
    no_period = len(table_text[0].split(' '))
        
    for row in table_text[1:]:
        temp_dir_cy[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][1]
        temp_dir_py[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][2]
        temp_dir_py2[(' '.join(row.split(' ')[:-(no_period-1)])).strip()] = row.split(' ')[-(no_period-1):][3]
    
    driver.quit()
    
    # Combine all data to fnancial_dir
    financial_dir_cy[ticker] = temp_dir_cy
    financial_dir_py[ticker] = temp_dir_py
    financial_dir_py2[ticker] = temp_dir_py2
    
combined_financials_cy = pd.DataFrame(financial_dir_cy)
combined_financials_py = pd.DataFrame(financial_dir_py)
combined_financials_py2 = pd.DataFrame(financial_dir_py2)

stats = ['Net Income Common Stockholders','Total Assets','Operating Cash Flow',
         'Total Non Current Liabilities Net Minority Interest',
         'Current Assets','Current Liabilities','Common Stock Equity',
         'Total Revenue','Gross Profit']

indx = ['NetIncome','TotAssets','CashFlowOps','LTDebt','CurrAssets','CurrLiab',
        'CommStock','TotRevenue','GrossProfit']

def info_filter(df,stats,indx):
    """    
    function to filter relevant financial information for each stock 
    and transform to numerical data
    """
    
    tickers = df.columns
    all_stats = {}
    
    for ticker in tickers:
        try:
            temp = df[ticker]
            ticker_stats = []
            for stat in stats:
                ticker_stats.append(temp.loc[stat])
            all_stats[ticker] = ticker_stats
        except:
            print(f'Cannot read data for {ticker}')
    
    all_stats_df = pd.DataFrame(all_stats, index=indx)
        
    # Convert to numerical data
    for ticker in tickers:
        all_stats_df[ticker] = all_stats_df[ticker].replace({',':''}, regex=True)
        all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values, errors='coerce')
   
    return all_stats_df

def piotroski_f(df_cy, df_py, df_py2):
    f_score = {}
    tickers = df_cy.columns
     
    for ticker in tickers:
        ROA_FS = int((df_cy.loc['NetIncome',ticker]/((df_cy.loc['TotAssets',ticker]+df_py.loc['TotAssets',ticker])/2)) > 0)
        CFO_FS= int(df_cy.loc['CashFlowOps',ticker] > 0)
        ROA_D_FS = int((df_cy.loc['NetIncome',ticker]/((df_cy.loc['TotAssets',ticker]+df_py.loc['TotAssets',ticker])/2)) > (df_py.loc['NetIncome',ticker]/((df_py.loc['TotAssets',ticker]+df_py2.loc['TotAssets',ticker])/2)))
        CFO_ROA_FS = int(df_cy.loc['CashFlowOps',ticker]/df_cy.loc['TotAssets',ticker] > (df_cy.loc['NetIncome',ticker]/((df_cy.loc['TotAssets',ticker]+df_py.loc['TotAssets',ticker])/2)))         
        LTD_FS = int(df_cy.loc['LTDebt',ticker] < df_py.loc['LTDebt',ticker])
        CR_FS = int(df_cy.loc['CurrAssets',ticker]/df_cy.loc['CurrLiab',ticker] > df_py.loc['CurrAssets',ticker]/df_py.loc['CurrLiab',ticker])
        DILUTION_FS = int(df_cy.loc['CommStock',ticker] <= df_py.loc['CommStock',ticker])
        GM_FS = int(df_cy.loc['GrossProfit',ticker]/df_cy.loc['TotRevenue',ticker] > df_py.loc['GrossProfit',ticker]/df_py.loc['TotRevenue',ticker])
        ATO_FS = int((df_cy.loc['TotRevenue',ticker]/((df_cy.loc['TotAssets',ticker]+df_py.loc['TotAssets',ticker])/2)) > (df_py.loc['TotRevenue',ticker]/((df_py.loc['TotAssets',ticker]+df_py2.loc['TotAssets',ticker])/2)))
        f_score[ticker] = [ROA_FS, CFO_FS, ROA_D_FS, CFO_ROA_FS, LTD_FS, CR_FS, DILUTION_FS, GM_FS, ATO_FS] 
    
    f_score_df = pd.DataFrame(f_score,index=['PosROA','PosCFO','ROAChange','Accruals','Leverage','Liquidity','Dilution','GM','ATO'])
    return f_score_df

# Select relevant info for each stock
transformed_df_cy = info_filter(combined_financials_cy, stats, indx)     
transformed_df_py = info_filter(combined_financials_py, stats, indx)     
transformed_df_py2 = info_filter(combined_financials_py2, stats, indx)     

# Remove financial stocks
transformed_df_cy.dropna(axis=1, inplace=True)
transformed_df_py.dropna(axis=1, inplace=True)
transformed_df_py2.dropna(axis=1, inplace=True)

# Select stocks with highest Piotroski F score
f_score_df = piotroski_f(transformed_df_cy, transformed_df_py, transformed_df_py2)
f_score_df.sum().sort_values(ascending=False)
