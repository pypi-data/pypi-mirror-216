from typing import Type, Union
from functools import wraps, lru_cache
import json
import requests
from xia_engine import Base, Document
from xia_engine import OutOfScopeError, AuthorizationError


def auth_required(func):
    @wraps(func)
    def need_auth(*args, **kwargs):
        if kwargs.get("acl", None) is not None and not kwargs["acl"].content:
            raise AuthorizationError("User has empty ACL")
        return func(*args, **kwargs)
    return need_auth


def auth_required_async(func):
    @wraps(func)
    async def need_auth(*args, **kwargs):
        if kwargs.get("acl", None) is not None and not kwargs["acl"].content:
            raise AuthorizationError("User has empty ACL")
        return await func(*args, **kwargs)
    return need_auth


class AuthClient:
    def __init__(self, api_root: str = "https://auth.x-i-a.com/api/"):
        self.api_root = api_root
        self.user_root = api_root + "user"
        self.role_root = api_root + "role"
        self.matrix_root = api_root + "matrix"

    def get_api_acl(self, api_key: str, app_name: str, api_id: str = ""):
        """Get Access Control List of API

        Args:
            api_key: API Key
            api_id: API ID
            app_name: app_name to check the API Key

        Returns:
            API Detail or Error Message
        """
        r = requests.post(self.role_root + f"/_/get_api_acl", json={"api_key": api_key, "app_name": app_name})
        try:
            result = r.json()
        except Exception as e:
            return {"message": e.args[0], "trace": r.content.decode()}, r.status_code
        if r.status_code == 200 and api_id and result["id"] != api_id:
            # An extra check for the API ID if API ID is provided
            return {"message": f"API ID {api_id} and {result['id']} don't match"}, 401
        if r.status_code >= 300 and "message" not in result:
            # It is not a standard XIA error
            return {"message": f"API Endpoint returns code {r.status_code}", "trace": r.content.decode()}, r.status_code
        # Everything seems to be good
        return r.json(), r.status_code


class Broadcaster:
    """Broadcasting document into subscribers (via websocket)"""
    active_connections = {}  #: Connection library, organized by doc_class

    @classmethod
    async def accept(cls, websocket):
        """Accept Event of a websocket event

        Args:
            websocket: websocket object
        """

    @classmethod
    async def subscribe(cls,
                        websocket,
                        class_name: str,
                        data_scope: list = None,
                        catalog: dict = None,
                        show_hidden: bool = False,
                        start_seq: str = "",
                        acl=None,
                        **kwargs):
        """Subscribe to a connection

        Args:
            websocket: websocket object
            class_name: Document Class Name
            data_scope: The subset of data to be shown
            catalog: data to be shown
            show_hidden: Show hidden data or not
            start_seq: Not interested on the message before this start sequence
            acl: User access Control

        Comments:
            * Know message to route to which client
            * Know the message content to be sent
        """
        if class_name not in cls.active_connections:
            cls.active_connections[class_name] = {}
        sub_params = {
            "data_scope": data_scope,
            "catalog": catalog,
            "show_hidden": show_hidden,
            "start_seq": start_seq,
            "acl": acl,
            **kwargs
        }
        cls.active_connections[class_name][websocket] = sub_params
        return sub_params

    @classmethod
    def disconnect(cls, websocket):
        """Disconnect the subscriber

        Args:
            websocket:
        """
        for _, doc_class_subscriber in cls.active_connections.items():
            doc_class_subscriber.pop(websocket, None)

    @classmethod
    async def send_message_async(cls, websocket, message: str):
        """Send message to the target websocket

        Args:
            websocket: websocket object
            message (str): message content
        """

    @classmethod
    async def send_json_async(cls, websocket, content: dict):
        """Send json message in async mode

        Args:
            websocket: websocket object
            content (dict): dictionary to be jsonify
        """
        message = json.dumps(content, ensure_ascii=False)
        # print(message)
        await cls.send_message_async(websocket, message)

    @classmethod
    def get_message_body(cls, doc: Document, data_scope: list, catalog: dict, show_hidden: bool) -> Union[dict, None]:
        """Get message body from document

        Args:
            doc: Document object holding contents
            data_scope: data scope
            catalog: data catalog
            show_hidden: Should show hidden value or not

        Returns:
            json object if data on the scope else None
        """
        try:
            doc.check_scope(data_scope)
            return doc.get_display_data(catalog=catalog, show_hidden=show_hidden)
        except OutOfScopeError:
            return None

    @classmethod
    def subscriber_is_connected(cls, websocket):
        """Check if the websocket is connected

        Args:
            websocket: websocket object
        """
        return True

    @classmethod
    def check_subscriber_acl(cls, doc: Document, acl):
        """Check if subscriber has right to get the data

        Args:
            doc: document to control
            acl: User access List

        Returns:
            True if use has authorization else False
        """
        return doc.check_acl(acl, "read", doc, False)

    @classmethod
    @auth_required_async
    async def document_sent_async(cls, /, doc: Document, op: str, seq: str):
        """ Sending document in async mode

        Args:
            doc: Document object
            op: Operation Type
            seq: Create Sequence
        """
        doc_class = doc.__class__.__name__
        # print(doc_class)
        doc_class_subscriber = cls.active_connections.get(doc_class, {})
        # print(doc_class_subscriber.values())
        closed_subscribers = []
        if not doc_class_subscriber:
            return  # No subscriber, let's pass
        for websocket, param in doc_class_subscriber.items():
            # Step 1: Check if connection is still open
            if not cls.subscriber_is_connected(websocket):
                # print("subscriber closed")
                closed_subscribers.append(websocket)
            # Step 2: Check if the sequence is big enough
            if seq < param["start_seq"]:
                # print("older than requested start_seq")
                return
            # Step 3: Check if the subscriber's ACL
            if not cls.check_subscriber_acl(doc, param["acl"]):
                # print("subscribe has not authorization")
                continue
            # Step 4: Get and send the message
            message = cls.get_message_body(doc, param["data_scope"], param["catalog"], param["show_hidden"])
            if message:
                await cls.send_json_async(websocket, {"doc_class": doc_class, "op": op, "seq": seq, "message": message})
            # else:
                # print("No message")
        for closed_subscriber in closed_subscribers:
            cls.disconnect(closed_subscriber)
