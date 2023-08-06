"""The API behind BlitzChain
"""
import requests
from .splitter import WordSplitter

def get_json_response(response):
    try:
        return response.json()
    except Exception as e:
        return response.content

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
        fields_for_vectorization: list=None,
        split_on_field: str = None,
        wait_to_finish=True
    ):
        if wait_to_finish:
            url = self.base_url + "collection/bulk-insert"
        else:
            raise NotImplementedError
            # url = self.base_url + "collection/async-bulk-insert"
        
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "objects": objects,
                "fieldsForVectorization": fields_for_vectorization,
                "splitOnField": split_on_field
            }

        )
        if not wait_to_finish:
            return response.status_code == 200, "Request failed - please make sure parameters are correct."
        return get_json_response(response)
    
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
        return get_json_response(response)

    
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
        return get_json_response(response)

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
        return get_json_response(response)

    def list_objects(self, limit: int=5, offset: int=0, 
            fields: list=None, where=None, sort:list=None):
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
        return get_json_response(response)
    
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
        return get_json_response(response)
