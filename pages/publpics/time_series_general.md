---
layout: page
title: Time Series and Forecasting Projects
---

<div class="navbar">
  <div class="navbar-inner">
      <ul class="nav">
          <li><a href="#crime">Crime Forecasting</a></li>
          <li><a href="iplotCorr.html">next</a></li>
      </ul>
  </div>
</div>

### <a name="crime"></a>Crime Analysis and Forecasting Term Paper

This paper is a literature review of forecasting methods for Big Data, as they are applied to the field of crime analysis. It reviews the concepts of stationarity, seasonality, and trend, for forecasting modeling as well as the best practices for intorducing crime types and spatial granularity into the modeling. The bulk of the paper is spent reviewing studies that applied forecasting models (specifically ARIMA and/or LSTM model), understanding the intricacies in their application, and how they are used to develop actionable insights. 

[![pdf](../icons16/pdf-icon.png)](https://github.com/kylearbide/kylearbide.github.io/blob/master/Assignments/CSCI6444/Term_Paper_Kyle_Arbide_Crime_Forecasting_CSCI6444.pdf)

### <a name="stock market"></a> Pseudo Random Walk Down Wall Street

How well can machine learning assist us with understanding and prediciting the stock market? This is the question I explored with Patrick O'connor and Asare Buahin for our Final Project in EMSE6575. The project uses daily stock market trading data, and applies a variety of regression and classification algorithms, using lag prices of stock tickers as features for predicting Apple's stock price. To enhance our feature selection, we applied PCA to a larger sample of stocks across multiple industries with the goal of feeding our models a broad view of market trends. The final algorithm used features derived from this PCA to fit a Random Forest classifier, with target classes of -1 and 1 for a drop or gain in the stock price of AAPL.

[![github](../icons16/github-icon.png)](https://github.com/kylearbide/Stock-Market-Analysis-EMSE6575)


