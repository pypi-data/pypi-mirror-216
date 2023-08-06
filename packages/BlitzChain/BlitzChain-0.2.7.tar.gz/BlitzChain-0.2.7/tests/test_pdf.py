"""Testing
"""

import blitzchain 
import os
client = blitzchain.Client(os.environ["TWILIX_API_KEY"])
collection = client.Collection("examplePdf2")
result = collection.insert_pdf(url="https://www.founders.unsw.edu.au/sites/default/files/documents/PFC%20terms%20and%20conditions_updated_2022.pdf")
print(result)
# import requests
# response = requests.post(
#     url="https://app.twilix.io/api/v1/collection/insert-pdf",
#     headers={"Authorization": "bearer " + os.environ["TWILIX_API_KEY"]},
#     json={
#         "collection": "examplePdf2",
#         "url": "https://www.founders.unsw.edu.au/sites/default/files/documents/PFC%20terms%20and%20conditions_updated_2022.pdf"
#     }
# )
# print(response.content)