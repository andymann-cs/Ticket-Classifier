# Ticket-Classifier

Dataset: Console-AI/IT-helpdesk-synthetic-tickets  
Source: Hugging Face  
License: MIT  

Compared effectiveness of different models (TF-IDF + Logistic, Pytorch, Transformers) on identifying the most reasonable recipient of an IT Ticket from a small dataset avaialbe on Hugging Face.

# AI-Powered IT Ticket Router
A small project involving experimentation of differing models with their ability to classify example IT-helpdesk tickets, before integrating the most favoured model to interact with the Jira REST API to automate ticket labelling.

## Overview
Experimented from varying levels of models from a TF-IDF + Logistic Regression to a simple transformer to exaluate the effectiveness of models in classifying example IT-helpdesk style tickets from a small dataset available on Hugging Face.

## Architecture
Jira → Automation → ngrok → FastAPI → DistilBERT → Jira REST API
(Ngrok exposes the local host as an accessible domain)

## Model Development
Development began by selecting a reasonable dataset. After browsing through Hugging Face's available datasets, "Console-AI/IT-helpdesk-synthetic-tickets" was selected. Despite being a small dataset with only 500 tickets available, this could prove a challenge for the more sophisticated models given each batch would consist of few training examples and therefore fewer reliable updates.

It was found that for a few categories out of the total 10, such as "Infrastructure", very few examples were given (<5 examples). After deciding it would be best to remove tickets of minor categories, the dataset was left with 8 categories, with some overpowering the dataset by taking a large portion of the avaialble examples. Models would take the ticket "Summary" and "Description" as inputs to give information for predicting the class. Since there was class imbalance, models were tested with and without class weightings to penalise mistakes especially for minority classes.

To begin with, a baseline model was used, which unsurprisingly labelled each example in the training, validation and testing set as the most popular category. Since a large majority of the dataset was from one category (software), the model achieved 46% accuracy. After building a simple TF-IDF+Logistic Regression model, a PyTorchNN implementation and finally a Transformer (distilBERT) model, the comparison between metrics were somewhat close, with distilBERT beating TF-IDF by a small margin.

## Results
All models were evaluated with the same validation split accuracy, weighted F1 and macro F1. Macro F1 was included due to class imbalances within the chosen dataset.

<img width="666" height="182" alt="image" src="https://github.com/user-attachments/assets/24043e82-e433-48a5-a3ee-bb41fd962257" />

DistilBERT achieved the strongest overall validation performance, reaching 80.8% accuracy, 0.803 weighted F1 and 0.768 macro F1.

## Automated Routing Workflow
When a Jira ticket is created in a Space, the automated workflow through Jira's management service allows the ticket to be sent to an instance of FastAPI, made public through Ngrok, which contains a webhook that attempts to classify (through distilBERT) the most reasonable support team of the ticket. After assigning a class, provided there is enough confidence, the instance interacts with Jira through the available REST API and sends a label to assign the ticket. Besides the label, a log file is produced on the root device detailing the class assigned to an identified ticket, with a confidence and date time of assignment. 

This process is backed by requiring a secret for the webhook to ensure only the correct Jira Space can interact with the Fast API endpoint.

## Confidence Handling
If the model confidence surpassed a set threshold (70% was chosen in this case), the ticket would be labelled with the predicted class. If not then the ticket would be set as "manual-review" meaning tickets would require manual labelling.

## Project Structure

## Setup
- Virtual environment containing all necessary libraries
- pip to install necessary libraries
- env variables for Jira API tokens, webhook secrets
- Uvicorn and FastAPI to host instances that allow interaction with Jira REST API
- Ngrok installed

## Jira Integration
Within Jira, an automation rule was configured such that whenever a new ticket was created, an action would be performed, sending a POST HTTP request to the ngrok url, along with the webhook password such to interact with the FastAPI server and receive a predicted ticket class.


## Logging
When submitting a request to predict a ticket's class, a log was made in the root folder. Examples of the kinds of contents shown below:
<img width="1027" height="151" alt="image" src="https://github.com/user-attachments/assets/b5c96c73-b891-4365-b58d-cac41f293cf2" />


## Testing

## Limitations / Future Improvements
Small synthetic dataset
tiny minority classes
local ngrok deployment
possible production deployment
