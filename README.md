
# ATCMarket Chatbot






## Overview

The project uses FAISS to store vectors, langchain for llm conversation thus with every user query. We perform two steps.
- Find similarity
- Feed the similarity results and the user query to the llm (which in this case is llama 3.3 70B).




## Deployment

After cloning this project. 

Follow the steps
## Step 1
- First make sure you have you data file. 
- File should be in docx format.
- The should contain data in question answer form.
- Every question should start with "QUESTION:" and every answer should start with "ANSWER:"
- Every Answer should have its reference link to the document from where it was made.

### Example
```Word
QUESTION: Who is the contracting party under the ATCMarket Free Membership Agreement?
ANSWER: The contracting party is ATCMARKET PORTAL with Company Registration No. 1452849. 
ATCMarket may also delegate some aspects of the Service to its affiliates.
IF you want to know more, check this link: 
https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/ATCMarket%20Free%20Membership%20Agreement.pdf

```

## Step 2
Then you have create a virtaul enviroment. For that:

```bash
  python -m venv venv
```


## Step 3
Then you have make you vector Database. 
For that, if you have 'make' installed in you system you can simply run

```bash
  make updatedb
```
Otherwise follow the steps:
- Activate virtual enviroment
```bash
  venv\Scripts\activate
```
- then cd into
```bash
  cd vectorDB
```
- Finally run:
```bash
  python make_faiss_db.py
```


## Step 4
### How to Run the chatbot
After the vector DB has been created. Check if you're in the root directory of the project. Then, if you have 'make' installed run:

```bash
  make run 
```
Otherwise follow the steps bellow:

- Activate virtual enviroment
```bash
  venv\Scripts\activate
```
- Then run:
```bash
  streamlit run chatbot.py
```
