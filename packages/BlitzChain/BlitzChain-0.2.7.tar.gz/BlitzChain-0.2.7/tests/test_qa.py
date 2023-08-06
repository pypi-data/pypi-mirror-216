"""Testing
"""
import blitzchain 
import os
client = blitzchain.Client(os.environ["TWILIX_API_KEY"])
collection = client.Collection("example")
result = collection.generative_qa(
    "testing", ["text"]
)
print(result)

# import requests
# response = requests.post(
#     "https://app.twilix.io/api/v1/collection/generative-qa",
#     headers={
#         "Authorization": "Bearer " + os.environ["TWILIX_API_KEY"],
#         "Content-Type": "application/json"
#     },
#     json={
#         "collection": "samplePdf2",
#         "userInput": "why",
#         "answerFields": ["text"]
#     }
# )
# print(response.content)
