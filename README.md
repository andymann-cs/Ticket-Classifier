# Ticket-Classifier

Dataset: Console-AI/IT-helpdesk-synthetic-tickets  
Source: Hugging Face  
License: MIT  

Compared effectiveness of different models (TF-IDF + Logistic, Pytorch, Transformers) on identifying the most reasonable recipient of an IT Ticket from a small dataset avaialbe on Hugging Face.
>>>>>>> d5468ff (Initial commit without model checkpoints)

# AI-Powered IT Ticket Router
A small project involving experimentation of differing models with their ability to classify example IT-helpdesk tickets.

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
Baseline model achieved:
Accuracy: 0.4657534246575342
Weighted F1: 0.2959928306234797
Macro F1: 0.0794392523364486

TF-IDF (Unweighted)
Accuracy: 0.6027397260273972
Weighted F1: 0.5162100456621005
Macro F1: 0.2885416666666667

TF-IDF (Weighted)
Accuracy: 0.7534246575342466
Weighted F1: 0.7639015055169991
Macro F1:0.751757294497082

PyTorchNN (Unweighted)
Accuracy: 0.726027397260274
Weighted F1: 0.7052681796496968
Macro F1: 0.5282276119402985

PyTorchNN (Weighted)
Accuracy: 0.6301369863013698
Weighted F1: 0.6435521440672963
Macro F1: 0.5621502383439989

DistilBERT (Unweighted)
Accuracy: 0.7945205479452054
Weighted F1: 0.7845618744963593
Macro F1: 0.6968431930388452

DistilBERT (Weighted)
Accuracy: 0.8082191780821918
Weighted F1: 0.8026262798150826
Macro F1: 0.7678236511996103

## Automated Routing Workflow
When a Jira ticket is created in a Space, the automated workflow through Jira's management service allows the ticket to be sent to an instance of FastAPI, made public through Ngrok, which contains a webhook that attempts to classify (through distilBERT) the most reasonable support team of the ticket. After assigning a class, provided there is enough confidence, the instance interacts with Jira through the available REST API and sends a label to assign the ticket. Besides the label, a log file is produced on the root device detailing the class assigned to an identified ticket, with a confidence and date time of assignment. 

This process is backed by requiring a secret for the webhook to ensure only the correct Jira Space can interact with the Fast API endpoint.

## Confidence Handling
>= 0.70 → automatic route
< 0.70 → manual-review

## Project Structure

## Setup
venv
pip install
.env variables
model location
uvicorn
ngrok

## Jira Integration
Automation rule configuration

## Security
API tokens
.env
webhook secret

## Logging
ticket_router.log examples

## Testing

## Limitations / Future Improvements
Small synthetic dataset
tiny minority classes
local ngrok deployment
possible production deployment