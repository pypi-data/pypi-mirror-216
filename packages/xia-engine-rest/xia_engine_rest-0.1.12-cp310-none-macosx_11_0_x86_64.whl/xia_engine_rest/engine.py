from typing import Type
from functools import wraps
import base64
import requests
from xia_fields import ByteField, StringField, OsEnvironField
from xia_engine import BaseDocument, Engine, EmbeddedDocument
from xia_engine.exception import *


class RestConnectParam(EmbeddedDocument):
    api_endpoint: str = StringField(description="API Endpoint", default="https://test.com/api/")
    api_key: str = StringField(description="API Key Directly Passed")
    api_key_env: bytes = OsEnvironField(description="API Key Stored in Environment Variable")


def rest_connect(api_endpoint: str, api_key: str = None, api_key_env: str = None):
    api_key = api_key_env if api_key_env else api_key
    api_headers = {"X-Api-Key": api_key} if api_key else {}
    return api_endpoint, api_headers


class RequestHttpClient:
    @classmethod
    def get(cls, *arg, **kwargs):
        return requests.get(*arg, **kwargs)


class RestEngine(Engine):
    _error_mapping = {err.__name__: err for err in Exception.__subclasses__() + XiaError.__subclasses__()}

    engine_unique_check = True  #: Unique check should be applied in backend

    engine_param = "rest"
    engine_db_shared = False
    engine_connector_class = RestConnectParam
    engine_connector = rest_connect

    http_client = RequestHttpClient

    encoders = {
        ByteField: lambda x: base64.b64encode(x).decode()
    }

    decoders = {
        ByteField: lambda x: base64.b64decode(x.encode())
    }

    @classmethod
    def translate_query(cls, payload: dict):
        result = {}
        for key, value in payload.items():
            if isinstance(value, list) and len(value) == 1:
                # To mark a single element list in query stream, we need to repeat it
                result[key] = value + value
            else:
                result[key] = value
        return result

    @classmethod
    def raise_error(cls, r: requests.Response):
        """Http error should be raised to a correct error type

        Args:
            r: Response object

        Returns:
            None if all goes well
            ExceptionObject + Error Trace when meeting errors
        """
        if r.status_code < 300:
            return  # Everything goes well
        try:
            error_info = r.json()
        except Exception:
            raise ServerError(f"API Endpoint returns code {r.status_code}", r.content.decode())
        if not isinstance(error_info, dict) or "type" not in error_info:
            raise ServerError(f"API Endpoint returns code {r.status_code}", r.content.decode())
        error_type = cls._error_mapping.get(error_info["type"], None)
        if not error_type:
            raise ServerError(f"API Endpoint returns code {r.status_code}", r.content.decode())
        raise error_type(error_info.get("message", ""), error_info.get("trace", ""))

    @classmethod
    def search(cls, document_class: Type[BaseDocument], *args, _acl_queries: list = None, _limit: int = 50, **kwargs):
        _acl_queries = [{}] if not _acl_queries else _acl_queries
        api_endpoint, api_headers = cls.get_connection(document_class)
        params = cls.translate_query(kwargs)
        # data_scope should be defined in the api endpoint. Avoid redundant apply
        if len(args) > 0:
            params["_show_hidden"] = True  # We will always show hidden field in api call
            params["_limit"] = _limit
            params["_id"] = ",".join([doc_id for doc_id in [arg for arg in args if arg]])
            r = requests.get(api_endpoint, headers=api_headers, params=params)
            if r.status_code == 200:
                for doc_dict in r.json():
                    db_content = document_class.from_display(**doc_dict).to_db()
                    db_content["_id"] = doc_dict["_id"]
                    yield db_content
        else:
            params["_show_hidden"] = True  # We will always show hidden field in api call
            r = requests.get(api_endpoint, headers=api_headers, params=params)
            cls.raise_error(r)
            for item in r.json():
                db_content = document_class.from_display(**item).to_db()
                yield db_content

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.post(api_endpoint, headers=api_headers, json=[db_content])
        cls.raise_error(r)
        created_docs = r.json()
        if not created_docs:
            raise ServerError("Document cannot be saved")
        created_doc = document_class.from_display(**created_docs[0])
        return created_doc.get_id()

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.get(api_endpoint + "/_id/" + doc_id, headers=api_headers, params={"_show_hidden": True})
        cls.raise_error(r)
        result = document_class.from_display(**r.json()).to_db()
        return result

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.put(api_endpoint + "/_id/" + doc_id, headers=api_headers, json=db_content)
        cls.raise_error(r)
        updated_doc = document_class.from_display(**r.json())
        return updated_doc.get_id()

    @classmethod
    def update(cls, document_class: Type[BaseDocument], doc_id: str, **kwargs):
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.patch(api_endpoint + "/_id/" + doc_id, headers=api_headers, json=kwargs)
        cls.raise_error(r)
        result = document_class.from_display(**r.json()).to_db()
        return result

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.delete(api_endpoint + "/_id/" + doc_id, headers=api_headers)
        cls.raise_error(r)
        return r.json()

    @classmethod
    def truncate(cls, document_class: Type[BaseDocument]):
        cls.drop(document_class)

    @classmethod
    def drop(cls, document_class: Type[BaseDocument]):
        api_endpoint, api_headers = cls.get_connection(document_class)
        r = requests.delete(api_endpoint, headers=api_headers, params={"drop": True})
        cls.raise_error(r)

    @classmethod
    def batch(cls, operations: list, originals: dict):
        if not operations:
            return True, ""  # Empty operation
        api_endpoint, api_headers = cls.get_connection(next(iter(operations))["cls"])
        api_endpoint = "/".join(api_endpoint.split("/")[:-1])  # Get root api endpoint instead of resource endpoint
        payload = []
        for operation in operations:
            payload_line = {
                "name": cls.get_connection(operation["cls"])[0].split("/")[-1],
                "op": operation["op"], "id": operation["doc_id"], "content": operation.get("content", {})
            }
            payload.append(payload_line)
        r = requests.post(api_endpoint, headers=api_headers, json=payload)
        cls.raise_error(r)
        return True, ""
