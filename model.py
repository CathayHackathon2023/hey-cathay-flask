import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

vertexai.init(project="heycathay-405507", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""A user is interacting with a travel app which can help with certain functions: for example in can navigate to certain screens, it can help book a flight, and it can show the food in a flight. To book a flight the user has to give their origin airport, arrival airport, flight date, optionally return date, and the type of request it is.""",
    examples=[
        InputOutputTextPair(
            input_text="""I want to see my flight""",
            output_text="""Flight"""
        ),
        InputOutputTextPair(
            input_text="""What are my flights?""",
            output_text="""Flights"""
        ),
        InputOutputTextPair(
            input_text="""What food is offered on my flight""",
            output_text="""Food"""
        )
    ]
)
response = chat.send_message("""What are some of the flights that I have coming up""", **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""I have a flight coming up today where should I go """, **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""What kind of food is offered in my current flight""", **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""
What kind of food is offered in my current flight""", **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""
What kind of food is offered in my current flight""", **parameters)
print(f"Response from Model: {response.text}")