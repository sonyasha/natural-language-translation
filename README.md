# Natural Language translation project

***This project has the following goals:***
- Create a Machine Translation System application, based on the Recurrent Neural Network with Keras deep learning model.
- Implement a haiku generator using character-level multi-layer Recurrent Neural Network model.
- Deploy the application to Heroku.

***Results:***
- Language Model was trained on 100 000 pairs for each language (English - Spanish and English - French) and is able to translate short phrases like 'where is the bathroom', 'give me a fork', 'I like to swim' etc.
- Haiku Model generates haiku, that sound close to the haiku rules.
- Application was deployed to Heroku, see (<sup>*</sup>) below.


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


### On the WEB

***Instructions for opening***
1. Click the link https://trainslator.herokuapp.com 
2. Wait 5 minites while the app is loading. During this time you can see ```Application Error``` on the screen<sup>*</sup>.
3. Renew the web page.

<sup>*</sup>The reason is that Heroku has memory restrictions - 500GB per application and this application is larger (after importing all the dependencies and loading models). We are aware that Heroku is not a proper platform for deploying the machine learning applications and working on this issue.

The project description and web-presentation is located on https://sonyasha.github.io/nlt-presentation

## Team Members:

- Christina Park: idea, language model training
- Malvica Mathur: language model training, design, web-presentation
- Ed Ali: language model training, AWS machine learning application
- Sonya Smirnova: data preparation, haiku model training, application developing, front-end, back-end, Heroku deployment
- Abubeker Ali: language model adjusting, web-presentation

## Tools:

- Python
- TensorFlow
- Keras
- Selenium
- Flask
- JavaScript
- CSS
- HTML
