## Cyptocurrency Market Analysis Codesheets and Notebooks

**Plots and EDA v1**

First version of the exporatory analysis. This sheet and the ones to follow pull from the Yahoo Finance API to get 2014-2021 daily opening and closing prices. The analysis contains
time series charts for each of the stocks, histograms for gaily change, and coorelation matricies. The analysis then identifies days where the S&P experienced large drops and captures
the data from the two weeks following these drops. From this data, histograms of daily change in the cryptocurrencies were created as well as new coorelation matricies

**EDA v2**

Version 2 repeats all the analysis in version 1, except with more recent data (2019-2021). The idea is to see how the relationships have changed now that the cryptocurrencies have become
more popular.

**Time Series**

Individual time series charts for each of the markets

**Rolling Average and Regression**

This analysis is similar to the exploratory analysis, except using weekly change instead of daily change. Weekly change is then used when creating the regression models for the project.
Weekly % change was selected for the following reasons: to combat the volatility seen in the cryptocurrencies, put all the variables on the same scale so the coefficients can be compared,
weekends are no longer an incosistency between crypto and market trading.

**ANOVA Prediction**

Each of the cryptocurrencies has their own ANOVA analysis and prediction. The ANOVA prediction gives the 95% prediction interval for future price.
