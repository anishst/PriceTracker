# Price Tracker App

App to keep track of prices and get alerts when desire price is reached. Currently the app expects db to be running on IP mongodb://192.168.1.50:27017

## Setup:

App uses Flask Framework and MongoDB as the database. 

## Deployment

Uses Docker and docker-compose to deploy the app

Steps to run: 
1. Go to app dir in command line
2. run ```docker-compose up --build```

## GitHub Action

- added GitHub action feature to deploy automatically to Docker hub on commit
    - https://github.com/anishst/PriceTracker/blob/master/.github/workflows/main.yml