# tradingcomdados

## Introduction
*Trading com Dados Library for quantitative finance*

The library consists of a collection of methods that can be used in order to help Data Scientists, Quantitative Analysts and data professionals during the development of quantitative finance applications. One of the main objectives of the library is to provide methods to connect to Trading com dados' data provider services.

## Library Motivation and Description
Trading com dados is an Edtech that provides educational content for people who want to know quantitative finance and in order to obtain that knowlegde, we need quality data, thus this library and our API service was created to solve that.

## API methods
-> get_data

-> get_data_tickers


## How to install
```python 
pip install tradingcomdados
```

## Importing and fetching data
```python
import tradingcomdados as tcd

# Fetching data
tcd.get_data('PETR4', start = '01/01/2019')
```
## Machine Learning
This library has a few machine learning models that you can use in your daily activities.

With our lib, you can easily implement machine learning models to your daily activities in the financial market.

```python
from tradingcomdados import unsupervised_learning as ul

ul.clustering_pipeline()
```

## Alternative Data
You can obtain alternative data from the Brazilian Market using this library


```python
from tradingcomdados import alternative_data as ad

ad.ibov_composition()
```
