# Natural Language translation project

***This project has the following goals:***
- Create a Machine Translation System application, based on the Recurrent Neural Network with Keras deep learning model.
- Implement a haiku generator using character-level multi-layer Recurrent Neural Network model.
- Deploy the application to Heroku.

## Requirements

```Python==3.6```\
```Flask==1.0.2```\
```gunicorn==19.9.0```\
```Keras==2.2.2```\
```scikit-learn==0.19.2```\
```scipy==1.1.0```\
```tensorflow==1.9.0```

The full list of requirements can be found in ```requirements.txt``` file

## Usage

Application can be opened locally and be deployed to Heroku.

### Local use

Install all necessary libraries.\
Proceed to ```local_app --> app``` folder.\
Run ```app.py```\
Open localhost ```http://127.0.0.1:5000/```

### Deployment

Install all necessary libraries.\
Proceed to ```heroku_app``` folder.\
Print ```heroku local``` in terminal.\
Open ```http://0.0.0.0:5000 (random_port_number)```\
If Everything works, the app is ready to be deployed on Heroku.

## On WEB

The app is located on https://trainslator.herokuapp.com/

The project description and web-presentation is located on https://gryazzz.github.io/nlt-presentation/

**Team Members:**

- Christina Park
- Malvica Mathur
- Ed Ali
- Sonya Smirnova
- Abubeker Ali


**Tools:**

- Python
- TensorFlow
- Keras
- Selenium
- Flask
- JavaScript
- HTML


## Steps of project

1. Data aquisition, cleaning and preparation.
2. Building model with Tensor Flow.
3. Model training.
4. Developing Flask app.
5. Developing Front-end.
6. Deploying.