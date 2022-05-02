from flask import Flask, render_template, request 
import joblib
import sklearn 
import jsonify
import pandas as pd 


df = pd.read_csv(r'end to end\predictos\data\Rich.csv')
image_df = pd.read_csv(r'end to end\predictos\data\preprocessed_df.csv')
model = joblib.load(open(r'end to end\predictos\random_forest_regression_model.sav', 'rb'))

country_dict = {
    'United states' : 18, 'United kingdom' : 17, 'France' : 5,
    'Brazil' : 2, 'South africa' : 14, 'Others' : 12, 'Spain' : 15, 
    'Italy' : 9, 'Australia' : 0, 'India' : 7, 'Canada' : 3, 
    'New zealand' : 11, 'Japan' : 10, 'Germany' : 6, 'China' : 4,
    'Switzerland' : 16, 'Russia' : 13, 'Ireland' : 8, 'Belgium' : 1
}

degree_dict = {
    'Post Graduate' : 1, 'high school' : 2, 'Graduate' : 0
}

marital_status_dict = {
    'single' : 3, 'married' : 2, 'divorced' : 0, 'in a relationship' : 1
}

category_dict = {
    'actresses' : 1, 'actors' : 0, 'baseball-players' : 2, 'basketball-players' : 3,
       'businesswomen' : 5, 'businessmen' : 4, 'ceos' : 6, 'comedians' : 7,
       'entrepreneurs' : 9, 'directors' : 8, 'hockey-players' : 10, 'models' : 11,
       'musicians' : 12, 'nfl-players' : 13, 'producers' : 14, 'rappers' : 15, 'singers' : 16,
       'soccer-players' : 17, 'tv-personalities' : 18
}

gender_dict = {
    'others' : 2, 'female' : 0, 'male' : 1
}

# find nearest int from database --> take his image --> name --> select quote
def find_image(value, dataframe) : 
    min_diff, row_num = 99999999999, 0
    for i in range(len(dataframe)) : 
        if abs(dataframe.net_worth.iloc[i] - value) < min_diff : 
            min_diff = abs(dataframe.net_worth.iloc[i] - value)
            row_num = i 
    name, name_text = dataframe.Name.iloc[row_num] , ''
    for word in name.split() : 
        name_text += word.capitalize() + ' '
        
    return dataframe.image.iloc[row_num], name_text, dataframe.category.iloc[row_num].capitalize()

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index() : 
    value = 'Predict your true worth using'
    return render_template('index.html', text = value)

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

        country = country_dict[country]
        degree = degree_dict[degree]
        relationship = marital_status_dict[relationship]
        category = category_dict[category]
        gender = gender_dict[gender]

        prediction = model.predict([[age, country, category, relationship, degree, gender]])
        print([age, country, category, relationship, degree, gender],prediction)

        if prediction < 0 : 
            return render_template('index.html', prediction_value = 'some random quote')  
        else : 
            return render_template('prediction.html', prediction_value = (find_image(prediction, image_df)), text = (name.capitalize(), int(prediction[0]))) 

    else : 
        return render_template('index.html', prediction_value = "invalid response")
 
if __name__ == "__main__" :
    app.run(debug = True)