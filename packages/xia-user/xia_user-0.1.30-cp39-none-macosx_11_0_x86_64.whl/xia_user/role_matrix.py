from __future__ import annotations
from xia_fields import StringField, DictField
from xia_engine import AclItem
from xia_engine import ListField, EmbeddedDocumentField
from xia_engine import Document, EmbeddedDocument
from xia_engine import Acl


class Policy(EmbeddedDocument):
    sub: str = StringField(required=True)
    obj: str = StringField(required=True)
    act: str = StringField(required=True)


class Group(EmbeddedDocument):
    child: str = StringField(required=True, regex="^(?=[A-Za-z0-9])(?!.*__)[A-Za-z0-9_]{1,18}[A-Za-z0-9]$")
    parent: str = StringField(required=True, regex="^(?=[A-Za-z0-9])(?!.*__)[A-Za-z0-9_]{1,18}[A-Za-z0-9]$")


class RoleContent(EmbeddedDocument):
    name: str = StringField(sample="user_admin", description="Role Name",
                            regex="^(?=[A-Za-z0-9])(?!.*__)[A-Za-z0-9_]{1,18}[A-Za-z0-9]$")
    roles: list = ListField(StringField(regex="^(?=[A-Za-z0-9])(?!.*__)[A-Za-z0-9_]{1,18}[A-Za-z0-9]$"),
                            description="Contained Roles", default=[])
    permissions: list = ListField(EmbeddedDocumentField(AclItem), description="Contained Permissions", default=[])


class RoleMatrix(Document):
    """Permission organization of an application. This object only contains the role and role contents

    Rules:
        * Each user could only be assigned to a role
    """
    _key_fields = ["name"]
    _actions = {
        "get_role_contents": {"out": RoleContent},
        "add_role_permissions": {"out": RoleContent, "in": {"permissions": AclItem}},
        "set_role_permissions": {"out": RoleContent, "in": {"permissions": AclItem}},
        "add_role_sub_roles": {"out": RoleContent},
        "set_role_sub_roles": {"out": RoleContent},
        "get_implicit_permissions_for_roles": {"out": RoleContent},
    }

    name: str = StringField(description="Application Name", unique=True,
                            regex="^(?=[A-Za-z0-9])(?!.*--)[A-Za-z0-9-]{1,18}[A-Za-z0-9]$")
    policies: list = ListField(EmbeddedDocumentField(document_type=Policy))
    groups: list = ListField(EmbeddedDocumentField(document_type=Group))
    new_user_fields: list = ListField(StringField(), description="Needed new user's information", default=[])
    new_user_roles: list = ListField(StringField(), description="Default roles for new user", default=[])
    new_user_profile: dict = DictField(description="New user's profile")
    callback_urls: list = ListField(StringField(), description="List of authorized callback Url", default=[])

    def __init__(self, **kwargs):
        if "policies" not in kwargs:
            kwargs["policies"] = [Policy(sub="root", obj="*", act="*")]
        if "groups" not in kwargs:
            kwargs["groups"] = [Group(child="admin", parent="root")]
        super().__init__(**kwargs)
        self.dag = {}
        self._dag_generate()

    def _dag_add_policy(self, policy: Policy):
        if policy.sub in self.dag:
            if (policy.obj, policy.act) not in self.dag[policy.sub]:
                self.dag[policy.sub].append((policy.obj, policy.act))
        else:
            self.dag[policy.sub] = [(policy.obj, policy.act)]
        if (policy.obj, policy.act) not in self.dag:
            self.dag[(policy.obj, policy.act)] = []

    def _dag_set_policies(self, sub, policies: list):
        policy_list = [policy for policy in policies if policy.sub == sub]
        self.dag[sub] = [item for item in self.dag[sub] if isinstance(item, str)]  # Keep roles
        for policy in policy_list:
            self._dag_add_policy(policy)

    def _dag_add_group(self, group: Group):
        if group.child in self.dag:
            if group.parent not in self.dag[group.child]:
                self.dag[group.child].append(group.parent)
        else:
            self.dag[group.child] = [group.parent]
        if group.parent not in self.dag:
            self.dag[group.parent] = []

    def _dag_set_groups(self, child: str, groups: list):
        group_list = [group for group in groups if group.child == child]
        self.dag[child] = [item for item in self.dag[child] if isinstance(item, tuple)]  # Keep policies
        for group in group_list:
            self._dag_add_group(group)

    def _dag_generate(self):
        for group in self.groups:
            self._dag_add_group(group)
        for policy in self.policies:
            self._dag_add_policy(policy)
        if "public" not in self.dag:
            self.dag["public"] = []

    def _dfs(self, start: str, discovered: dict) -> dict:
        """Deep First Search

        Args:
            start: start point
            discovered: a dictionary [point, discovered] to mark if a point could be reached from start point

        Returns:
            discovered record after searching.
        """
        discovered[start] = True
        for end in self.dag[start]:
            if not discovered[end]:
                self._dfs(end, discovered)
        return discovered

    def _check_new_group(self, new_group: Group) -> bool:
        """Check if new added group will break DAG (making a circular)

        Args:
            new_group: New group to be added into DAG

        Returns:
            True if the new group is safe else False
        """
        if new_group.child not in self.dag:
            self.dag[new_group.child] = []
        discovered = {k: False for k in self.dag}
        self._dfs(new_group.parent, discovered)
        return not discovered[new_group.child]

    def _add_permissions(self, sub: str, permissions: list):
        for permission in permissions:
            new_policy = Policy(sub=sub, obj=permission.obj, act=permission.act)
            if new_policy not in self.policies:
                self._dag_add_policy(new_policy)
                self.policies.append(new_policy)

    def _add_groups(self, child: str, parents: list):
        for parent in parents:
            new_group = Group(child=child, parent=parent)
            if new_group not in self.groups and self._check_new_group(new_group):
                self._dag_add_group(new_group)
                self.groups.append(new_group)

    def _set_sub_permissions(self, sub: str, permissions: list):
        assert isinstance(self.policies, list)
        new_policies = [Policy(sub=sub, obj=permission.obj, act=permission.act) for permission in permissions]
        self.policies = [policy for policy in self.policies if policy.sub != sub]
        if new_policies:
            self.policies.extend(new_policies)
            self._dag_set_policies(sub, new_policies)

    def _set_sub_groups(self, child: str, parents: list):
        new_groups = [Group(child=child, parent=parent) for parent in parents]
        old_groups = [group for group in self.groups if group.child == child]
        self.groups = [group for group in self.groups if group.child != child]
        if new_groups:
            for new_group in new_groups:
                if not self._check_new_group(new_group):
                    self.groups.extend(old_groups)
                    return
            self.groups.extend(new_groups)
            self._dag_set_groups(child, new_groups)

    def get_role_contents(self, role_name: str, _acl=None):
        """Get Role Contents

        Args:
            role_name: Name of role
            _acl: Access Control List

        Returns:
            Role Content object
        """
        policies = [policy for policy in self.policies if policy.sub == role_name]
        permissions = [{"obj": policy.obj, "act": policy.act} for policy in policies]
        roles = [group.parent for group in self.groups if group.child == role_name]
        content = RoleContent.from_display(name=role_name, roles=roles, permissions=permissions)
        return content

    def add_role_permissions(self, role_name: str, permissions: list, _acl=None):
        permissions = [AclItem.from_display(**p) for p in permissions]
        self._add_permissions(role_name, permissions)
        self.save()
        return self.get_role_contents(role_name=role_name)

    def set_role_permissions(self, role_name: str, permissions: list, _acl=None):
        permissions = [AclItem.from_display(**p) for p in permissions]
        self._set_sub_permissions(role_name, permissions)
        self.save()
        return self.get_role_contents(role_name=role_name)

    def add_role_sub_roles(self, role_name: str, sub_role_names: list, _acl=None):
        self._add_groups(role_name, sub_role_names)
        self.save()
        return self.get_role_contents(role_name=role_name)

    def set_role_sub_roles(self, role_name: str, sub_role_names: list, _acl=None):
        self._set_sub_groups(role_name, sub_role_names)
        self.save()
        return self.get_role_contents(role_name=role_name)

    def get_implicit_permissions_for_roles(self, role_names: list, _acl=None):
        """Get full recursive permission of a list of roles

        Args:
            role_names (:obj:`list`): Role list
            _acl: Access Control List

        Returns:
            Role Content object of all implicit permissions
        """
        for role_name in role_names:
            if role_name not in self.dag:
                self.dag[role_name] = []  # Necessary for un-existed role
        private_disc = {k: False for k in self.dag}
        for role_name in role_names:
            self._dfs(role_name, private_disc)
        private_permission = [{"obj": k[0], "act": k[1]}
                              for k, v in private_disc.items() if v and isinstance(k, tuple)]
        content = RoleContent.from_display(name=",".join(role_names), permissions=private_permission)
        return content
