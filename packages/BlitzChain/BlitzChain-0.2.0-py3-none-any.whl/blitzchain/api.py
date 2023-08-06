"""The API behind BlitzChain
"""
import requests

class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def Collection(self, collection_name: str):
        return Collection(api_key=self.api_key, collection_name=collection_name)

class Collection:
    def __init__(self, api_key: str, collection_name: str):
        self.collection_name = collection_name
        self.api_key = api_key
        self.base_url = "https://app.twilix.io/api/v1/"
    
    def insert_objects(
        self,
        objects: list,
        fields_to_vectorize: list=None,
        field_to_split: str = None,
        wait_to_finish=False
    ):
        if wait_to_finish:
            url = self.base_url + "collection/bulk-insert"
        else:
            url = self.base_url + "collection/async-bulk-insert"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "objects": objects,
                "fieldsToVectorize": fields_to_vectorize,
                "fieldToSplit": field_to_split
            }

        )
        print(response.content.decode())
        if not wait_to_finish:
            return response.status_code == 200, "Request failed - please make sure parameters are correct."
        return response.json()
    
    def insert_pdf(self, url: str):
        api_url = self.base_url + "collection/insert-pdf"
        print(api_url)
        response = requests.post(
            api_url,
            headers={
                # "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "url": url
            }
        )
        print(response.content.decode())
        return response.json()

    
    def generative_qa(self, user_input: str, answer_fields: list,
        conversation_id: str=None, limit: int=5, fields: list=None,
        include_rerank: bool=False, minimum_rerank_score: float=0.7):
        """Get an answer based on a question that you ask.
        """
        url =  self.base_url + "collection/generative-qa"
        print(url)
        data={
            "collection": self.collection_name,
            "userInput": user_input,
            "answerFields": answer_fields,
            "limit": limit,
            "fields": fields,
            "includeRerank": include_rerank,
            "minimumRerankScore": minimum_rerank_score
        }
        if conversation_id:
            data["conversationID"] = conversation_id
        print(data)
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json=data
        )
        return response.json()

    def generative_code_qa(self, user_input: str, answer_fields: list,
        conversation_id: str=None, limit: int=5, fields: list=None,
        include_rerank: bool=False, minimum_rerank_score: float=0.7):
        """Get an answer based on a question that you ask.
        """
        url =  self.base_url + "collection/generative-code-qa"
        print(url)
        data={
            "collection": self.collection_name,
            "userInput": user_input,
            "answerFields": answer_fields,
            "limit": limit,
            "fields": fields,
            "includeRerank": include_rerank,
            "minimumRerankScore": minimum_rerank_score
        }
        if conversation_id:
            data["conversationID"] = conversation_id
        print(data)
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json=data
        )
        return response.json()

    def list_objects(self, limit: int=5, offset: int=0, fields: list=None,
                     where=None, sort=list):
        api_url = self.base_url + "object/list"
        print(api_url)
        response = requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "limit": limit,
                "offset": offset,
                "fields": fields,
                "where": where,
                "sort": sort
            }
        )
        print(response.content.decode())
        return response.json()
    
    def count(self):
        api_url = self.base_url + "object/count"
        response = requests.get(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            params={
                "collection": self.collection_name,
            }
        )
        print(response.content.decode())
        return response.json()
