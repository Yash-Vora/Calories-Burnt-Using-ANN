FROM python:3.9
COPY ./Code/calories.h5 ./Code/scaler.pkl ./Web_App_Code/app.py ./Dockerfile ./requirements.txt  ./caloriesburntapp/
COPY ./Web_App_Code/templates ./caloriesburntapp/templates/
WORKDIR /caloriesburntapp
RUN pip install -r requirements.txt
EXPOSE 8000
CMD gunicorn --workers 4 --bind 0.0.0.0:8000 app:app