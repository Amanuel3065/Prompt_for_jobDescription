
from enum import unique
import os
import sys
import random

import cohere
from flask import Flask, request, jsonify, render_template

import creds

# cohere class instance
co = cohere.Client(creds.api_key)

# create an instance of the Flask class
app = Flask(__name__, template_folder='template')

"""@app.route('/')
@app.route('/api')
def home():
    """"""
    # Main page
    return render_template('index.html')
"""

# list if items
items = [{"item": "item1"}, {"item": "item2"}]



# This is a simple placeholder for eccomerce, to make it dynamic we need to use a dictionary for different types of items and use the examples based on the item type
descs = [{"document": "Bachelor's degree in Mechanical Engineering or Physical Science 3+ years track record of developing or specifying fiber optic cables and connector related products Knowledge of fiber optic component, cabling, and interconnect products, technologies, and standards Experience in statistical data analysis Experience with product life cycle management (PLM) process Experience providing solutions to problems and meeting deadlines Experience engaging stakeholders PREFERRED Advanced degree Experience using a software tool for statistical data analysis such as JMP Experience using Agile as product life-cycle management tool Data center or other mission critical development experience",
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
  }]


@app.route('/', methods=['GET', 'POST'])
def description_route():
    """description route."""
    if request.method == 'GET':
        # push the item to the list
        items.append(request.get_json())
        # return the created item
        return jsonify({
            "status": "success",
            "item": request.get_json()
        })
        # return jsonify({"status": "success", "message": "Post item!"})
    elif request.method == 'POST':
        # return generated description
        # response = co.generate(
        #     model='xlarge',
        #     prompt='Company: Casper\nProduct Name: The Wave Hybrid\nWhat is it: A mattress to improve sleep quality\nWhy is it unique: It helps with back problems\nDescription: We\'ve got your back. Literally, improving the quality of your sleep is our number one priority. We recommend checking out our Wave Hybrid mattress as it is designed specifically to provide support and pain relief.\n--SEPARATOR--\nCompany: Glossier\nProduct Name: The Beauty Bag\nWhat is it: A makeup bag\nWhy is it unique: It can hold all your essentials but also fit into your purse\nDescription: Give a very warm welcome to the newest member of the Glossier family - the Beauty Bag!! It\'s the ultimate home for your routine, with serious attention to detail. See the whole shebang on Glossier.\n--SEPARATOR--\nCompany: Cohere\nProduct Name: The FastMile\nWhat is it: A running shoe\nWhy is it unique: It\'s designed for long-distance running\nDescription:',
        #     max_tokens=50,
        #     temperature=0.9,
        #     k=0,
        #     p=0.75,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stop_sequences=["--SEPARATOR--"],
        #     return_likelihoods='NONE'
        # )

        description = request.form.get('Description')
        

        # construct final string from input
        final = f"Company: {description}"

        response = co.generate(
            model='xlarge',
            # based on the item type, we can use the examples from the list, but for now we will use the same example
            prompt=descs[0] + descs[1] + final,
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
        if '--SEPARATOR--' in res:
            res = res.replace('--SEPARATOR--', '')

        return jsonify({"status": "success", "brand_description": res})
        # return jsonify({"status": "sucess", "message": "Get Route for items!"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', debug=True, port=port)
