#from crypt import methods
from enum import unique
import os
import sys
import random

import cohere
from flask import Flask, request, jsonify, render_template
from prompt_toolkit import prompt

sys.path.append(os.path.abspath(os.path.join('..')))
import creds

api_key = creds.api_key

# cohere class instance
co = cohere.Client(api_key)

# create an instance of the Flask class
app = Flask(__name__)

# list if items
items = [{"item": "item1"}, {"item": "item2"}]

#@app.route('/')
#def home():
    
    # Main page
    #user_input = request.get_json('Description')
    #return render_template('index.html')

# This is a simple placeholder for eccomerce, to make it dynamic we need to use a dictionary for different types of items and use the examples based on the item type
descs = [{
    "document": "Bachelor's degree in Mechanical Engineering or Physical Science 3+ years track record of developing or specifying fiber optic cables and connector related products Knowledge of fiber optic component, cabling, and interconnect products, technologies, and standards Experience in statistical data analysis Experience with product life cycle management (PLM) process Experience providing solutions to problems and meeting deadlines Experience engaging stakeholders PREFERRED Advanced degree Experience using a software tool for statistical data analysis such as JMP Experience using Agile as product life-cycle management tool Data center or other mission critical development experience",
    "tokens": [
      {
        "text": "Bachelor",
        "start": 0,
        "end": 8,
        "token_start": 0,
        "token_end": 0,
        "entityLabel": "DIPLOMA"
      },
      {
        "text": "Mechanical Engineering",
        "start": 21,
        "end": 43,
        "token_start": 4,
        "token_end": 5,
        "entityLabel": "DIPLOMA_MAJOR"
      },
      {
        "text": "Physical Science",
        "start": 47,
        "end": 63,
        "token_start": 7,
        "token_end": 8,
        "entityLabel": "DIPLOMA_MAJOR"
      },
      {
        "text": "3+ years",
        "start": 64,
        "end": 72,
        "token_start": 9,
        "token_end": 11,
        "entityLabel": "EXPERIENCE"
      },
      {
        "text": "developing",
        "start": 89,
        "end": 99,
        "token_start": 15,
        "token_end": 15,
        "entityLabel": "SKILLS"
      },
      {
        "text": "fiber optic cables",
        "start": 114,
        "end": 132,
        "token_start": 18,
        "token_end": 20,
        "entityLabel": "SKILLS"
      },
      {
        "text": "connector related products",
        "start": 137,
        "end": 163,
        "token_start": 22,
        "token_end": 24,
        "entityLabel": "SKILLS"
      }
    ],
    "relations": [
      { "child": 4, "head": 0, "relationLabel": "DEGREE_IN" },
      { "child": 7, "head": 0, "relationLabel": "DEGREE_IN" },
      { "child": 15, "head": 9, "relationLabel": "EXPERIENCE_IN" },
      { "child": 18, "head": 9, "relationLabel": "EXPERIENCE_IN" },
      { "child": 22, "head": 9, "relationLabel": "EXPERIENCE_IN" }
    ]
  },
  {
    "document": "10+ years of software engineering work experience. Technical experience in release automation engineering, CI/CD or related roles. Experience building and leading a software organization through product design, delivery and commercialization of consumer electronics devices. Experience recruiting and managing technical teams, including performance management. BS/MS in Computer Science. Experience in leading timeline, multi-partner initiatives. Organizational communication and coordination experience. PREFERRED 5+ years of experience with hands-on technical management, release engineering, tools engineering, DevOps, or related area.",
    "tokens": [
      {
        "text": "10+ years",
        "start": 0,
        "end": 9,
        "token_start": 0,
        "token_end": 2,
        "entityLabel": "EXPERIENCE"
      },
      {
        "text": "software engineering",
        "start": 13,
        "end": 33,
        "token_start": 4,
        "token_end": 5,
        "entityLabel": "SKILLS"
      },
      {
        "text": "5+ years",
        "start": 515,
        "end": 523,
        "token_start": 77,
        "token_end": 79,
        "entityLabel": "EXPERIENCE"
      },
      {
        "text": "technical management",
        "start": 552,
        "end": 572,
        "token_start": 86,
        "token_end": 87,
        "entityLabel": "SKILLS"
      },
      {
        "text": "release engineering",
        "start": 574,
        "end": 593,
        "token_start": 89,
        "token_end": 90,
        "entityLabel": "SKILLS"
      },
      {
        "text": "tools engineering",
        "start": 595,
        "end": 612,
        "token_start": 92,
        "token_end": 93,
        "entityLabel": "SKILLS"
      },
      {
        "text": "DevOps",
        "start": 614,
        "end": 620,
        "token_start": 95,
        "token_end": 95,
        "entityLabel": "SKILLS"
      },
      {
        "text": "BS/MS",
        "start": 361,
        "end": 366,
        "token_start": 53,
        "token_end": 55,
        "entityLabel": "DIPLOMA"
      },
      {
        "text": "Computer Science",
        "start": 370,
        "end": 386,
        "token_start": 57,
        "token_end": 58,
        "entityLabel": "DIPLOMA_MAJOR"
      }
    ],
    "relations": [
      { "child": 4, "head": 0, "relationLabel": "EXPERIENCE_IN" },
      { "child": 86, "head": 77, "relationLabel": "EXPERIENCE_IN" },
      { "child": 89, "head": 77, "relationLabel": "EXPERIENCE_IN" },
      { "child": 92, "head": 77, "relationLabel": "EXPERIENCE_IN" },
      { "child": 95, "head": 77, "relationLabel": "EXPERIENCE_IN" },
      { "child": 57, "head": 53, "relationLabel": "DEGREE_IN" }
    ]
  }
]


@app.route('/', methods = ['GET','POST'])

def description_route():      
    

        #document = request.get_json()['document']
        #tokens = request.get_json()['tokens']
        #relations = request.get_json()['relations']
        
        
        # construct final string from input
        user_input = request.form.get('Description')
        final = f"document: {user_input}\ntokens:"
        Task = f"Task: Generate job description tokens from the following job description\n"
        #prompt = Task + descs[0] + descs[1] + final
        first_shot = "10+ years of software engineering work experience. Technical experience in release automation engineering, CI/CD or related roles. Experience building and leading a software organization through product design, delivery and commercialization of consumer electronics devices. Experience recruiting and managing technical teams, including performance management. BS/MS in Computer Science. Experience in leading timeline, multi-partner initiatives. Organizational communication and coordination experience. PREFERRED 5+ years of experience with hands-on technical management, release engineering, tools engineering, DevOps, or related area.\ntokens:{\n{\ntext: 10+ years\nstart: 0\nend: 9\ntoken_start: 0\ntoken_end: 2\nentityLabel: EXPERIENCE\n}\n{\ntext: software engineering\nstart: 13\nend: 33\ntoken_start: 4\ntoken_end: 5\nentityLabel: SKILLS\n}\n{\ntext: 5+ years\nstart: 515\nend: 523\ntoken_start: 77\ntoken_end: 79\nentityLabel: EXPERIENCE\n}\n{\ntext: technical management\nstart: 552\nend: 572\ntoken_start: 86\ntoken_end: 87\nentityLabel: SKILLS\n}\n{\ntext: release engineering\nstart: 574\nend: 593\ntoken_start: 89\ntoken_end: 90\nentityLabel: SKILLS\n}\n{\ntext: tools engineering\nstart: 595\nend: 612\ntoken_start: 92\ntoken_end: 93\nentityLabel: SKILLS\n}\n{\ntext: DevOps\nstart: 614\nend: 620\ntoken_start: 95\ntoken_end: 95\nentityLabel: SKILLS\n}\n{\ntext: BS/MS\nstart: 361\nend: 366\ntoken_start: 53\ntoken_end: 55\nentityLabel: DIPLOMA\n}\n{\ntext: Computer Science\nstart: 370\nend: 386\ntoken_start: 57\ntoken_end: 58\nentityLabel: DIPLOMA_MAJOR\n}"
        prompt = Task + first_shot + final
        response = co.generate(
            model='xlarge',
            # based on the item type, we can use the examples from the list, but for now we will use the same example
            prompt= prompt,
            max_tokens=50,
            temperature=0.9,
            k=0,
            p=0.75,
            frequency_penalty=0,
            presence_penalty=0,
            stop_sequences=["--SEPARATOR--"],
            return_likelihoods='NONE'
        )
        
        res = response.generations[0].text
        # remove --SEPARATOR-- if x contains it
        #if '--SEPARATOR--' in res:
        #    res = res.replace('--SEPARATOR--', '')
        res_final = final + res
        print(res_final)
        return render_template('index.html', res_final = res_final)
        # return jsonify({"status": "sucess", "message": "Get Route for items!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', debug=True, port=port)