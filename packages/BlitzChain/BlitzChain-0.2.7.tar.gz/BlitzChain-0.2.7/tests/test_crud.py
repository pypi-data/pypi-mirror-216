"""Testing
"""

import blitzchain 
import os
client = blitzchain.Client(os.environ["TWILIX_API_KEY"])
collection = client.Collection("example")
result = collection.insert_objects([{"text": "example"}])
print(result)
