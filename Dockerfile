FROM python:3.9
COPY ./Code/calories.h5 ./Code/scaler.pkl ./Web_App_Code/app.py ./Dockerfile ./requirements.txt  ./caloriesburntapp/
COPY ./Web_App_Code/templates ./caloriesburntapp/templates/
WORKDIR /caloriesburntapp
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app