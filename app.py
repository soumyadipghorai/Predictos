import sys
import pickle
import pandas as pd 
import numpy as np
import logging
import emoji
import random
from rich.logging import RichHandler
from flask import Flask, render_template, request 
from quotes import generateQuote

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn of debug
logger = logging.getLogger("rich")


from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('data/Rich.csv')
image_df = pd.read_csv('data/preprocessed_df.csv')
model = pickle.load(open('data/ML_models/StackedModelLog.pkl', 'rb'))
scaler = pickle.load(open('data/ML_models/StandardScaler.pkl', 'rb'))


categoryEncoder = pickle.load(open('data/ML_models/categoryEncoder.pkl', 'rb'))
degreeEncoder = pickle.load(open('data/ML_models/degreeEncoder.pkl', 'rb'))
genderEncoder = pickle.load(open('data/ML_models/genderEncoder.pkl', 'rb'))
nationalityEncoder = pickle.load(open('data/ML_models/nationalityEncoder.pkl', 'rb'))
maritalStatusEncoder = pickle.load(open('data/ML_models/maritalStatusEncoder.pkl', 'rb'))

emojiList = ["💰","🥳","💶","💴","🪙","💷","👑","🔥", "💸", "🐸"]

# find nearest int from database --> take his image --> name --> select quote
def find_image(value, dataframe, category, country) : 
    min_diff, row_num = sys.maxsize, 0
    unavailableImage = [
        'Derek Hough', 'Cloris Leachman', 'Vic Gundotra', 'Eric Koston', 
        'Shepard Fairey', 'Bobby Baldwin', 'Ted Harbert', 'Dr. Cindy Trimm', 
        'Jackee Harry', 'Tom Hiddleston'
    ]
    logging.info('Inside find_image ' + str(category) + str(country))
    toCheckDf = dataframe[(dataframe.category == category)]

    logging.debug(toCheckDf.head())
    for i in range(len(toCheckDf)) : 
        if abs(toCheckDf.networth.iloc[i] - value) < min_diff and (toCheckDf.Name.iloc[i] not in unavailableImage) : 
            min_diff = abs(toCheckDf.networth.iloc[i] - value)
            row_num = i 

    name, name_text = toCheckDf.Name.iloc[row_num] , ''
    for word in name.split() : 
        name_text += word.capitalize() + ' '
        
    return toCheckDf.profile_pic.iloc[row_num], name_text, toCheckDf.category.iloc[row_num].capitalize()

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index() : 
    value = 'Predict your true worth using'
    country = list(image_df.nationality.unique())
    category = list(image_df.category.unique())
    gender = list(image_df.gender.unique())
    marital_status = list(image_df.marital_status.unique())
    degree = list(image_df.Degree.unique())

    country.sort()
    category.sort()
    gender.sort()
    marital_status.sort()
    degree.sort()

    # return render_template(
    #     'index.html', 
    #     text = value, 
    #     countryList = country, 
    #     categoryList = category, 
    #     genderList = gender, 
    #     maritalStatusList = marital_status,
    #     degreeList = degree
    #     )
    return render_template(
        'newIndex.html', 
        countryList = country, 
        categoryList = category, 
        genderList = gender, 
        maritalStatusList = marital_status,
        degreeList = degree
    )

@app.route('/predict', methods = ['POST'])
def predict() : 

    if request.method == 'POST' : 
        name = request.form['name']
        age = int(request.form['age']) 
        category = request.form['category']
        country = request.form['country']
        gender = request.form['gender']
        degree = request.form['degree']
        relationship = request.form['relationship']

        if (age > 99) : 
            age = age / (99 - 20) 
            logging.warning("Age not within usual range! More")
        elif age < 25 : 
            age += 10 
            logging.warning("Age not within usual range! Less")

        if len(name) == 0 : 
            name = "Hi, "
            logging.warning("Name not mentioned")
      
        countryEncoded = nationalityEncoder.transform([str(country)])[0]
        degreeEncoded  = degreeEncoder.transform([str(degree)])[0]
        relationshipEncoded  = maritalStatusEncoder.transform([str(relationship)])[0]
        categoryEncoded  = categoryEncoder.transform([str(category)])[0]
        genderEncoded  = genderEncoder.transform([str(gender)])[0]

        logging.info('Encoding Done : ')
        logging.debug('Country -->'+ str(country)) 
        logging.debug('Deegree -->' + str(degree))
        logging.debug('relationship -->' + str(relationship))
        logging.debug('gender -->' + str(gender))

        to_predict = scaler.transform([[
            genderEncoded, categoryEncoded, degreeEncoded, relationshipEncoded, countryEncoded, age
            ]])

        prediction = np.exp(model.predict(to_predict))
        logging.debug("final networth prediction "+ str(prediction))

        if prediction < 0 : 
            return render_template('index.html', prediction_value = 'some random quote')  
        else : 
            # return render_template(
            #     'prediction.html',  
            #     prediction_value = (find_image(prediction, image_df, category, country)), 
            #     text = (name.capitalize(), round(int(prediction[0])))
            # ) 
            return render_template(
                'newPrediction.html',  
                prediction_value = (find_image(prediction, image_df, category, country)), 
                text = (
                    name.capitalize(), 
                    round(int(prediction[0])), 
                    emoji.emojize(emojiList[random.randint(0, len(emojiList)-1)])
                    ),
                quote = generateQuote()[0],
                author = generateQuote()[1]
            ) 
 
    else : 
        return render_template('index.html', prediction_value = "invalid response")
 
if __name__ == "__main__" :
    app.run(debug = True)