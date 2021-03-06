<h1 align='center'> Predictos </h1>
<h2 align='center'> Predict your potential networth using Ai </h2>

So I have been playing those fun `Facebook games` for a while where they say you'll get married in this year or you'll have this many kids bla bla. But noboady gives you the reason why? I think these are pretty random. So thought of building a fun game using `Machine Learning`, and provide **Data Driven** results.

<p align='center'> 
    <img alt = 'home_imge' width = 550px src = 'results/desktop_home.png'>
</p>

----------------------------

## Approach : 

* I have collected data of top 100 richest persons in different fields. I have used `BeautifulSoup` to scrape [therichest.com](https://www.therichest.com/top-lists/top-100-richest).
* after collecting the data done some data cleaning and feature engineering on raw data. 
* fitted multiple regression model and used hyper parameter tuning to get the best result. 
* saved the model in a `.sav` file and.
* later used the same model in the `flask app` 

------------------------------

## How to run? 

> To run the app you need to download this repository along with the required libraries. and you have to the `app.py` file. 

> after running `app.py` open [http://127.0.0.1:5000](http://127.0.0.1:5000)

------------------------------- 

## Document Structure 

```
Personal Finance 
│
|---- Data
|   |-- preprocessed_df.csv
|   |-- Rich.csv
|
|---- results
|   |-- desktop_home.png
|   |-- desktop_prediction.png
|   |-- mobile_home.png
|   |-- mobile_prediction.png
|
|---- scraper 
|   |-- webscraper.py
|
|---- static 
|   |-- images
|   |
|
|   |-- styles
|   |   |-- index.css
|   |   |-- prediction.css
|   
|---- templates
|   |   |-- index.html
|   |   |-- layout.html
|   |   |-- prediction.html
|
|
|---- app.py
|---- LICENSE
|---- model_training.ipynb
|---- markdown.py
|---- random_forest_regression_model.pkl
|---- random_forest_regression_model.sav
|---- README.md
|---- requirements.txt

```
---------------------

## Technologies used : 

* python library - numpy, pandas, seaborn, matplotlib, flask, plotly, sklearn, joblib, bs4
* version control - git 
* backend - flask
* concept - Machine Learning

## Tools and Services : 
* IDE - Vs code 
* Application Deployment - local host
* Code Repository - GitHub

-----------------------
<br>

# If you Liked this project the you can consider connecting with me:
* [LinkedIn](https://www.linkedin.com/in/soumyadip-ghorai/) 

* You can find my other projects and EDAs on [Kaggle](https://www.kaggle.com/soumyadipghorai)
