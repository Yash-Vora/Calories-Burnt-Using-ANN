'''
To run app in docker follow this process:
1. Build the image: docker build -t caloriesburntapp .
2. Run the image: docker run -p 8000:8000 caloriesburntapp
'''
# Required Libraries
from flask import Flask, render_template, request
from tensorflow.python.keras.models import load_model
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
import pickle

# Initializing app
app = Flask(__name__)


# Load Model
model = load_model('calories.h5')

# Load scaler object
with open('scaler.pkl', 'rb') as file:
    sc = pickle.load(file)
    
# Creating Pipeline
calories_burnt_pipeline = Pipeline(steps=[
    ('scaling', sc),
    ('model', model)
])

# Method that will predict how many calories will be burnt
def total_calories_burnt(input_):  # input_ = [Age, Height, Weight, Duration, Heart_Rate, Body_Temp, Gender]
    # In Gender if it is male then 1 otherwise 0
    input_[-1] = 1 if input_[-1] == 'male' else 0
    # convert to a numpy array
    input_arr = np.array(input_)
    # change shape from (7,) to (1,7)
    input_arr = np.expand_dims(input_arr, 0)
    # Calories burnt prediction
    prediction = round(calories_burnt_pipeline.predict(input_arr)[0,0], 3)
    
    return prediction


# This route will return predicted calories
@app.route("/", methods=['GET', 'POST'])
def calories_burnt():
    if request.method == 'POST':
        # Input from user
        input_ = [request.form['Age'], request.form['Height'], request.form['Weight'], request.form['Duration'], 
                    request.form['Heart_Rate'], request.form['Body_Temp'], request.form['Gender']]
        # Calories burnt prediction
        prediction = total_calories_burnt(input_)

        return render_template('index.html', prediction = prediction)

    return render_template('index.html')


if __name__ == '__main__':
   app.run()