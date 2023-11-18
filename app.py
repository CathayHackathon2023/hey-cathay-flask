from flask import Flask
from flask import request
from flask import jsonify
import json
import pymongo
from bson.objectid import ObjectId

# Google AI modules
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

CONNECTION_STIRNG = "mongodb://127.0.0.1:27017"
mongo_client = pymongo.MongoClient(CONNECTION_STIRNG)
db = mongo_client["cathay_db"]
flights = db["flights"]

app = Flask(__name__)

with open('classifier_dataset.json', 'r') as f:
    data = json.load(f)

vertexai.init(
    project="heycathay-405507", 
    location="us-central1",
    )
examples = []
for example in data:
    examples.append(InputOutputTextPair(
        input_text=example["input_text"],
        output_text= example["output_text"]
    ))
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}

chat = chat_model.start_chat(
    context="""A user is interacting with a travel app which can help with certain functions: for example in can navigate to certain screens, it can help book a flight, and it can show the food in a flight. 
                To book a flight the user has to give their origin airport, arrival airport, flight date, optionally return date, and the type of request it is.
            """,
    examples=examples
)

naturalizer = chat_model.start_chat(
    context="""
                Imagine you are an assistant for a passenger, you will be presented with information and respond with a summarized version. 
                The response should be natural language that can be understod by passenger.   
          """
)


@app.route("/")
def home():
    response = chat.send_message("""What kind of food is offered in my current flight""", **parameters)
    print(f"Response from Model: {response.text}")
    return {"message": "Welcome to Hey Cathay"}, 200

@app.route("/api/input", methods=["POST"])
def input():
    if request.method == "POST":
        question = request.json.get("input")
        response = chat.send_message(question, **parameters)
        print(f"Response from Model: {response.text}")
        return {"response": response.text}, 200
    
@app.route("/api/naturalize", methods=["POST"])
def natarulize():
    if request.method == "POST":
        input = request.json.get("input")
        response = naturalizer.send_message(input, **parameters)
        return {"response": response.text}, 200
    
@app.route("/api/flights")
def get_flights_by_filters():
    if request.method == "GET":
        data = list(flights.find())
        for flight in data:
            flight["_id"] = str(flight["_id"])
        return data, 200
    
if __name__=="__main__":
    app.run(debug=True)