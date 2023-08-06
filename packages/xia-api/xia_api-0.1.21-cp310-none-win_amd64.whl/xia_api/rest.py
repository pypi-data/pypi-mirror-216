import json
import traceback
from functools import wraps
from typing import Type, Union
from xia_engine import Base, Document, ListRuntime, Batch
from xia_engine import XiaError, NotFoundError, ConflictError, BadRequestError, AuthorizationError
from xia_api.message import XiaCollectionDeleteMsg, XiaDocumentDeleteMsg
from xia_api.message import XiaErrorMessage


def error_handle(func):
    @wraps(func)
    def handled_error(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ValueError, TypeError, RuntimeError, XiaError) as e:
            err_document = XiaErrorMessage(
                type=e.__class__.__name__,
                message=e.args[0],
                trace=traceback.format_exc()[:1024],
            )
            if isinstance(e, XiaError):
                return err_document.get_display_data(), e.status_code
            else:
                return err_document.get_display_data(), 400
    return handled_error


def auth_required(func):
    @wraps(func)
    def need_auth(*args, **kwargs):
        if kwargs.get("acl", None) is not None and not kwargs["acl"].content:
            raise AuthorizationError("User has empty ACL")
        return func(*args, **kwargs)
    return need_auth


class RestApi:
    """Definition of API Implementation of xia-universe related objects

    Url Path Full Version: https://hostname:port/prefix/resource/path_to_doc/_/field_path/action
        * hostname:port : Service location
        * prefix: fixed api prefix, /api/v1/ for example
        * resource: Class Type, should be case-insensitive
        * path_to_doc: Locating a document
            * Could use /_id/id_number to search by id
            * Could use /field_name/field_value to search by value
        * /_/: a seperator to separate the document part and action part
        * action_path: Action of which sub-object should be called
            * path could be composed by multi-level. In the case of list field, fetch by using keyword has priority.
        * action: the method should be called

    Main HTTP -> class method Map:
        * root_(post): https://hostname:port/prefix/
        * collection_(get, post, delete): https://hostname:port/prefix/resource
        * document_(get, post, delete, put, patch): https://hostname:port/prefix/resource/path_to_doc
        * action_post: https://hostname:port/prefix/resource/path_to_doc/_/path_to_object/action

    """
    @classmethod
    def _parse_catalog(cls, catalog: Union[str, dict, type(None)]):
        if catalog is None or isinstance(catalog, dict):
            return catalog
        else:
            return json.loads(catalog)

    @classmethod
    @error_handle
    @auth_required
    def root_post(cls, class_dict: dict, payload: list, acl=None):
        """Batch operation

        Args:
            class_dict: dictionary of document classes
            payload: list of operations to be performed
            acl: Access Control List

        Returns:
            * successful: Empty message, 200
            * failed: error message, 500

        Format of operation (item of payload):
            * name: Name of the document class
            * id: Document ID
            * op: "I", "U", "D", "S"
            * content: content in display format
        """
        if not class_dict:
            return "No class mapping found", 400
        batch = Batch(engine=class_dict[next(iter(class_dict))]._engine)
        for operation in payload:
            if any(key not in operation for key in ["name", "id", "op"]):
                return f"Wrong payload line format, need have name, id, op", 400
            if operation["name"] not in class_dict:
                return f"Class {operation['name']} not found", 400
            if operation["op"] == "I":  # Insert
                doc = class_dict[operation["name"]].from_display(**operation['content'])
                doc.save(batch=batch, acl=acl)
            elif operation["op"] == "S":  # Set
                doc = class_dict[operation["name"]].from_display(**operation['content'])
                doc._id = doc.calculate_id() if doc._key_fields else operation['id']
                doc.save(batch=batch, acl=acl)
            elif operation["op"] == "U":  # Update
                doc = class_dict[operation["name"]]()
                doc._id = operation['id']
                doc.update(_batch=batch, _acl=acl, **operation["content"])
            elif operation["op"] == "D":  # Delete
                doc = class_dict[operation["name"]]()
                doc._id = operation['id']
                doc.delete(batch=batch, acl=acl)
            else:
                return f"Operation {operation['op']} is not supported", 400
        result, message = batch.commit()
        if result:
            return "", 200  # Success
        else:
            return message, 500  # Failed at server side

    @classmethod
    @error_handle
    @auth_required
    def collection_get(cls, /, doc_class: Type[Document], payload=None, acl=None, limit=None, id_only=False,
                       catalog=None, lazy=True, show_hidden: bool = False):
        """Search Document

        Args:
            lazy: Don't load the reference or external data if they are not loaded
            catalog: Display Catalog
            limit: How many documents should be returned
            id_only: Only return a list of id (Accelerator when there is a search engine)
            acl: Access Control List
            payload: Searching payload
            doc_class: Document Class
            show_hidden: Show hidden field or not

        Returns:
            document_list, or id_list if id_only is True
        """
        if isinstance(payload, list) and id_only:
            return payload, 204   # Do nothing and just return the original result
        payload = {} if not payload else payload
        catalog = cls._parse_catalog(catalog)
        if limit is None:  # Default value of limit depends on the request type
            limit = 1000 if id_only else 50
        if isinstance(payload, dict):
            document_list = doc_class.objects(_acl=acl, _limit=limit, _id_only=id_only, **payload)
        elif isinstance(payload, list):
            if any(not isinstance(item, str) for item in payload):
                return "Document ID must be string", 400
            document_list = doc_class.objects(*payload, _acl=acl, _limit=limit)
        else:
            return "payload should be list or dictionary", 400
        if id_only:
            return list(document_list), 200
        result = [doc.get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden) for doc in document_list]
        return result, 200

    @classmethod
    @error_handle
    @auth_required
    def collection_analyze(cls, /, doc_class: Type[Document], analytic_request=None, acl=None):
        """Analyze Document

        Args:
            doc_class: Document Class
            analytic_request: Analytic Request
            acl: Access Control List

        Returns:
            document_list
        """
        analytic_request = {} if not analytic_request else analytic_request
        result = doc_class.analyze(analytic_request=analytic_request, acl=acl)
        return result, 200

    @classmethod
    @error_handle
    @auth_required
    def collection_post(cls, /, doc_class: Type[Document], payload: list, acl=None):
        """Massive document creation

        Args:
            doc_class: Document Class
            payload: list of document to be created
            acl: Access Control List

        Returns:
            Display form of saved document (lazy mode forced to be true, and will return whole documents)
        """
        saved_docs = []
        for document in payload:
            new_doc = doc_class.from_display(**document)
            saved_docs.append(new_doc.save(acl=acl))
        return [doc.get_display_data() for doc in saved_docs], 200

    @classmethod
    @error_handle
    @auth_required
    def collection_delete(cls, /, doc_class: Type[Document], acl=None, drop=False):
        """Drop a collection

        Args:
            drop: Using Drop (Not cascade operation in that case)
            acl: Access Control List
            doc_class: Document Class

        Returns:
            document_list
        """
        if drop:
            doc_class.drop(acl=acl)
            delete_msg = XiaCollectionDeleteMsg.from_display(collection=doc_class.get_collection_name(), drop=True)
        else:
            delete_results = doc_class.delete_all(acl=acl)
            deleted, ignored = [], {}
            for delete_result in delete_results:
                if delete_result["result"] == 200:
                    deleted.append(delete_result)
                else:
                    collection_errors = ignored.get(delete_result["collection"], {})
                    error_counter = collection_errors.get(delete_result["result"], 0) + 1
                    collection_errors.update({delete_result["result"]: error_counter})
                    ignored.update({delete_result["collection"]: collection_errors})
            delete_msg = XiaCollectionDeleteMsg.from_display(
                collection=doc_class.get_collection_name(),
                drop=False,
                deleted=deleted,
                ignored=ignored
            )
        return delete_msg.get_display_data(), 200

    @classmethod
    def _get_document_from_path(cls, doc_class: Type[Document], doc_path: str, acl=None):
        """Get document from a given path

        Args:
            acl: Access Control List
            doc_class: Document Class
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
        """
        paths = [path for path in doc_path.split('/') if path]  # Split and remove empties
        if paths[0] == "_id":
            return doc_class.load(paths[1], _acl=acl)
        else:
            load_dict = {paths[2*i]: paths[2*i + 1] for i in range(len(paths) // 2) if not paths[2*i].startswith("_")}
            return doc_class.load(_acl=acl, **load_dict)

    @classmethod
    def _get_method_from_path(cls, doc: Base, action_path: str, acl=None):
        """Get method of a document from a given path

        Args:
            acl: Access Control List
            doc: Document object
            action_path: path to document, could be /field1/subfield/action

        Returns:
            document object, action name
        """
        if not isinstance(doc, Base):
            raise BadRequestError(f"Parameter has a wrong type: {type(doc)},"
                                  f"should be a document or an embedded document")
        if "/" in action_path:
            field_name, sub_path = action_path.split("/", 1)
            sub_doc = getattr(doc, field_name, None)
            if sub_doc is None:
                raise BadRequestError(f"field {field_name} not found for parsing {action_path}")
            elif isinstance(sub_doc, Base):
                return cls._get_method_from_path(sub_doc, sub_path, acl)
            elif isinstance(sub_doc, list):
                member_name, member_path = sub_path.split("/", 1)
                member_doc = sub_doc[int(member_name)]
                return cls._get_method_from_path(member_doc, member_path, acl)
            elif isinstance(sub_doc, ListRuntime):
                member_name, member_path = sub_path.split("/", 1)
                if member_name in sub_doc:
                    member_doc = sub_doc[member_name]
                elif member_name.isdigit():
                    member_doc = sub_doc[int(member_name)]
                else:
                    raise NotFoundError(f"Cannot found {member_name} in {field_name}")
                return cls._get_method_from_path(member_doc, member_path, acl)
        else:
            return doc, action_path

    @classmethod
    @error_handle
    @auth_required
    def document_get(cls, /, doc_class: Type[Document], doc_path: str, acl=None,
                     catalog=None, lazy=True, show_hidden: bool = False):
        """Get a document

        Args:
            lazy: Don't load the reference or external data if they are not loaded
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            catalog: Display Catalog
            acl: Access Control List
            doc_class: Document Class
            show_hidden: Show hidden field or not

        Returns:
            Display form of the document
        """
        doc = cls._get_document_from_path(doc_class, doc_path, acl)
        if doc is None:
            raise NotFoundError(f"Cannot find the document {doc_class.__name__}/{doc_path}")
        catalog = cls._parse_catalog(catalog)
        result = doc.get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden)
        return result, 200

    @classmethod
    @error_handle
    @auth_required
    def document_delete(cls, /, doc_class: Type[Document], doc_path: str, acl=None):
        """Delete a document

        Args:
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            acl: Access Control List
            doc_class: Document Class
        """
        doc = cls._get_document_from_path(doc_class, doc_path, acl)
        if doc is None:
            raise NotFoundError(f"Cannot find the document {doc_class.__name__}/{doc_path}")
        if isinstance(doc, doc_class):
            delete_results = doc.delete(acl=acl)
            return [XiaDocumentDeleteMsg.from_display(**result).get_display_data() for result in delete_results], 200
        else:
            raise BadRequestError(f"Document of type {doc.__class__.__name__} is not of type {doc_class.__name__}")

    @classmethod
    @error_handle
    @auth_required
    def document_patch(cls, /, doc_class: Type[Document], payload: dict, catalog: None, doc_path: str, acl=None):
        """Update some fields of a document

        Args:
            doc_class: Document Class
            catalog: Display Catalog
            payload: Field to be modified and its new value
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            acl: Access Control List

        Returns:
            Display form of modified document (lazy mode forced to be true)
        """
        doc = cls._get_document_from_path(doc_class, doc_path, acl)
        if doc is None:
            raise NotFoundError(f"Cannot find the document {doc_class.__name__}/{doc_path}")
        catalog = cls._parse_catalog(catalog)
        doc = doc.update(_acl=acl, **payload)
        return doc.get_display_data(catalog=catalog), 200

    @classmethod
    @error_handle
    @auth_required
    def document_put(cls, /, doc_class: Type[Document], payload: dict, doc_path: str, create=False, acl=None):
        """Update the whole document

        Args:
            doc_class: Document Class
            create: Create the document if not exist
            payload: Field to be modified and its new value
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            acl: Access Control List

        Returns:
            Display form of modified document (lazy mode forced to be true, and will return whole document)
        """
        old_doc = cls._get_document_from_path(doc_class, doc_path)  # acl is not passed here
        if old_doc is None:
            if not create:
                raise ValueError(f"Cannot find the document {doc_class.__name__}/{doc_path}, "
                                 f"set create=True if you need to create a new one")
            else:
                return cls.document_post(doc_class=doc_class, payload=payload, doc_path=doc_path, acl=acl)
        new_doc = doc_class.from_display(**payload)
        if new_doc._key_fields and new_doc.calculate_id() != old_doc.get_id():
            raise ValueError(f"Update primary key from {old_doc.get_id()} to {new_doc.calculate_id()} is not supported")
        new_doc._id = old_doc.get_id()
        new_doc = new_doc.save(acl=acl)
        return new_doc.get_display_data(), 200

    @classmethod
    @error_handle
    @auth_required
    def document_post(cls, /, doc_class: Type[Document], payload: dict, doc_path: str, acl=None):
        """Save the new document if not exist

        Args:
            doc_class: Document Class
            payload: Field to be modified and its new value
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            acl: Access Control List

        Returns:
            Display form of saved document (lazy mode forced to be true, and will return whole document)
        """
        old_doc = cls._get_document_from_path(doc_class, doc_path)  # acl is not passed here
        if old_doc is not None:
            raise ConflictError(f"Document already exists {doc_class.__name__}/{doc_path}")
        if not payload:
            raise ValueError(f"Empty payload")
        create_status = cls.collection_post(doc_class=doc_class, payload=[payload], acl=acl)
        return create_status[0][0], 200

    @classmethod
    @error_handle
    def action_post(cls, /, doc_class: Type[Document], payload: dict, doc_path: str, action_path: str, acl=None):
        """Doing an action of a path

        Args:
            doc_class: Document Class
            action_path: Path to action
            payload: Field to be modified and its new value
            doc_path: path to document, could be /_id/xxx or /field1/value1/field2/value2
            acl: Access Control List

        Returns:
            result of the chosen method
        """
        if doc_path == "":
            # collection level method might be public
            public = doc_class.get_actions().get(action_path, {}).get("public", False)
            if not public:
                doc_class.check_acl(acl=acl, act="action." + action_path)
            action_result = doc_class.collection_action(action_name=action_path, acl=acl, payload=payload)
            return action_result, doc_class, action_path
        else:
            doc = cls._get_document_from_path(doc_class, doc_path, acl)
            if doc is None:
                raise NotFoundError(f"Cannot find the document {doc_class.__name__}/{doc_path}")
            sub_doc, action_name = cls._get_method_from_path(doc, action_path, acl)
            doc.check_acl(acl=acl, act="action." + action_name, doc=doc)
            action_result = sub_doc.action(action_name=action_name, acl=acl, payload=payload)
            return action_result, sub_doc.__class__, action_name
