import asyncio
import io
import logging
import threading
import uuid
from datetime import datetime
from typing import Type
from flask import Blueprint, request, send_file, g, jsonify, abort
from xia_engine import Acl, Document, Base
from xia_api import RestApi, AuthClient, XiaRecordBook, XiaRecordItem
from xia_api import XiaFileMsg
from xia_token_flask import FlaskToken
from xia_broadcast_listener import BroadcastListener


class Restful:
    @classmethod
    def get_response(cls, rest_response):
        if isinstance(rest_response, tuple):
            return jsonify(rest_response[0]), rest_response[1]
        else:
            return jsonify(rest_response), 200

    @classmethod
    def get_action_response(cls, action_result):
        if isinstance(action_result, XiaFileMsg):
            return send_file(
                io.BytesIO(action_result.file_content),
                download_name=action_result.file_name,
                mimetype=action_result.mime_type
            )
        elif isinstance(action_result, tuple):
            # Some error occurs so the response has already been prepared
            return action_result
        elif isinstance(action_result, Base):
            return jsonify(action_result.get_display_data())
        else:
            return action_result

    @classmethod
    def translate_query(cls, query_obj):
        """Translate the http query object into xia compatible query object

        Args:
            query_obj: MultiDict

        Returns:
            dictionary

        Comments:
            The normal http parameter cannot distinguish a single item and a list with single item.
            So the single item will be presented twice at the query string: `key=value&key=value` will be
            converted to `key=[value]`
        """
        result = {}
        for key in query_obj:
            values = query_obj.getlist(key)
            if len(values) == 1:
                # Case 1: It is a single list
                result[key] = values[0]
            elif len(values) == 2 and values[0] == values[1]:
                # Case 2: A single value but should be presented as list
                result[key] = [values[0]]
            else:
                result[key] = values
        return result

    @classmethod
    def _get_record_from_g(cls, recorder: Type[XiaRecordBook]) -> XiaRecordBook:
        record_items = []
        if "request_size" in g.record:
            record_items.append(XiaRecordItem(name="request_size", int_value=g.record["request_size"]))
        if "response_size" in g.record:
            record_items.append(XiaRecordItem(name="response_size", int_value=g.record["response_size"]))
        if "end_time" in g.record:
            record_items.append(XiaRecordItem(name="process_time",
                                              float_value=g.record["end_time"]-g.record["start_time"]))
        if "batch_size" in g.record:
            record_items.append(XiaRecordItem(name="batch_size", int_value=g.record["batch_size"]))
        new_record = recorder(
            app_name=g.record["app_name"],
            class_name=g.record.get("class", ""),
            method_type=g.record.get("level", ""),
            method_name=g.record.get("method", ""),
            start_time=g.record["start_time"],
            transaction_id=g.transaction_id,
            user_name=g.record.get("user_name", ""),
            api_key_id=g.record.get("id", ""),
            remote_ip=g.record.get("ip", ""),
            status_code=g.record.get("status_code", ""),
            consumption=record_items,
        )
        return new_record

    @classmethod
    def _root_operations(cls, class_dict: dict):
        if class_dict is None:
            return abort(404)
        if request.method == "GET":
            return jsonify({"message": "Welcome to X-I-A!"})
        if request.method == "POST":
            user_acl = getattr(g, "acl", None)
            payload = request.get_json(silent=True)
            payload = [] if payload is None else payload
            g.record.update({"class": "Batch", "level": "root", "method": request.method, "batch_size": len(payload)})
            return cls.get_response(RestApi.root_post(class_dict=class_dict, payload=payload, acl=user_acl))

    @classmethod
    def _collection_operations(cls, document_class: Type[Document]):
        if document_class is None:
            return abort(404)
        g.record.update({"class": document_class.__name__, "level": "collection", "method": request.method})
        user_acl = getattr(g, "acl", None)
        if request.method == "GET":
            query_args = request.args.copy()
            query_args = cls.translate_query(query_args)
            sql = query_args.pop("_sql", None)
            dialect = query_args.pop("_dialect", None)
            model = query_args.pop("_model", None)
            id_only = str(query_args.pop("_id_only", "False")).upper() != "FALSE"
            limit = int(query_args.pop("_limit", 1000 if id_only else 50))
            id_list: str = query_args.pop("_id", None)
            catalog = query_args.pop("_catalog", None)
            lazy = str(query_args.pop("_lazy", "True")).upper() != "FALSE"
            show_hidden = str(query_args.pop("_show_hidden", "False")).upper() != "FALSE"
            if sql:
                # Analytic Operation requested
                analytic_request = {
                    "sql": str(sql), "limit": limit, "dialect": str(dialect), "payload": query_args, "model": str(model)
                }
                return cls.get_response(RestApi.collection_analyze(doc_class=document_class,
                                                                   analytic_request=analytic_request,
                                                                   acl=user_acl))
            query_args = id_list.split(",") if id_list else query_args
            return cls.get_response(RestApi.collection_get(doc_class=document_class, payload=query_args,
                                                           id_only=id_only, lazy=lazy, limit=limit, catalog=catalog,
                                                           show_hidden=show_hidden, acl=user_acl))
        elif request.method == "DELETE":
            query_args = request.args.copy()
            drop = str(query_args.pop("drop", "False")).upper() != "FALSE"
            return cls.get_response(RestApi.collection_delete(doc_class=document_class, acl=user_acl, drop=drop))
        elif request.method == "POST":
            query_args = request.args.copy()
            payload = request.get_json(silent=True)
            payload = [] if payload is None else payload
            return cls.get_response(RestApi.collection_post(doc_class=document_class, payload=payload, acl=user_acl))

    @classmethod
    def _collection_actions(cls, document_class: Type[Document], action_name: str):
        g.record.update({"class": document_class.__name__, "level": "collection", "method": "action/" + action_name})
        user_acl = getattr(g, "acl", None)
        payload = request.get_json(silent=True)
        payload = {} if payload is None else payload
        action_result = RestApi.action_post(doc_class=document_class, doc_path="", action_path=action_name,
                                            payload=payload, acl=user_acl)
        if isinstance(action_result, tuple) and len(action_result) == 2:
            # Error return is of form result, status code
            return action_result
        elif isinstance(action_result, tuple) and len(action_result) == 3:
            # Successful so will return result, sub_path, method as tuple 3 (Not useful at collection level)
            return action_result[0]
        else:
            raise RuntimeError("action result should be tuple of 2 or 3 elements")

    @classmethod
    def _document_operations(cls, document_class: Type[Document], doc_path: str):
        g.record.update({"class": document_class.__name__, "level": "document", "method": request.method})
        user_acl = getattr(g, "acl", None)
        if document_class is None:
            return abort(404)
        if request.method == "GET":
            query_args = request.args.copy()
            catalog = query_args.pop("catalog", None)
            lazy = str(query_args.pop("lazy", "False")).upper() != "FALSE"
            show_hidden = str(query_args.pop("show_hidden", "False")).upper() != "FALSE"
            return cls.get_response(RestApi.document_get(doc_class=document_class, doc_path=doc_path, acl=user_acl,
                                                         catalog=catalog, lazy=lazy, show_hidden=show_hidden))
        elif request.method == "DELETE":
            return cls.get_response(RestApi.document_delete(doc_class=document_class, doc_path=doc_path,
                                                            acl=user_acl))
        elif request.method == "POST":
            query_args = request.args.copy()
            payload = request.get_json(silent=True)
            payload = {} if payload is None else payload
            return cls.get_response(RestApi.document_post(doc_class=document_class, doc_path=doc_path, payload=payload,
                                                          acl=user_acl))
        elif request.method == "PATCH":
            query_args = request.args.copy()
            catalog = query_args.pop("catalog", None)
            payload = request.get_json(silent=True)
            payload = {} if payload is None else payload
            return cls.get_response(RestApi.document_patch(doc_class=document_class, doc_path=doc_path, payload=payload,
                                                           acl=user_acl, catalog=catalog))
        elif request.method == "PUT":
            query_args = request.args.copy()
            create = str(query_args.pop("create", "False")).upper() != "FALSE"
            payload = request.get_json(silent=True)
            payload = {} if payload is None else payload
            return cls.get_response(RestApi.document_put(doc_class=document_class, doc_path=doc_path, payload=payload,
                                                         acl=user_acl, create=create))

    @classmethod
    def _document_actions(cls, document_class: Type[Document], doc_path: str, action_path: str):
        user_acl = getattr(g, "acl", None)
        payload = request.get_json(silent=True)
        payload = {} if payload is None else payload
        action_result = RestApi.action_post(doc_class=document_class, doc_path=doc_path,
                                            action_path=action_path, payload=payload, acl=user_acl)
        if isinstance(action_result, tuple) and len(action_result) == 2:
            g.record.update({"class": document_class.__name__, "level": "document", "method": "action/" + action_path})
            return action_result
        elif isinstance(action_result, tuple) and len(action_result) == 3:
            action_result, sub_doc, method = action_result
            sub_doc = sub_doc if isinstance(sub_doc, type) else sub_doc.__class__
            g.record.update({"class": sub_doc.__name__, "level": "document", "method": "action/" + method})
            return action_result
        else:
            raise RuntimeError("action result should be tuple of 2 or 3 elements")

    @classmethod
    def get_api_blueprint(
            cls,
            path_name: str,
            resource_mapping: dict,
            token_manager: Type[FlaskToken] = None,
            auth_client: AuthClient = None,
            recorder: Type[XiaRecordBook] = None,
            listener: BroadcastListener = None
    ):
        """Get API Blueprint

        Args:
            path_name: path name to be registered in application
            resource_mapping: resource path to object mapping
            token_manager: token management
            auth_client: Authorization client. None means no security check
            recorder: Consumption report destination of each API Call
            listener: Listen to the object changes

        Returns:
            API Blueprint
        """
        api = Blueprint(path_name, __name__)
        class_mapping = {klass.__name__: klass for _, klass in resource_mapping.items()}
        resource_mapping.update(class_mapping)  # Class Mapping will overwrite manuel mapping to avoid human errors

        if isinstance(listener, BroadcastListener):
            def on_open():
                for document_class in resource_mapping.values():
                    document_class._listener_is_active = True
                print(f"Connection opened. Listener activated for {list(class_mapping)}")

            def on_message(message):
                doc_class = class_mapping.get(message["doc_class"], None)
                if doc_class:
                    doc_class.set_version(message["message"]["_id"])

            def on_close(close_status_code, close_msg):
                for document_class in resource_mapping.values():
                    document_class._listener_is_active = False
                    document_class.purge_version_table()
                print(f"Connection closed {close_status_code} {close_msg}. Listeners: {list(class_mapping)}")

            def on_error(error):
                for document_class in resource_mapping.values():
                    document_class._listener_is_active = False
                    document_class.purge_version_table()
                print(f"Connection error {error}. Listeners: {list(class_mapping)}")

            @api.record_once
            def setup_listener(state):
                threading.Thread(
                    target=asyncio.run,
                    args=(listener.listen(on_open, on_message, on_error, on_close, True), )
                ).start()

        @api.before_request
        def before_request():
            # Step 1: Prepare execution context
            g.transaction_id = str(uuid.uuid4())
            g.call_id = request.headers.get("X-Caller-Id", g.transaction_id)
            g.record = {
                "start_time": datetime.now().timestamp(),
                "request_size": 0 if not request.content_length else request.content_length,
                "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
                "transaction_id": g.transaction_id,
            }
            # Step 2:
            if token_manager:
                g.user_name, g.acl, g.user_info, token_info = token_manager.parse_access_token()
                if g.user_name and g.acl and g.user_info:
                    g.record["user_name"] = g.user_name
                    g.record["id"] = token_info.get("iss", "")
                    g.record["app_name"] = g.user_info.get("app_profile", {}).get("app_name", "")
                    return  # Authorization got, no need to continue
            # Step 3: Get Authorization from API call
            if auth_client and auth_client.api_root and auth_client.app_name:
                # Must have auth_client configured to activate authorization check
                api_id = request.headers.get("X-Api-Id")
                api_key = request.headers.get("X-Api-Key")
                g.record["app_name"] = auth_client.app_name
                if not api_key and request.authorization:
                    # Try to get the api key from basic authorization (password field)
                    api_key = request.authorization.password
                if not api_key:
                    g.acl = Acl.from_display(content=[])
                else:
                    api_detail, status_code = auth_client.get_api_acl(request.headers.get("X-Api-Key"), api_id)
                    if status_code == 200:
                        g.user_name = api_detail["user_name"]
                        g.acl = Acl.from_display(**api_detail["acl"])
                        g.record.update({k: v for k, v in api_detail.items() if k in ["user_name", "id"]})
                    else:
                        abort(401, description=api_detail)
            else:
                g.acl = None  # None means full authorization

        @api.after_request
        def after_request(response):
            g.record.update({
                "end_time": datetime.now().timestamp(),
                "response_size": response.content_length,
                "status_code": response.status_code,
            })
            if recorder:
                stat_record = Restful._get_record_from_g(recorder)
                stat_record.save()
            return response

        @api.errorhandler(401)
        def not_authenticated(e):
            return jsonify(e.description), 401

        @api.url_value_preprocessor
        def app_necessary_data(endpoint, values):
            """"""

        @api.route("/", methods=["GET", "POST"])
        def root_operations():
            return cls._root_operations(resource_mapping)

        @api.route("/<resource>", methods=["GET", "DELETE", "POST"])
        def collection_operations(resource: str):
            return cls._collection_operations(resource_mapping.get(resource, None))

        @api.route("/<resource>/<path:doc_path>", methods=["GET", "DELETE", "POST", "PATCH", "PUT"])
        def document_operations(resource: str, doc_path: str):
            if doc_path.startswith("_/"):
                # It is collection level action
                # No solution of Flask to separate collection method as an individual route
                action_name = doc_path.split("/")[-1]
                action_result = cls._collection_actions(resource_mapping.get(resource, None), action_name)
                return cls.get_action_response(action_result)
            return cls._document_operations(resource_mapping.get(resource, None), doc_path)

        @api.route("/<resource>/_/<path:action_path>", methods=["GET", "POST"], defaults={"doc_path": ""})
        @api.route("/<resource>/<path:doc_path>/_/<path:action_path>", methods=["GET", "POST"])
        def document_actions(resource: str, doc_path: str, action_path: str):
            action_result = cls._document_actions(resource_mapping.get(resource, None), doc_path, action_path)
            return cls.get_action_response(action_result)

        return api
