import random
import string
import hashlib
import uuid
from datetime import datetime, timezone
from functools import lru_cache
from passlib.hash import sha512_crypt as sha512
from xia_fields import StringField, IntField, TimestampField, DictField
from xia_fields_network import EmailField
from xia_engine import EmbeddedDocument, Document
from xia_engine import ListField, EmbeddedDocumentField, ExternalField
from xia_engine import Acl, AclItem
from xia_engine import AuthenticationError, NotFoundError, AuthorizationError, OutOfQuotaError
from xia_user.role_matrix import RoleMatrix, RoleContent
from xia_user.messages import UserBasicInfo


class ApiKey(EmbeddedDocument):
    """Structure hold necessary Information of an API Key

    """
    id: str = StringField(description="Api Key ID", examle=str(uuid.uuid4()))
    description: str = StringField(description="Description of API Key")
    key: str = StringField(description="hashed value of an API Key", hidden=True)
    expires: float = TimestampField(description="Expiration timestamp of API Key")
    acl: dict = EmbeddedDocumentField(Acl, description="ACL of API")


class ApiInfo(ApiKey):
    user_name: str = StringField(description="API attached username")
    app_name: str = StringField(description="API attached application name")
    key: str = StringField(description="API Key (only visible during the creation)", hidden=False)


class UserAppInfo(EmbeddedDocument):
    """Structure hold the user information
    """
    user_name: str = StringField(description="User name")
    app_name: str = StringField(description="Application name")
    user_profile: str = DictField(description="Application specific User profile")
    acl: dict = EmbeddedDocumentField(Acl, description="ACL of User")


class UserRoles(Document):
    """User Role assignment of a specified application

    """
    _key_fields = ["app_name", "user_name"]
    _api_acl_cache_length = 600  #: get api acl cache expiration period, default = 600 seconds
    _auth_app_name = "xia-auth"  #: This will be the authorization master authorization

    _actions = {
        "create_role_matrix": {"out": UserAppInfo},
        "delete_role_matrix": {"out": UserAppInfo},
        "get_user_acl": {"out": UserAppInfo},
        "api_key_add": {"in": {"acl": AclItem}, "out": ApiInfo},
        "api_key_remove": {"out": ApiKey},
        "get_api_acl": {"out": ApiInfo, "public": True},
    }
    _field_groups = {"basic": ["user_name", "app_name", "nick_name", "user_settings", "api_keys", "api_key_details"]}

    app_name: str = StringField(required=True, description="Application Name")
    user_name: str = StringField(required=True, description="User unique identification")
    nick_name: str = StringField(required=True, unique_with=["app_name"], description="Application specific nick name")
    user_fields: list = ListField(StringField(), description="Fields of which value is retrieved from User", default=[])
    user_settings: dict = DictField(description="User's settings")
    profile: dict = DictField(description="Application specific profile", default={})
    sso_token: str = StringField(description="SSO Token which will expire very soon", hidden=True)
    roles: list = ListField(StringField(), default=[], description="User's role inside the Application")
    api_keys: list = ListField(StringField(), unique=True, default=[], hidden=True)
    api_key_details: list = ListField(EmbeddedDocumentField(document_type=ApiKey), default=[])
    permission: RoleMatrix = ExternalField(
        document_type=RoleMatrix,
        description="Permission Details",
        field_map={"app_name": "name"},
    )

    def __init__(self, **kwargs):
        if "user_name" in kwargs and "nick_name" not in kwargs:
            # Nick Name is by default the same as user_name
            kwargs["nick_name"] = kwargs["user_name"]
        super().__init__(**kwargs)

    @classmethod
    def get_hashed_key(cls, key: str) -> str:
        """Get an immutable hash key

        Args:
            key: key to be hashed

        Returns:
            object: hashed key
        """
        return hashlib.sha3_512(key.encode('utf-8')).hexdigest()

    def get_user_profile(self) -> dict:
        """Get application specific user profile

        Returns:
            dictionary of user profile
        """
        profile = {} if not self.profile else self.profile
        profile.update({
            "user_name": self.user_name,
            "nick_name": self.nick_name,
        })
        return profile

    def get_user_acl(self, _acl=None) -> UserAppInfo:
        user_profile = self.get_user_profile()
        role_matrix = self.permission
        role_content = role_matrix.get_implicit_permissions_for_roles(self.roles)
        user_acl = Acl(content=role_content.permissions)
        user_app_info = UserAppInfo(
            user_name=self.user_name,
            app_name=self.app_name,
            user_profile=self.get_user_profile(),
            acl=user_acl.get_filled_acl(user_profile)
        )
        return user_app_info

    def api_key_add(self, description: str = "", expires: float = 0.0, acl: list = None, _acl=None):
        """Adding an API Key

        Args:
            description: API Key description
            expires: Timestamp when the key expires. default never expires
            acl: Access control list of this key or the format [{"obj": xxx,"act": xxx}]
            _acl: Access control list to check

        Returns:
            Original API Key

        Notes:
            This function is designed to use cache. So the execution is divided into two steps:
            * Step 1: Get related object's object ID
            * Step 2: Get Data
        """
        api_id = str(uuid.uuid4())
        api_key = "".join(map(lambda x: random.choice(string.digits + string.ascii_letters), [0] * 48))
        hashed_key = self.get_hashed_key(api_key)
        self.api_keys.append(hashed_key)
        if not acl:
            api_acl = Acl.from_display(content=[{"obj": "*", "act": "*"}])
        else:
            api_acl = Acl.from_display(content=acl)
        api_detail = ApiKey.from_display(description=description, expires=expires, acl=api_acl,
                                         key=hashed_key, id=api_id)
        self.api_key_details.append(api_detail)
        self.save()
        return ApiInfo(description=description, expires=expires, acl=api_acl, key=api_key, id=api_id)

    def api_key_remove(self, key_id: str, _acl=None):
        """Remove an existed hashed key

        Args:
            key_id: API Key ID
            _acl: Access control list to check
        """
        api_to_delete = [detail for detail in self.api_key_details if detail.id == key_id]
        if api_to_delete:
            self.api_key_details = [detail for detail in self.api_key_details if detail.id != key_id]
            self.api_keys = [key_info.key for key_info in self.api_key_details]
            self.save()
            return api_to_delete[0]
        else:
            raise NotFoundError(f"API Key with id {key_id} cannot be found.")

    @classmethod
    @lru_cache(maxsize=1024)
    def _prepare_get_api_acl_call(cls, api_key: str, app_name: str):
        hashed_key = cls.get_hashed_key(api_key)
        user_role = cls.load(api_keys=[hashed_key])
        if not user_role or user_role.app_name != app_name:
            raise AuthenticationError(f"Unknown API Key for app: {app_name}")
        role_matrix = user_role.permission
        api_details = [detail for detail in user_role.api_key_details if detail.key == hashed_key]
        api_expires = api_details[0].expires
        if 0 < api_expires <= datetime.now().timestamp():
            # Api key expires
            user_role.api_key_details = [detail for detail in user_role.api_key_details if detail.key != hashed_key]
            user_role.api_keys = [key_info.key for key_info in user_role.api_key_details]
            user_role.save()
            raise AuthenticationError("API Key expired")
        return hashed_key, user_role.get_id(), role_matrix.get_id(), api_expires, role_matrix.__class__

    @classmethod
    @lru_cache(maxsize=1024)
    def _exec_get_api_acl_call(cls, api_key: str, app_name: str, time_ver: int, role_vers: str, matrix_ver: str):
        hashed_key, role_id, matrix_id, _, matrix_class = cls._prepare_get_api_acl_call(api_key, app_name)
        user_role = cls.load(role_id)
        role_matrx = matrix_class.load(matrix_id)
        if not user_role or user_role.app_name != app_name:
            raise AuthenticationError(f"Unknown API Key for app: {app_name}")
        role_content = role_matrx.get_implicit_permissions_for_roles(user_role.roles)
        user_acl = Acl.from_display(content=role_content.permissions)
        user_acl = user_acl.get_filled_acl(user_role.get_user_profile())
        api_details = [detail for detail in user_role.api_key_details if detail.key == hashed_key]
        if not api_details:
            if hashed_key in user_role.api_keys:
                # Desync between api_keys and api_details, remove
                user_role.api_keys = [key for key in user_role.api_keys if key != hashed_key]
                user_role.save()
            return None, AuthenticationError("Can not find API Details")
        if 0 < api_details[0].expires <= datetime.now().timestamp():
            # Api key expires so we should remove the key
            user_role.api_key_details = [detail for detail in user_role.api_key_details if detail.key != hashed_key]
            user_role.api_keys = [key_info.key for key_info in user_role.api_key_details]
            user_role.save()
            return None, AuthenticationError("API Key expired")
        api_acl = api_details[0].acl - user_acl
        api_acl = api_acl.get_filled_acl(user_role.get_user_profile())
        api_info = ApiInfo(
            id=api_details[0].id,
            user_name=user_role.user_name,
            app_name=user_role.app_name,
            description=api_details[0].description,
            expires=api_details[0].expires,
            acl=api_acl
        )
        return api_info, None

    @classmethod
    def get_api_acl(cls, api_key: str, app_name: str, _acl=None) -> ApiInfo:
        """Get Access List of User

        Args:
            api_key: API Key to provide access
            app_name: Application Name
            _acl: User Access List (of the requester)

        Returns:
            ApiInfo object attached to the api acl
        """
        if not api_key or not app_name:
            raise AuthenticationError("No API Key or No Application Name Found")
        hashed_key, role_id, matrix_id, expires, matrix_class = cls._prepare_get_api_acl_call(api_key, app_name)
        if 0 < expires <= datetime.now().timestamp():
            # Extra Expiration Check
            raise AuthenticationError("API Key expired")
        time_ver = int(datetime.now().timestamp()) // cls._api_acl_cache_length * cls._api_acl_cache_length
        role_ver = cls.get_version(role_id)
        matrix_ver = matrix_class.get_version(matrix_id)
        api_info, exception = cls._exec_get_api_acl_call(api_key, app_name, time_ver, role_ver, matrix_ver)
        if api_info is None:
            raise exception
        else:
            return api_info

    def create_role_matrix(self, matrix_name, _acl=None):
        if self.app_name != self._auth_app_name:
            raise AuthorizationError(f"{self.app_name} is not authorization application")
        app_name = matrix_name.lower()
        admin_apps = self.profile.get("admin_apps", [])
        # Check app count quota
        matrix_quota = self.profile.get("app_max", 5)  # Normal User could hold at max 5 application
        if matrix_quota <= len(admin_apps):
            raise OutOfQuotaError(f"You can not administrate more than {len(admin_apps)} applications")
        auth_matrix = RoleMatrix.load(name=self._auth_app_name)  # Also get the runtime class of RoleMatrix
        if not auth_matrix:
            raise RuntimeError(f"Can not find Root Matrix")
        # Name check
        is_valid = False
        for prefix in self.profile.get("app_prefixes", []):
            if app_name.startswith(prefix):
                is_valid = True
        if not is_valid and (
                app_name.startswith("xia") or
                app_name.startswith("x-i-a") or
                "--" in app_name or
                "-" not in app_name
        ):
            raise ValueError("app name must have '-', not have '--' and cannot start with reserved words")
        # Save new role matrix
        auth_matrix.__class__(name=app_name).save()
        self.__class__(user_name=self.user_name, app_name=app_name, roles=["admin"]).save()
        self.profile["admin_apps"] = self.profile["admin_apps"] + [app_name]
        self.save()
        # Return new app info of the current app:
        user_app_info = UserAppInfo(
            user_name=self.user_name,
            app_name=self.app_name,
            user_profile=self.get_user_profile()
        )
        return user_app_info

    def delete_role_matrix(self, matrix_name, _acl=None):
        if self.app_name != self._auth_app_name:
            raise AuthorizationError(f"{self.app_name} is not authorization application")
        app_name = matrix_name.lower()
        admin_apps = self.profile.get("admin_apps", [])
        if app_name not in admin_apps:
            raise AuthorizationError(f"You are not administrator of {app_name}")
        for user_role in UserRoles.objects(app_name=app_name):
            # We should also remove the admin_apps of the related users in auth_app
            for auth_role in UserRoles.objects(app_name=self._auth_app_name, user_name=user_role.user_name):
                if app_name in auth_role.profile.get("admin_apps", []) and user_role.user_name != self.user_name:
                    # Prevent self lock situation, so we delete the current user in admin list at the end
                    admin_apps = [app for app in auth_role.profile.get("admin_apps", []) if app != app_name]
                    auth_role.profile["admin_apps"] = admin_apps
                    auth_role.save()
            user_role.delete()
        for role_matrix in RoleMatrix.objects(name=app_name):
            role_matrix.delete()
        # Save current user at the end
        admin_apps = [app for app in self.profile.get("admin_apps", []) if app != app_name]
        self.profile["admin_apps"] = admin_apps
        self.save()
        # Return new app info of the current app:
        user_app_info = UserAppInfo(
            user_name=self.user_name,
            app_name=self.app_name,
            user_profile=self.get_user_profile()
        )
        return user_app_info


class User(Document):
    """All information about the user

    """
    _actions = {
        "login_basic": {"out": UserBasicInfo},
        "get_basic": {"out": UserBasicInfo},
        "change_passwd": {"out": UserBasicInfo},
    }

    _key_fields = ["name"]

    _lock_period = 0  #: Each failed login attempt will lock the account for how many seconds
    _basic_catalog = {"name": None, "apps": None, "user_id": None, "confirm_time": None}

    _field_groups = {
        "basic": ["user_id"],
        "email": ["name", "user_id"]
    }

    name: str = EmailField(required=True, unique=True, description="User Name (Email Address)")
    hashed_passwd: str = StringField(description="Hashed password", hidden=True)
    user_id: str = StringField(description="User Unique ID")
    confirm_time: float = TimestampField(description="Account confirmed date")
    lock_time: float = TimestampField(description="Until when user's account is locked", default=0.0)
    login_link: str = StringField(description="User Login URL + Token", hidden=True)
    confirm_link: str = StringField(description="Confirmation URL + Token", hidden=True)
    apps: list = ListField(StringField(), default=[], description="Application Names")
    app_authorizations: dict = DictField(description="Each Application's user fields scope")
    api_keys: list = ListField(StringField(), unique=True, default=[], description="API Keys (hashed)")
    api_key_details: list = ListField(EmbeddedDocumentField(document_type=ApiKey), default=[], description="API detail")
    app_roles = ExternalField(
        document_type=UserRoles,
        description="All roles assigned to user",
        field_map={"user_id": "user_name", "apps": "app_name"},
        list_length=2**10,
    )

    def __init__(self, **kwargs):
        if "passwd" in kwargs:
            kwargs["hashed_passwd"] = self.get_htpasswd(kwargs["passwd"])
            kwargs.pop("passwd")
        if "user_id" not in kwargs:
            kwargs["user_id"] = str(uuid.uuid4())
        super().__init__(**kwargs)

    def change_passwd(self, new_passwd: str, _acl=None):
        self.hashed_passwd = self.get_htpasswd(new_passwd)
        self.save()
        return UserBasicInfo.from_display(**self.get_display_data(catalog=self._basic_catalog))

    @classmethod
    def login_basic(cls, user_name: str, passwd: str, _acl=None):
        user = cls.load(name=user_name, _acl=_acl)
        if user is None or not passwd:
            raise AuthenticationError("User or Password is not correct")
        if not user.hashed_passwd:
            raise AuthenticationError("Password based login is disabled")
        if user.lock_time > datetime.now().timestamp():
            raise AuthenticationError(f"User is locked until {datetime.fromtimestamp(user.lock_time)} UTC")
        if cls.validate_htpasswd(passwd, user.hashed_passwd):
            return UserBasicInfo.from_display(**user.get_display_data(catalog=cls._basic_catalog))
        else:
            if cls._lock_period > 0:
                user.update(lock_time=datetime.now().timestamp() + cls._lock_period)
            raise AuthenticationError("User or Password is not correct")

    @classmethod
    def get_basic(cls, user_id: str, _acl=None):
        """Get User Basic information from user id

        Args:
            user_id: User identification
            _acl: Access Control List

        Returns:
            User information
        """
        user = cls.load(user_id=user_id, _acl=_acl)
        if user is None:
            raise NotFoundError("User cannot be found")
        return UserBasicInfo.from_display(**user.get_display_data(catalog=cls._basic_catalog))

    @classmethod
    def get_hashed_key(cls, key: str) -> str:
        """Get an immutable hash key

        Args:
            key: key to be hashed

        Returns:
            object: hashed key
        """
        return hashlib.sha3_512(key.encode('utf-8')).hexdigest()

    @classmethod
    def get_htpasswd(cls, passwd: str) -> str:
        """Get linux password hash

        Args:
            passwd (obj:`str`): Original Password

        Returns:
            Hashed password string
        """
        return sha512.using().hash(passwd, rounds=5000)

    @classmethod
    def validate_htpasswd(cls, passwd: str, hashed_passwd: str) -> str:
        """Validate linux password hash

        Args:
            passwd: (obj:`str`): password to be validated
            hashed_passwd: hashcode to check
        """
        return sha512.using().verify(passwd, hashed_passwd)
