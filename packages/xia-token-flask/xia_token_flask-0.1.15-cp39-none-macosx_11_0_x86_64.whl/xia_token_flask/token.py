import json
import base64
from datetime import datetime
from flask import Response, request
import jwt
from xia_engine import Acl


class FlaskToken:
    """JWT management

    Workflow is quite straight forward:
        * Using Access token when it is available
        * When Access token is not available, using refresh token to get a new access token
        * When refresh token is not there, redirect to authentication process

    JWT keys:
        * Need to rotate the key so key is a list
        * Encode with the first key
        * Decode with one of given key list

    Token type:
        * Access Token: The token contains user information and user acl, will have a short expiration time
        * Refresh Token: The token allows to generate access token, will have a long expiration time but narrow scope
        * Refresh Signal: Sign that a refresh token might exist
    """
    keys = []  #: keys to be used to encrypt token
    ACCESS_TOKEN_LIFETIME = 3600  #: Lifetime of access token
    REFRESH_TOKEN_LIFETIME = 2**26  #: Lifetime of refresh token
    CONFIRM_TOKEN_LIFETIME = 86400  #: Lifetime of confirmation token
    LOGIN_TOKEN_LIFETIME = 3600  #: Lifetime of login token

    ROOT_HEADER_TOKEN_NAME = "xia_root_header_token"  #: Root Menu Token
    APP_HEADER_TOKEN_NAME = "xia_app_header_token"  #: App Menu Token
    REFRESH_TOKEN_NAME = "xia_refresh_token"  #: Refresh token name
    REFRESH_SIGNAL_NAME = "xia_refresh_signal"  #: Refresh signal token name
    ACCESS_TOKEN_NAME = "xia_access_token"  #: Access token name
    CONFIRM_TOKEN_NAME = "xia_confirm_token"  #: Confirm token name
    LOGIN_TOKEN_NAME = "xia_password_reset_token"  #: Password reset token

    ISSUER_ID = "xia_token"  #: Name of Issuer

    ACCESS_TOKEN_PATH = "/"  #: Refresh Token Cookie Path should be bound to. Change default value to enforce security
    REFRESH_TOKEN_PATH = "/"  #: Refresh Token Cookie Path should be bound to. Change default value to enforce security

    @classmethod
    def get_origin_fqdn(cls):
        return request.headers.get("X-Forwarded-Host", request.url_root.split("://")[1].split("/")[0])

    @classmethod
    def get_root_domain(cls):
        fqdn = cls.get_origin_fqdn()
        if "X-Forwarded-Host" in request.headers:
            domain_parts = fqdn.split(".")
            if len(domain_parts) == 2:  # Case 1: login module is configured as root domain
                root_domain = fqdn
            elif all([part.isdigit() for part in domain_parts]):  # Case 2: ip address domain
                root_domain = fqdn
            else:  # Case 3: login module is configured as a sub domain
                root_domain = ".".join(domain_parts[1:])
        else:
            root_domain = fqdn
        return root_domain

    @classmethod
    def _parse_header_token(cls, token_name: str, header_token: str = ""):
        header_token = request.cookies.get(token_name) if not header_token else header_token
        try:
            return json.loads(base64.b64decode(header_token.encode()).decode())
        except Exception as e:
            return {}

    @classmethod
    def set_app_header_token(cls, resp: Response, app_name: str, app_info: dict, app_profile: dict):
        user_name = app_profile.get("user_name", "")
        nick_name = app_profile.get("nick_name", "")
        app_search = app_info.pop("search", None)
        app_status = app_info.pop("status", {})
        app_status = {k: app_profile.get(k, "") for k, v in app_status.items()}
        if "user_name" not in app_status and "nick_name" not in app_status:
            app_status["nick_name"] = app_profile.get("nick_name", "") if user_name != nick_name else "New User"
        app_header_settings = {
            "app_name": app_name,
            "app_menu": app_info,
            "app_search": app_search,
            "app_status": app_status
        }
        app_header_token = base64.b64encode(json.dumps(app_header_settings, ensure_ascii=False).encode()).decode()
        resp.set_cookie(cls.APP_HEADER_TOKEN_NAME, app_header_token, max_age=2**26)

    @classmethod
    def remove_app_header_token(cls, resp: Response):
        resp.set_cookie(cls.APP_HEADER_TOKEN_NAME, "dummy", max_age=0)

    @classmethod
    def get_app_header_token(cls, header_token: str = ""):
        return cls._parse_header_token(cls.APP_HEADER_TOKEN_NAME, header_token)

    @classmethod
    def _set_root_header_token(cls, resp: Response, token_value: str):
        root_domain = cls.get_root_domain()
        if root_domain.split(".")[-1].isdigit() or root_domain == "localhost":  # Cannot attribute domain cookie locally
            resp.set_cookie(cls.ROOT_HEADER_TOKEN_NAME, token_value, max_age=2 ** 26)
        else:
            resp.set_cookie(cls.ROOT_HEADER_TOKEN_NAME, token_value, max_age=2 ** 26, domain=root_domain)

    @classmethod
    def set_root_header_token(cls, resp: Response, user_info: dict):
        """Set Root Header token

        Args:
            resp:
            user_info:
        """
        menu_info = {}
        for k in user_info.get("apps", []):
            if cls.get_origin_fqdn() == cls.get_root_domain():
                item_info = {"url": "https://" + cls.get_root_domain(), "title": k}
            else:
                item_info = {"url": "https://" + k + "." + cls.get_root_domain(), "title": k}
            menu_info[k] = item_info
        root_header_settings = {
            "login": True,
            "root_menu": menu_info,
            "root_search": None,
            "root_status": {}
        }
        root_header_token = base64.b64encode(json.dumps(root_header_settings, ensure_ascii=False).encode()).decode()
        cls._set_root_header_token(resp, root_header_token)

    @classmethod
    def remove_root_header_token(cls, resp: Response):
        root_header_settings = cls.get_root_header_token()
        if root_header_settings:
            root_header_settings["login"] = False
            root_header_token = base64.b64encode(json.dumps(root_header_settings, ensure_ascii=False).encode()).decode()
            cls._set_root_header_token(resp, root_header_token)

    @classmethod
    def active_root_header_token(cls, resp: Response):
        root_header_settings = cls.get_root_header_token()
        if root_header_settings:
            root_header_settings["login"] = True
            root_header_token = base64.b64encode(json.dumps(root_header_settings, ensure_ascii=False).encode()).decode()
            cls._set_root_header_token(resp, root_header_token)

    @classmethod
    def get_root_header_token(cls, header_token: str = ""):
        return cls._parse_header_token(cls.ROOT_HEADER_TOKEN_NAME, header_token)

    @classmethod
    def parse_token(cls, token: str):
        """Parse token and get payload

        Args:
            token: token contents

        Returns:
            token payload or {} if Token is wrong
        """
        payload = {}
        if not token:
            return payload
        for key in cls.keys:
            try:
                payload = jwt.decode(token.encode(), key, algorithms=['HS512'], options={"require": ["exp"]})
            except jwt.PyJWTError as e:
                continue
            return payload
        return payload

    @classmethod
    def parse_access_token(cls, access_token: str = None):
        """Get information of access token

        Args:
            access_token (str): Access Token

        Returns:
            arg0 (str): Username
            arg1 (list): User ACL : example [[domain/*, read], [user/*, *]]
            arg2 (dict): User profile
            arg3 (dict): Token related information

        Notes:
            Expire in cookie in 15 minutes while 20 minutes in the payload.
        """
        root_header_info = cls.get_root_header_token()
        if root_header_info and not root_header_info.get("login", True):
            # Marked as logged out in the root header token
            return "", [], {}, {}
        access_token = request.cookies.get(cls.ACCESS_TOKEN_NAME) if not access_token else access_token
        payload = cls.parse_token(access_token)
        if payload.get("name", "") != cls.ACCESS_TOKEN_NAME:
            # Wrong cookie loaded
            return "", [], {}, {}
        token_info = payload.pop("token_info", {})
        token_info.update({k: v for k, v in payload.items() if k not in ["user_id", "user_acl", "user_profile"]})
        user_acl = Acl.from_display(content=payload.get("user_acl", []))
        return payload.get("user_id", ""), user_acl, payload.get("user_profile", {}), token_info

    @classmethod
    def parse_refresh_token(cls, refresh_token: str = None):
        """Get the information of refresh token

        Args:
            refresh_token (str): Refresh Token

        Returns:
            arg1 (str): Username
            arg2 (dict): Token information

        """
        root_header_info = cls.get_root_header_token()
        if root_header_info and not root_header_info.get("login", True):
            # Marked as logged out in the root header token
            return "", {}
        refresh_token = request.cookies.get(cls.REFRESH_TOKEN_NAME) if not refresh_token else refresh_token
        payload = cls.parse_token(refresh_token)
        if payload.get("name", "") != cls.REFRESH_TOKEN_NAME:
            # Wrong cookie loaded
            return "", {}
        token_info = payload.pop("token_info", {})
        token_info.update({k: v for k, v in payload.items() if k not in ["user_id"]})
        return payload.get("user_id", ""), token_info

    @classmethod
    def parse_refresh_signal(cls, refresh_signal: str = None):
        """Parse the information of a refresh Signal

        Args:
            refresh_signal (str): Refresh Signal

        Returns:
            arg1 (str): Username
            arg2 (dict): Token information

        """
        root_header_info = cls.get_root_header_token()
        if root_header_info and not root_header_info.get("login", True):
            # Marked as logged out in the root header token
            return "", {}
        refresh_signal = request.cookies.get(cls.REFRESH_SIGNAL_NAME) if not refresh_signal else refresh_signal
        payload = cls.parse_token(refresh_signal)
        if payload.get("name", "") != cls.REFRESH_SIGNAL_NAME:
            # Wrong cookie loaded
            return "", {}
        token_info = payload.pop("token_info", {})
        token_info.update({k: v for k, v in payload.items() if k not in ["user_id"]})
        return payload.get("user_id", ""), token_info

    @classmethod
    def parse_confirm_token(cls, confirm_token: str):
        """Parse the information of a confirmation token

        Args:
            confirm_token (str): Refresh Signal

        Returns:
            arg1 (str): Username
            arg2 (dict): Token information

        Notes:
            Expire in cookie in 15 minutes while 20 minutes in the payload.
        """
        payload = cls.parse_token(confirm_token)
        if payload.get("name", "") != cls.CONFIRM_TOKEN_NAME:
            # Wrong cookie loaded
            return "", {}
        token_info = payload.pop("token_info", {})
        token_info.update({k: v for k, v in payload.items() if k not in ["user_id"]})
        return payload.get("user_id", ""), token_info

    @classmethod
    def parse_login_token(cls, login_token: str):
        """Parse the information of a password reset token

        Args:
            login_token (str): Refresh Signal

        Returns:
            arg1 (str): Username
            arg1 (str): Hashed Password
            arg3 (dict): Token information

        Notes:
            Expire in cookie in 15 minutes while 20 minutes in the payload.
        """
        payload = cls.parse_token(login_token)
        if payload.get("name", "") != cls.LOGIN_TOKEN_NAME:
            # Wrong cookie loaded
            return "", "", {}
        token_info = payload.pop("token_info", {})
        token_info.update({k: v for k, v in payload.items() if k not in ["user_id"]})
        return payload.get("user_id", ""), payload.get("password", ""), token_info

    @classmethod
    def generate_access_token(cls, user_id: str, user_acl: Acl, user_profile: dict, token_info: dict):
        """Generate an Access Token:

        Args:
            user_id (str): token user id
            user_acl (Acl): User ACL
            user_profile (dict): attached user profile (permission + profile)
            token_info (dict): token related information
        """
        expire_time = int(round((datetime.now().timestamp() + cls.ACCESS_TOKEN_LIFETIME)))
        user_acl_info = user_acl.get_display_data()["content"]
        payload = {
            "user_id": user_id,
            "name": cls.ACCESS_TOKEN_NAME,
            "exp": expire_time,
            "iss": cls.ISSUER_ID,
            "user_acl": user_acl_info,
            "user_profile": user_profile,
            "token_info": token_info,
        }
        return jwt.encode(payload, cls.keys[0], algorithm='HS512')

    @classmethod
    def generate_refresh_token(cls, user_id: str, token_info: dict):
        """Generate a refresh Token:

        Args:
            user_id (str): token user id
            token_info (dict): token related information
        """
        expire_time = int(round((datetime.now().timestamp() + cls.REFRESH_TOKEN_LIFETIME)))
        payload = {
            "user_id": user_id,
            "name": cls.REFRESH_TOKEN_NAME,
            "exp": expire_time,
            "iss": cls.ISSUER_ID,
            "token_info": token_info,
        }
        return jwt.encode(payload, cls.keys[0], algorithm='HS512')

    @classmethod
    def generate_refresh_signal(cls, user_id: str, token_info: dict):
        """Generate a refresh Signal:

        Args:
            user_id (str): token user id
            token_info (dict): token related information
        """
        expire_time = int(round((datetime.now().timestamp() + cls.REFRESH_TOKEN_LIFETIME)))
        payload = {
            "user_id": user_id,
            "name": cls.REFRESH_SIGNAL_NAME,
            "exp": expire_time,
            "iss": cls.ISSUER_ID,
            "token_info": token_info,
        }
        return jwt.encode(payload, cls.keys[0], algorithm='HS512')

    @classmethod
    def generate_confirm_token(cls, user_id: str, token_info: dict):
        """Generate a confirmation token:

        Args:
            user_id (str): token user id
            token_info (dict): token related information
        """
        expire_time = int(round((datetime.now().timestamp() + cls.CONFIRM_TOKEN_LIFETIME)))
        payload = {
            "user_id": user_id,
            "name": cls.CONFIRM_TOKEN_NAME,
            "exp": expire_time,
            "iss": cls.ISSUER_ID,
            "token_info": token_info,
        }
        return jwt.encode(payload, cls.keys[0], algorithm='HS512')

    @classmethod
    def generate_login_token(cls, user_id: str, hashed_passwd: str, token_info: dict):
        """Generate a password reset Token:

        Args:
            user_id (str): token user id
            hashed_passwd (str): sha256 of hashed password (hash on hash)
            token_info (dict): token related information
        """
        expire_time = int(round((datetime.now().timestamp() + cls.LOGIN_TOKEN_LIFETIME)))
        payload = {
            "user_id": user_id,
            "name": cls.LOGIN_TOKEN_NAME,
            "password": hashed_passwd,
            "exp": expire_time,
            "iss": cls.ISSUER_ID,
            "token_info": token_info,
        }
        return jwt.encode(payload, cls.keys[0], algorithm='HS512')

    @classmethod
    def set_access_token(cls, resp: Response, user_id: str, user_acl: Acl, user_profile: dict, token_info: dict):
        """Set Access Token:

        Args:
            resp (:obj:`Response`): A http response which the cookies should be attached to
            user_id (str): token user id
            user_acl (Acl): User ACL
            user_profile (dict): attached user profile (permission + profile)
            token_info (dict): token related information
        """
        access_token = cls.generate_access_token(user_id, user_acl, user_profile, token_info)
        resp.set_cookie(cls.ACCESS_TOKEN_NAME, access_token,
                        max_age=cls.ACCESS_TOKEN_LIFETIME, path=cls.ACCESS_TOKEN_PATH)
        return resp

    @classmethod
    def set_refresh_token(cls, resp: Response, user_id: str, token_info: dict):
        """Set Refresh Token ans Refresh Signal

        Args:
            resp (:obj:`Response`): A http response which the cookies should be attached to
            user_id (str): token user id
            token_info (dict): token related information
        """
        refresh_token = cls.generate_refresh_token(user_id, token_info)
        refresh_signal = cls.generate_refresh_signal(user_id, token_info)
        resp.set_cookie(cls.REFRESH_TOKEN_NAME, refresh_token,
                        max_age=cls.REFRESH_TOKEN_LIFETIME, path=cls.REFRESH_TOKEN_PATH)
        resp.set_cookie(cls.REFRESH_SIGNAL_NAME, refresh_signal,
                        max_age=cls.REFRESH_TOKEN_LIFETIME, path=cls.ACCESS_TOKEN_PATH)
        return resp

    @classmethod
    def remove_all_tokens(cls, resp: Response):
        cls.remove_root_header_token(resp)
        cls.remove_app_header_token(resp)
        resp.set_cookie(cls.REFRESH_TOKEN_NAME, "dummy", max_age=0, path=cls.REFRESH_TOKEN_PATH)
        resp.set_cookie(cls.REFRESH_SIGNAL_NAME, "dummy", max_age=0, path=cls.ACCESS_TOKEN_PATH)
        resp.set_cookie(cls.ACCESS_TOKEN_NAME, "dummy", max_age=0, path=cls.ACCESS_TOKEN_PATH)
        return resp
