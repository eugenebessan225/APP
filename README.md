## The APP API microservice

## Table Of Contents
- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [TODO](#todo)

## About The Project
This is an API that link the raspberry py and the frend.
All the request go through the app

## Built With
Python, Flask

## Getting Started
### Prerequisites

### Installation
1-Clone the repo
```sh
git clone https://github.com/eugenebessan225/app.git
```
2-Install dependencies
```sh
pip (conda) install
```
## usage
### Run app
```sh
python app.py
```
### API documentation
  - 'sshserver', methods=['GET'] is used to launch to establish a ssh connection to RPI server and launch the server script to connect socnnect and get data.
  - 'offsshserver', methods=['GET'] used to turn off the server and break the connections
  - Une fois le script du serveur lancé, celui ci envoie un message socket au serveur de type "data_request" et commeence à recevoir les données pour le moteur d'IA et pour l'affichage sur le dashboard.
## TODO
Dockerize + link to TimescaleDB
