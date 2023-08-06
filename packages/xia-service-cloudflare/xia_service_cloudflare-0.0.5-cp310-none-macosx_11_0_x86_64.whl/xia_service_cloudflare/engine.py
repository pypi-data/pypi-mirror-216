from typing import Type
import requests
from xia_fields import StringField, OsEnvironField
from xia_engine import BaseDocument, Engine, EmbeddedDocument


class CfServiceAdmParam(EmbeddedDocument):
    env: str = StringField(description="Environment", choices=["dev", "sit", "prd"])
    api_key: str = OsEnvironField(description="Project Secret Key", prefix="CLOUDFLARE_", required=True)
    account_id: str = StringField(description="Account identifier")


class CfServiceAdmClient:
    API_ENDPOINT = "https://api.cloudflare.com/client/v4"

    @classmethod
    def get_namespaces(cls, api_key: str, account_id: str, env: str):
        api_url = f"{cls.API_ENDPOINT}/accounts/{account_id}/storage/kv/namespaces"
        api_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        result = requests.get(api_url, headers=api_headers).json()
        if not result["success"]:
            raise RuntimeError(str(result["errors"]))
        root_namespace, app_namespace, sso_namespace = "", "", ""
        for namespace in result["result"]:
            if namespace["title"].endswith(f"-srv-{env}"):
                root_namespace = namespace["id"]
            elif namespace["title"].endswith(f"-app-{env}"):
                app_namespace = namespace["id"]
            elif namespace["title"].endswith(f"-sso-{env}"):
                sso_namespace = namespace["id"]
        return root_namespace, app_namespace, sso_namespace

    def __init__(self, api_key: str, account_id: str, env: str):
        self.api_key = api_key
        self.account_id = account_id
        self.env = env
        self.root_id, self.app_id, self.sso_id = self.get_namespaces(api_key, account_id, env=env)

    def update_service_url(self, service_name: str, root_url: str, app_url: str, sso_url: str):
        api_url = f"{self.API_ENDPOINT}/accounts/{self.account_id}/storage/kv/namespaces"
        root_api_url = f"{api_url}/{self.root_id}/values/{service_name}"
        app_api_url = f"{api_url}/{self.app_id}/values/{service_name}"
        sso_api_url = f"{api_url}/{self.sso_id}/values/{service_name}"
        api_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        r = {"success": True}
        # We don't do the change if target_url is "" (special value if not presented on the update method)
        if root_url:
            r = requests.put(root_api_url, headers=api_headers, data=root_url).json()
        elif root_url is None:
            r = requests.delete(root_api_url, headers=api_headers).json()
        assert r["success"]
        if app_url:
            r = requests.put(app_api_url, headers=api_headers, data=app_url).json()
        elif app_url is None:
            r = requests.delete(app_api_url, headers=api_headers).json()
        assert r["success"]
        if sso_url:
            r = requests.put(sso_api_url, headers=api_headers, data=sso_url).json()
        elif sso_url is None:
            r = requests.delete(sso_api_url, headers=api_headers).json()
        assert r["success"]

    def get_service_url(self, service_name: str):
        api_url = f"{self.API_ENDPOINT}/accounts/{self.account_id}/storage/kv/namespaces"
        root_api_url = f"{api_url}/{self.root_id}/values/{service_name}"
        app_api_url = f"{api_url}/{self.app_id}/values/{service_name}"
        sso_api_url = f"{api_url}/{self.sso_id}/values/{service_name}"
        api_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        return {
            "root_url": requests.get(root_api_url, headers=api_headers).content.decode(),
            "app_url": requests.get(app_api_url, headers=api_headers).content.decode(),
            "sso_url": requests.get(sso_api_url, headers=api_headers).content.decode()
        }


class CfServiceAdmEngine(Engine):
    engine_param = "cf_service_adm"
    engine_connector = CfServiceAdmClient
    engine_connector_class = CfServiceAdmParam

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        if doc_id is None:
            sample_doc = document_class.from_db(**db_content)
            doc_id = sample_doc.get_id()
        db_con = cls.get_connection(document_class)
        db_con.update_service_url(
            service_name=db_content["service_name"],
            root_url=db_content.get("root_service", None),
            app_url=db_content.get("app_service", None),
            sso_url=db_content.get("sso_service", None)
        )
        return doc_id

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict):
        db_con = cls.get_connection(document_class)
        db_con.update_service_url(
            service_name=db_content["service_name"],
            root_url=db_content.get("root_service", None),
            app_url=db_content.get("app_service", None),
            sso_url=db_content.get("sso_service", None)
        )
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        db_con = cls.get_connection(_document_class)
        key_content = _document_class.id_to_dict(_doc_id)
        db_con.update_service_url(
            service_name=key_content["service_name"],
            root_url=kwargs.get("root_service", ""),
            app_url=kwargs.get("app_service", ""),
            sso_url=kwargs.get("sso_service", "")
        )
        return key_content

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        key_content = document_class.id_to_dict(doc_id)
        db_con.update_service_url(
            service_name=key_content["service_name"],
            root_url=None,
            app_url=None,
            sso_url=None
        )
