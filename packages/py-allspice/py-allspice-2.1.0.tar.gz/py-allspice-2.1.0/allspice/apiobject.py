from __future__ import annotations

import logging
from functools import cached_property
from typing import List, Tuple, Dict, Sequence, Optional, Union, Set, IO, Literal
from datetime import datetime, timezone
from enum import Enum

from .baseapiobject import ReadonlyApiObject, ApiObject
from .exceptions import *


class Organization(ApiObject):
    """see https://hub.allspice.io/api/swagger#/organization/orgGetAll"""

    API_OBJECT = """/orgs/{name}"""  # <org>
    ORG_REPOS_REQUEST = """/orgs/%s/repos"""  # <org>
    ORG_TEAMS_REQUEST = """/orgs/%s/teams"""  # <org>
    ORG_TEAMS_CREATE = """/orgs/%s/teams"""  # <org>
    ORG_GET_MEMBERS = """/orgs/%s/members"""  # <org>
    ORG_IS_MEMBER = """/orgs/%s/members/%s"""  # <org>, <username>
    ORG_HEATMAP = """/users/%s/heatmap"""  # <username>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Organization): return False
        return self.allspice_client == other.allspice_client and self.name == other.name

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.name)

    @classmethod
    def request(cls, allspice_client: 'AllSpice', name: str) -> 'Organization':
        return cls._request(allspice_client, {"name": name})

    @classmethod
    def parse_response(cls, allspice_client, result) -> 'Organization':
        api_object = super().parse_response(allspice_client, result)
        # add "name" field to make this behave similar to users for gitea < 1.18
        # also necessary for repository-owner when org is repo owner
        if not hasattr(api_object, "name"):
            Organization._add_read_property("name", result["username"], api_object)
        return api_object

    _patchable_fields = {"description", "full_name", "location", "visibility", "website"}

    def commit(self):
        args = {"name": self.name}
        self._commit(args)

    def create_repo(
            self,
            repoName: str,
            description: str = "",
            private: bool = False,
            autoInit=True,
            gitignores: str = None,
            license: str = None,
            readme: str = "Default",
            issue_labels: str = None,
            default_branch="master",
    ):
        """Create an organization Repository

        Throws:
            AlreadyExistsException: If the Repository exists already.
            Exception: If something else went wrong.
        """
        result = self.allspice_client.requests_post(
            f"/orgs/{self.name}/repos",
            data={
                "name": repoName,
                "description": description,
                "private": private,
                "auto_init": autoInit,
                "gitignores": gitignores,
                "license": license,
                "issue_labels": issue_labels,
                "readme": readme,
                "default_branch": default_branch,
            },
        )
        if "id" in result:
            self.allspice_client.logger.info("Successfully created Repository %s " % result["name"])
        else:
            self.allspice_client.logger.error(result["message"])
            raise Exception("Repository not created... (gitea: %s)" % result["message"])
        return Repository.parse_response(self, result)

    def get_repositories(self) -> List["Repository"]:
        results = self.allspice_client.requests_get_paginated(
            Organization.ORG_REPOS_REQUEST % self.username
        )
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def get_repository(self, name) -> "Repository":
        repos = self.get_repositories()
        for repo in repos:
            if repo.name == name:
                return repo
        raise NotFoundException("Repository %s not existent in organization." % name)

    def get_teams(self) -> List["Team"]:
        results = self.allspice_client.requests_get(
            Organization.ORG_TEAMS_REQUEST % self.username
        )
        teams = [Team.parse_response(self.allspice_client, result) for result in results]
        # organisation seems to be missing using this request, so we add org manually
        for t in teams: setattr(t, "_organization", self)
        return teams

    def get_team(self, name) -> "Team":
        teams = self.get_teams()
        for team in teams:
            if team.name == name:
                return team
        raise NotFoundException("Team not existent in organization.")

    def create_team(
            self,
            name: str,
            description: str = "",
            permission: str = "read",
            can_create_org_repo: bool = False,
            includes_all_repositories: bool = False,
            units=(
                    "repo.code",
                    "repo.issues",
                    "repo.ext_issues",
                    "repo.wiki",
                    "repo.pulls",
                    "repo.releases",
                    "repo.ext_wiki",
            ),
            units_map={},
    ) -> "Team":
        """Alias for AllSpice#create_team"""
        # TODO: Move AllSpice#create_team to Organization#create_team and
        #       deprecate AllSpice#create_team.
        return self.allspice_client.create_team(
            org=self,
            name=name,
            description=description,
            permission=permission,
            can_create_org_repo=can_create_org_repo,
            includes_all_repositories=includes_all_repositories,
            units=units,
            units_map=units_map,
        )

    def get_members(self) -> List["User"]:
        results = self.allspice_client.requests_get(Organization.ORG_GET_MEMBERS % self.username)
        return [User.parse_response(self.allspice_client, result) for result in results]

    def is_member(self, username) -> bool:
        if isinstance(username, User):
            username = username.username
        try:
            # returns 204 if its ok, 404 if its not
            self.allspice_client.requests_get(
                Organization.ORG_IS_MEMBER % (self.username, username)
            )
            return True
        except:
            return False

    def remove_member(self, user: "User"):
        path = f"/orgs/{self.username}/members/{user.username}"
        self.allspice_client.requests_delete(path)

    def delete(self):
        """ Delete this Organization. Invalidates this Objects data. Also deletes all Repositories owned by the User"""
        for repo in self.get_repositories():
            repo.delete()
        self.allspice_client.requests_delete(Organization.API_OBJECT.format(name=self.username))
        self.deleted = True

    def get_heatmap(self) -> List[Tuple[datetime, int]]:
        results = self.allspice_client.requests_get(User.USER_HEATMAP % self.username)
        results = [
            (datetime.fromtimestamp(result["timestamp"]), result["contributions"])
            for result in results
        ]
        return results


class User(ApiObject):
    API_OBJECT = """/users/{name}"""  # <org>
    USER_MAIL = """/user/emails?sudo=%s"""  # <name>
    USER_PATCH = """/admin/users/%s"""  # <username>
    ADMIN_DELETE_USER = """/admin/users/%s"""  # <username>
    ADMIN_EDIT_USER = """/admin/users/{username}"""  # <username>
    USER_HEATMAP = """/users/%s/heatmap"""  # <username>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)
        self._emails = []

    def __eq__(self, other):
        if not isinstance(other, User): return False
        return self.allspice_client == other.allspice_client and self.id == other.id

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.id)

    @property
    def emails(self):
        self.__request_emails()
        return self._emails

    @classmethod
    def request(cls, allspice_client: 'AllSpice', name: str) -> "User":
        api_object = cls._request(allspice_client, {"name": name})
        return api_object

    _patchable_fields = {
        "active",
        "admin",
        "allow_create_organization",
        "allow_git_hook",
        "allow_import_local",
        "email",
        "full_name",
        "location",
        "login_name",
        "max_repo_creation",
        "must_change_password",
        "password",
        "prohibit_login",
        "website",
    }

    def commit(self, login_name: str, source_id: int = 0):
        """
        Unfortunately it is necessary to require the login name
        as well as the login source (that is not supplied when getting a user) for
        changing a user.
        Usually source_id is 0 and the login_name is equal to the username.
        """
        values = self.get_dirty_fields()
        values.update(
            # api-doc says that the "source_id" is necessary; works without though
            {"login_name": login_name, "source_id": source_id}
        )
        args = {"username": self.username}
        self.allspice_client.requests_patch(User.ADMIN_EDIT_USER.format(**args), data=values)
        self._dirty_fields = {}

    def create_repo(
            self,
            repoName: str,
            description: str = "",
            private: bool = False,
            autoInit=True,
            gitignores: str = None,
            license: str = None,
            readme: str = "Default",
            issue_labels: str = None,
            default_branch="master",
    ):
        """Create a user Repository

        Throws:
            AlreadyExistsException: If the Repository exists already.
            Exception: If something else went wrong.
        """
        result = self.allspice_client.requests_post(
            "/user/repos",
            data={
                "name": repoName,
                "description": description,
                "private": private,
                "auto_init": autoInit,
                "gitignores": gitignores,
                "license": license,
                "issue_labels": issue_labels,
                "readme": readme,
                "default_branch": default_branch,
            },
        )
        if "id" in result:
            self.allspice_client.logger.info("Successfully created Repository %s " % result["name"])
        else:
            self.allspice_client.logger.error(result["message"])
            raise Exception("Repository not created... (gitea: %s)" % result["message"])
        return Repository.parse_response(self, result)

    def get_repositories(self) -> List["Repository"]:
        """ Get all Repositories owned by this User."""
        url = f"/users/{self.username}/repos"
        results = self.allspice_client.requests_get_paginated(url)
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def get_orgs(self) -> List[Organization]:
        """ Get all Organizations this user is a member of."""
        url = f"/users/{self.username}/orgs"
        results = self.allspice_client.requests_get_paginated(url)
        return [Organization.parse_response(self.allspice_client, result) for result in results]

    def get_teams(self) -> List['Team']:
        url = f"/user/teams"
        results = self.allspice_client.requests_get_paginated(url, sudo=self)
        return [Team.parse_response(self.allspice_client, result) for result in results]

    def get_accessible_repos(self) -> List['Repository']:
        """ Get all Repositories accessible by the logged in User."""
        results = self.allspice_client.requests_get("/user/repos", sudo=self)
        return [Repository.parse_response(self, result) for result in results]

    def __request_emails(self):
        result = self.allspice_client.requests_get(User.USER_MAIL % self.login)
        # report if the adress changed by this
        for mail in result:
            self._emails.append(mail["email"])
            if mail["primary"]:
                self._email = mail["email"]

    def delete(self):
        """ Deletes this User. Also deletes all Repositories he owns."""
        self.allspice_client.requests_delete(User.ADMIN_DELETE_USER % self.username)
        self.deleted = True

    def get_heatmap(self) -> List[Tuple[datetime, int]]:
        results = self.allspice_client.requests_get(User.USER_HEATMAP % self.username)
        results = [
            (datetime.fromtimestamp(result["timestamp"]), result["contributions"])
            for result in results
        ]
        return results


class Branch(ReadonlyApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/branches/{branch}"""

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Branch):
            return False
        return self.commit == other.commit and self.name == other.name

    def __hash__(self):
        return hash(self.commit["id"]) ^ hash(self.name)

    _fields_to_parsers = {
        # This is not a commit object
        # "commit": lambda allspice_client, c: Commit.parse_response(allspice_client, c)
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, branch: str):
        return cls._request(allspice_client, {"owner": owner, "repo": repo, "branch": branch})


class Repository(ApiObject):
    API_OBJECT = """/repos/{owner}/{name}"""  # <owner>, <reponame>
    REPO_IS_COLLABORATOR = """/repos/%s/%s/collaborators/%s"""  # <owner>, <reponame>, <username>
    REPO_SEARCH = """/repos/search/%s"""  # <reponame>
    REPO_BRANCHES = """/repos/%s/%s/branches"""  # <owner>, <reponame>
    REPO_BRANCH = """/repos/{owner}/{repo}/branches/{branch}"""
    REPO_ISSUES = """/repos/{owner}/{repo}/issues"""  # <owner, reponame>
    REPO_DESIGN_REVIEWS = """/repos/{owner}/{repo}/pulls"""
    REPO_DELETE = """/repos/%s/%s"""  # <owner>, <reponame>
    REPO_TIMES = """/repos/%s/%s/times"""  # <owner>, <reponame>
    REPO_USER_TIME = """/repos/%s/%s/times/%s"""  # <owner>, <reponame>, <username>
    REPO_COMMITS = "/repos/%s/%s/commits"  # <owner>, <reponame>
    REPO_TRANSFER = "/repos/{owner}/{repo}/transfer"
    REPO_MILESTONES = """/repos/{owner}/{repo}/milestones"""
    REPO_GET_ARCHIVE = "/repos/{owner}/{repo}/archive/{ref}.{format}"
    REPO_GET_ALLSPICE_JSON = "/repos/{owner}/{repo}/allspice_generated/json/{content}"
    REPO_GET_ALLSPICE_SVG = "/repos/{owner}/{repo}/allspice_generated/svg/{content}"

    class ArchiveFormat(Enum):
        """
        Archive formats for Repository.get_archive
        """

        TAR = "tar.gz"
        ZIP = "zip"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Repository): return False
        return self.owner == other.owner and self.name == other.name

    def __hash__(self):
        return hash(self.owner) ^ hash(self.name)

    _fields_to_parsers = {
        # dont know how to tell apart user and org as owner except form email being empty.
        "owner": lambda allspice_client, r: Organization.parse_response(allspice_client, r)
        if r["email"] == "" else User.parse_response(allspice_client, r),
        "updated_at": lambda allspice_client, t: Util.convert_time(t),
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, name: str):
        return cls._request(allspice_client, {"owner": owner, "name": name})

    _patchable_fields = {
        "allow_manual_merge",
        "allow_merge_commits",
        "allow_rebase",
        "allow_rebase_explicit",
        "allow_rebase_update",
        "allow_squash_merge",
        "archived",
        "autodetect_manual_merge",
        "default_branch",
        "default_delete_branch_after_merge",
        "default_merge_style",
        "description",
        "enable_prune",
        "external_tracker",
        "external_wiki",
        "has_issues",
        "has_projects",
        "has_pull_requests",
        "has_wiki",
        "ignore_whitespace_conflicts",
        "internal_tracker",
        "mirror_interval",
        "name",
        "private",
        "template",
        "website",
    }

    def commit(self):
        args = {"owner": self.owner.username, "name": self.name}
        self._commit(args)

    def get_branches(self) -> List['Branch']:
        """Get all the Branches of this Repository."""

        results = self.allspice_client.requests_get_paginated(
            Repository.REPO_BRANCHES % (self.owner.username, self.name)
        )
        return [Branch.parse_response(self.allspice_client, result) for result in results]

    def get_branch(self, name: str) -> 'Branch':
        """Get a specific Branch of this Repository."""
        result = self.allspice_client.requests_get(
            Repository.REPO_BRANCH.format(owner=self.owner.username, repo=self.name, branch=name)
        )
        return Branch.parse_response(self.allspice_client, result)


    def add_branch(self, create_from: Branch, newname: str) -> "Branch":
        """Add a branch to the repository"""
        # Note: will only work with gitea 1.13 or higher!
        data = {"new_branch_name": newname, "old_branch_name": create_from.name}
        result = self.allspice_client.requests_post(
            Repository.REPO_BRANCHES % (self.owner.username, self.name), data=data
        )
        return Branch.parse_response(self.allspice_client, result)

    def get_issues(
            self,
            state: Union[Literal["open"], Literal["closed"], Literal["all"]] = "all",
            search_query: Optional[str] = None,
            labels: Optional[List[str]] = None,
            milestones: Optional[List[Union[Milestone, str]]] = None,
            assignee: Optional[Union[User, str]] = None,
            since: Optional[datetime] = None,
            before: Optional[datetime] = None,
    ) -> List["Issue"]:
        """
        Get all Issues of this Repository (open and closed)

        https://hub.allspice.io/api/swagger#/repository/repoListIssues

        All params of this method are optional filters. If you don't specify a filter, it
        will not be applied.

        :param state: The state of the Issues to get. If None, all Issues are returned.
        :param search_query: Filter issues by text. This is equivalent to searching for
                             `search_query` in the Issues on the web interface.
        :param labels: Filter issues by labels.
        :param milestones: Filter issues by milestones.
        :param assignee: Filter issues by the assigned user.
        :param since: Filter issues by the date they were created.
        :param before: Filter issues by the date they were created.
        :return: A list of Issues.
        """

        data = {
            "state": state,
        }
        if search_query:
            data["q"] = search_query
        if labels:
            data["labels"] = ",".join(labels)
        if milestones:
            data["milestone"] = ",".join(
                [milestone.name if isinstance(milestone, Milestone) else milestone for
                 milestone in milestones]
            )
        if assignee:
            if isinstance(assignee, User):
                data["assignee"] = assignee.username
            else:
                data["assignee"] = assignee
        if since:
            data["since"] = Util.format_time(since)
        if before:
            data["before"] = Util.format_time(before)

        results = self.allspice_client.requests_get_paginated(
            Repository.REPO_ISSUES.format(owner=self.owner.username, repo=self.name),
            params=data,
        )

        issues = []
        for result in results:
            issue = Issue.parse_response(self.allspice_client, result)
            # This is mostly for compatibility with the older implementation, as the
            # `repository` property already has this info in the parsed Issue.
            Issue._add_read_property("repo", self, issue)
            Issue._add_read_property("owner", self.owner, issue)
            issues.append(issue)

        return issues

    def get_design_reviews(
            self,
            state: Union[Literal["open"], Literal["closed"], Literal["all"]] = "all",
            milestone: Optional[Union[Milestone, str]] = None,
            labels: Optional[List[str]] = None,
    ) -> List["DesignReview"]:
        """
        Get all Design Reviews of this Repository.

        https://hub.allspice.io/api/swagger#/repository/repoListPullRequests

        :param state: The state of the Design Reviews to get. If None, all Design Reviews
                      are returned.
        :param milestone: The milestone of the Design Reviews to get.
        :param labels: A list of label IDs to filter DRs by.
        :return: A list of Design Reviews.
        """

        params = {
            "state": state,
        }
        if milestone:
            if isinstance(milestone, Milestone):
                params["milestone"] = milestone.name
            else:
                params["milestone"] = milestone
        if labels:
            params["labels"] = ",".join(labels)

        results = self.allspice_client.requests_get_paginated(
            self.REPO_DESIGN_REVIEWS.format(owner=self.owner.username,
                                            repo=self.name),
            params=params,
        )
        return [DesignReview.parse_response(self.allspice_client, result)
                for result in results]

    def get_commits(
            self,
            sha: Optional[str] = None,
            path: Optional[str] = None,
            stat: bool = True,
    ) -> List["Commit"]:
        """
        Get all the Commits of this Repository.

        https://hub.allspice.io/api/swagger#/repository/repoGetAllCommits

        :param sha: The SHA of the commit to start listing commits from.
        :param path: filepath of a file/dir.
        :param stat: Include the number of additions and deletions in the response.
                     Disable for speedup.
        :return: A list of Commits.
        """

        data = {}
        if sha:
            data["sha"] = sha
        if path:
            data["path"] = path
        if not stat:
            data["stat"] = False

        try:
            results = self.allspice_client.requests_get_paginated(
                Repository.REPO_COMMITS % (self.owner.username, self.name),
                params=data,
            )
        except ConflictException as err:
            logging.warning(err)
            logging.warning(
                "Repository %s/%s is Empty" % (self.owner.username, self.name)
            )
            results = []
        return [Commit.parse_response(self.allspice_client, result) for result in results]

    def get_issues_state(self, state) -> List["Issue"]:
        """
        DEPRECATED: Use get_issues() instead.

        Get issues of state Issue.open or Issue.closed of a repository.
        """

        assert state in [Issue.OPENED, Issue.CLOSED]
        issues = []
        data = {"state": state}
        results = self.allspice_client.requests_get_paginated(
            Repository.REPO_ISSUES.format(owner=self.owner.username, repo=self.name), params=data
        )
        for result in results:
            issue = Issue.parse_response(self.allspice_client, result)
            # adding data not contained in the issue answer
            Issue._add_read_property("repo", self, issue)
            Issue._add_read_property("owner", self.owner, issue)
            issues.append(issue)
        return issues

    def get_times(self):
        results = self.allspice_client.requests_get(
            Repository.REPO_TIMES % (self.owner.username, self.name)
        )
        return results

    def get_user_time(self, username) -> float:
        if isinstance(username, User):
            username = username.username
        results = self.allspice_client.requests_get(
            Repository.REPO_USER_TIME % (self.owner.username, self.name, username)
        )
        time = sum(r["time"] for r in results)
        return time

    def get_full_name(self) -> str:
        return self.owner.username + "/" + self.name

    def create_issue(self, title, assignees=frozenset(), description="") -> ApiObject:
        data = {
            "assignees": assignees,
            "body": description,
            "closed": False,
            "title": title,
        }
        result = self.allspice_client.requests_post(
            Repository.REPO_ISSUES.format(owner=self.owner.username, repo=self.name), data=data
        )
        return Issue.parse_response(self.allspice_client, result)

    def create_design_review(
            self,
            title: str,
            head: Union[Branch, str],
            base: Union[Branch, str],
            assignees: Optional[Set[Union[User, str]]] = None,
            body: Optional[str] = None,
            due_date: Optional[datetime] = None,
            milestone: Optional['Milestone'] = None,
    ) -> 'DesignReview':
        """
        Create a new Design Review.

        See https://hub.allspice.io/api/swagger#/repository/repoCreatePullRequest

        :param title: Title of the Design Review
        :param head: Branch or name of the branch to merge into the base branch
        :param base: Branch or name of the branch to merge into
        :param assignees: Optional. A list of users to assign this review. List can be of
                          User objects or of usernames.
        :param body: An Optional Description for the Design Review.
        :param due_date: An Optional Due date for the Design Review.
        :param milestone: An Optional Milestone for the Design Review
        :return: The created Design Review
        """

        data = {
            "title": title,
        }

        if isinstance(head, Branch):
            data["head"] = head.name
        else:
            data["head"] = head
        if isinstance(base, Branch):
            data["base"] = base.name
        else:
            data["base"] = base
        if assignees:
            data["assignees"] = [a.username if isinstance(a, User) else a for a in
                                 assignees]
        if body:
            data["body"] = body
        if due_date:
            data["due_date"] = Util.format_time(due_date)
        if milestone:
            data["milestone"] = milestone.id

        result = self.allspice_client.requests_post(
            self.REPO_DESIGN_REVIEWS.format(owner=self.owner.username, repo=self.name),
            data=data
        )

        return DesignReview.parse_response(self.allspice_client, result)

    def create_milestone(self, title: str, description: str, due_date: str = None, state: str = "open") -> "Milestone":
        url = Repository.REPO_MILESTONES.format(owner=self.owner.username, repo=self.name)
        data = {"title": title, "description": description, "state": state}
        if due_date: data["due_date"] = due_date
        result = self.allspice_client.requests_post(url, data=data)
        return Milestone.parse_response(self.allspice_client, result)

    def create_gitea_hook(self, hook_url: str, events: List[str]):
        url = f"/repos/{self.owner.username}/{self.name}/hooks"
        data = {
            "type": "gitea",
            "config": {"content_type": "json", "url": hook_url},
            "events": events,
            "active": True,
        }
        return self.allspice_client.requests_post(url, data=data)

    def list_hooks(self):
        url = f"/repos/{self.owner.username}/{self.name}/hooks"
        return self.allspice_client.requests_get(url)

    def delete_hook(self, id: str):
        url = f"/repos/{self.owner.username}/{self.name}/hooks/{id}"
        self.allspice_client.requests_delete(url)

    def is_collaborator(self, username) -> bool:
        if isinstance(username, User):
            username = username.username
        try:
            # returns 204 if its ok, 404 if its not
            self.allspice_client.requests_get(
                Repository.REPO_IS_COLLABORATOR
                % (self.owner.username, self.name, username)
            )
            return True
        except:
            return False

    def get_users_with_access(self) -> Sequence[User]:
        url = f"/repos/{self.owner.username}/{self.name}/collaborators"
        response = self.allspice_client.requests_get(url)
        collabs = [User.parse_response(self.allspice_client, user) for user in response]
        if isinstance(self.owner, User):
            return collabs + [self.owner]
        else:
            # owner must be org
            teams = self.owner.get_teams()
            for team in teams:
                team_repos = team.get_repos()
                if self.name in [n.name for n in team_repos]:
                    collabs += team.get_members()
            return collabs

    def remove_collaborator(self, user_name: str):
        url = f"/repos/{self.owner.username}/{self.name}/collaborators/{user_name}"
        self.allspice_client.requests_delete(url)

    def transfer_ownership(self, new_owner: Union["User", "Organization"], new_teams: Set["Team"] = frozenset()):
        url = Repository.REPO_TRANSFER.format(owner=self.owner.username, repo=self.name)
        data = {"new_owner": new_owner.username}
        if isinstance(new_owner, Organization):
            new_team_ids = [team.id for team in new_teams if team in new_owner.get_teams()]
            data["team_ids"] = new_team_ids
        self.allspice_client.requests_post(url, data=data)
        # TODO: make sure this instance is either updated or discarded

    def get_git_content(
            self: str = None,
            ref: Optional["Ref"] = None,
            commit: "Commit" = None
    ) -> List["Content"]:
        """
        Get a list of all files in the repository.

        https://hub.allspice.io/api/swagger#/repository/repoGetContentsList

        :param ref: branch or commit to get content from
        :param commit: commit to get content from (deprecated)
        """
        url = f"/repos/{self.owner.username}/{self.name}/contents"
        data = Util.data_params_for_ref(ref or commit)

        result = [Content.parse_response(self.allspice_client, f) for f in self.allspice_client.requests_get(url, data)]
        return result

    def get_file_content(
            self,
            content: "Content",
            ref: "Ref" = None,
            commit: "Commit" = None,
    ) -> Union[str, List["Content"]]:
        """https://hub.allspice.io/api/swagger#/repository/repoGetContents"""
        url = f"/repos/{self.owner.username}/{self.name}/contents/{content.path}"
        data = Util.data_params_for_ref(ref or commit)

        if content.type == Content.FILE:
            return self.allspice_client.requests_get(url, data)["content"]
        else:
            return [Content.parse_response(self.allspice_client, f) for f in self.allspice_client.requests_get(url, data)]

    def get_generated_json(
            self,
            content: Union[Content, str],
            ref: Optional[Ref] = None
    ) -> dict:
        """
        Get the json blob for a cad file if it exists, otherwise enqueue
        a new job and return a 503 status.

        WARNING: This is still experimental and not recommended for critical
        applications. The structure and content of the returned dictionary can
        change at any time.

        See https://hub.allspice.io/api/swagger#/repository/repoGetAllSpiceJSON
        """

        if isinstance(content, Content):
            content = content.path

        url = self.REPO_GET_ALLSPICE_JSON.format(
            owner=self.owner.username,
            repo=self.name,
            content=content,
        )
        data = Util.data_params_for_ref(ref)
        return self.allspice_client.requests_get(url, data)

    def get_generated_svg(
            self,
            content: Union[Content, str],
            ref: Optional[Ref] = None
    ) -> bytes:
        """
        Get the svg blob for a cad file if it exists, otherwise enqueue
        a new job and return a 503 status.

        WARNING: This is still experimental and not yet recommended for
        critical applications. The content of the returned svg can change
        at any time.

        See https://hub.allspice.io/api/swagger#/repository/repoGetAllSpiceSVG
        """

        if isinstance(content, Content):
            content = content.path

        url = self.REPO_GET_ALLSPICE_SVG.format(
            owner=self.owner.username,
            repo=self.name,
            content=content,
        )
        data = Util.data_params_for_ref(ref)
        return self.allspice_client.requests_get_raw(url, data)

    def create_file(self, file_path: str, content: str, data: dict = None):
        """https://hub.allspice.io/api/swagger#/repository/repoCreateFile"""
        if not data:
            data = {}
        url = f"/repos/{self.owner.username}/{self.name}/contents/{file_path}"
        data.update({"content": content})
        return self.allspice_client.requests_post(url, data)

    def change_file(self, file_path: str, file_sha: str, content: str, data: dict = None):
        """https://hub.allspice.io/api/swagger#/repository/repoCreateFile"""
        if not data:
            data = {}
        url = f"/repos/{self.owner.username}/{self.name}/contents/{file_path}"
        data.update({"sha": file_sha, "content": content})
        return self.allspice_client.requests_put(url, data)

    def get_archive(
            self,
            ref: Ref = "main",
            archive_format: ArchiveFormat = ArchiveFormat.ZIP,
    ) -> bytes:
        """
        Download all the files in a specific ref of a repository as a zip or tarball
        archive.

        https://hub.allspice.io/api/swagger#/repository/repoGetArchive

        :param ref: branch or commit to get content from, defaults to the "main" branch
        :param archive_format: zip or tar, defaults to zip
        """

        ref_string = Util.data_params_for_ref(ref)["ref"]
        url = self.REPO_GET_ARCHIVE.format(
            owner=self.owner.username,
            repo=self.name,
            ref=ref_string,
            format=archive_format.value,
        )
        return self.allspice_client.requests_get_raw(url)

    def delete(self):
        self.allspice_client.requests_delete(
            Repository.REPO_DELETE % (self.owner.username, self.name)
        )
        self.deleted = True


class Milestone(ApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/milestones/{number}"""  # <owner, repo>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Milestone): return False
        return self.allspice_client == other.allspice_client and self.id == other.id

    def __hash__(self):
        return hash(self.allspice_client) ^ hash(self.id)

    _fields_to_parsers = {
        "closed_at": lambda allspice_client, t: Util.convert_time(t),
        "due_on": lambda allspice_client, t: Util.convert_time(t),
    }

    _patchable_fields = {
        "allow_merge_commits",
        "allow_rebase",
        "allow_rebase_explicit",
        "allow_squash_merge",
        "archived",
        "default_branch",
        "description",
        "has_issues",
        "has_pull_requests",
        "has_wiki",
        "ignore_whitespace_conflicts",
        "name",
        "private",
        "website",
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, number: str):
        return cls._request(allspice_client, {"owner": owner, "repo": repo, "number": number})


class Attachment(ReadonlyApiObject):
    """
    An asset attached to a comment.

    You cannot edit or delete the attachment from this object - see the instance methods
    Comment.edit_attachment and delete_attachment for that.
    """

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Attachment):
            return False

        return self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)


class Comment(ApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/issues/comments/{id}"""
    GET_ATTACHMENTS_PATH = """/repos/{owner}/{repo}/issues/comments/{id}/assets"""
    ATTACHMENT_PATH = """/repos/{owner}/{repo}/issues/comments/{id}/assets/{attachment_id}"""

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.repo == other.repo and self.id == other.id

    def __hash__(self):
        return hash(self.repo) ^ hash(self.id)

    @classmethod
    def request(
            cls,
            allspice_client: 'AllSpice',
            owner: str,
            repo: str,
            id: str
    ) -> 'Comment':
        return cls._request(allspice_client, {"owner": owner, "repo": repo, "id": id})

    _fields_to_parsers = {
        "user": lambda allspice_client, r: User.parse_response(allspice_client, r),
        "created_at": lambda allspice_client, t: Util.convert_time(t),
        "updated_at": lambda allspice_client, t: Util.convert_time(t),
    }

    _patchable_fields = {
        "body"
    }

    @property
    def parent_url(self) -> str:
        """URL of the parent of this comment (the issue or the pull request)"""

        if self.issue_url is not None:
            return self.issue_url
        else:
            return self.pull_request_url

    @cached_property
    def repository(self) -> Repository:
        """The repository this comment was posted on."""

        owner_name, repo_name = self.parent_url.split("/")[-4:-2]
        return Repository.request(self.allspice_client, owner_name, repo_name)

    def __fields_for_path(self):
        return {
            "owner": self.repository.owner.username,
            "repo": self.repository.name,
            "id": self.id,
        }

    def commit(self):
        self._commit(self.__fields_for_path())

    def delete(self):
        self.allspice_client.requests_delete(
            self.API_OBJECT.format(**self.__fields_for_path())
        )
        self.deleted = True

    def get_attachments(self) -> List[Attachment]:
        """
        Get all attachments on this comment. This returns Attachment objects, which
        contain a link to download the attachment.

        https://hub.allspice.io/api/swagger#/issue/issueListIssueCommentAttachments
        """

        results = self.allspice_client.requests_get(
            self.GET_ATTACHMENTS_PATH.format(**self.__fields_for_path())
        )
        return [Attachment.parse_response(self.allspice_client, result) for result in
                results]

    def create_attachment(self, file: IO, name: Optional[str] = None) -> Attachment:
        """
        Create an attachment on this comment.

        https://hub.allspice.io/api/swagger#/issue/issueCreateIssueCommentAttachment

        :param file: The file to attach. This should be a file-like object.
        :param name: The name of the file. If not provided, the name of the file will be
                     used.
        :return: The created attachment.
        """

        args = {
            "files": {"attachment": file},
        }
        if name is not None:
            args["params"] = {"name": name}

        result = self.allspice_client.requests_post(
            self.GET_ATTACHMENTS_PATH.format(**self.__fields_for_path()),
            **args,
        )
        return Attachment.parse_response(self.allspice_client, result)

    def edit_attachment(self, attachment: Attachment, data: dict) -> Attachment:
        """
        Edit an attachment.

        The list of params that can be edited is available at
        https://hub.allspice.io/api/swagger#/issue/issueEditIssueCommentAttachment

        :param attachment: The attachment to be edited
        :param data: The data parameter should be a dictionary of the fields to edit.
        :return: The edited attachment
        """

        args = {
            **self.__fields_for_path(),
            "attachment_id": attachment.id,
        }
        result = self.allspice_client.requests_patch(
            self.ATTACHMENT_PATH.format(**args),
            data=data,
        )
        return Attachment.parse_response(self.allspice_client, result)

    def delete_attachment(self, attachment: Attachment):
        """https://hub.allspice.io/api/swagger#/issue/issueDeleteIssueCommentAttachment"""

        args = {
            **self.__fields_for_path(),
            "attachment_id": attachment.id,
        }
        self.allspice_client.requests_delete(self.ATTACHMENT_PATH.format(**args))
        attachment.deleted = True


class Commit(ReadonlyApiObject):

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    _fields_to_parsers = {
        # NOTE: api may return None for commiters that are no allspice users
        "author": lambda allspice_client, u: User.parse_response(allspice_client, u) if u else None
    }

    def __eq__(self, other):
        if not isinstance(other, Commit): return False
        return self.sha == other.sha

    def __hash__(self):
        return hash(self.sha)

    @classmethod
    def parse_response(cls, allspice_client, result) -> 'Commit':
        commit_cache = result["commit"]
        api_object = cls(allspice_client)
        cls._initialize(allspice_client, api_object, result)
        # inner_commit for legacy reasons
        Commit._add_read_property("inner_commit", commit_cache, api_object)
        return api_object


class Issue(ApiObject):
    API_OBJECT = """/repos/{owner}/{repo}/issues/{index}"""  # <owner, repo, index>
    GET_TIME = """/repos/%s/%s/issues/%s/times"""  # <owner, repo, index>
    GET_COMMENTS = """/repos/{owner}/{repo}/issues/{index}/comments"""
    CREATE_ISSUE = """/repos/{owner}/{repo}/issues"""

    OPENED = "open"
    CLOSED = "closed"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Issue):
            return False
        return self.repo == other.repo and self.id == other.id

    def __hash__(self):
        return hash(self.repo) ^ hash(self.id)

    _fields_to_parsers = {
        "milestone": lambda allspice_client, m: Milestone.parse_response(allspice_client, m),
        "user": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "assignee": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "assignees": lambda allspice_client, us: [User.parse_response(allspice_client, u) for u in us],
        "state": lambda allspice_client, s: Issue.CLOSED if s == "closed" else Issue.OPENED,
        # Repository in this request is just a "RepositoryMeta" record, thus request whole object
        "repository": lambda allspice_client, r: Repository.request(allspice_client, r["owner"], r["name"])
    }

    _parsers_to_fields = {
        "milestone": lambda m: m.id,
    }

    _patchable_fields = {
        "assignee",
        "assignees",
        "body",
        "due_date",
        "milestone",
        "state",
        "title",
    }

    def commit(self):
        args = {
            "owner": self.repository.owner.username,
            "repo": self.repository.name,
            "index": self.number,
        }
        self._commit(args)


    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, number: str):
        api_object = cls._request(allspice_client, {"owner": owner, "repo": repo, "index": number})
        return api_object

    @classmethod
    def create_issue(cls, allspice_client: 'AllSpice', repo: Repository, title: str, body: str = ""):
        args = {"owner": repo.owner.username, "repo": repo.name}
        data = {"title": title, "body": body}
        result = allspice_client.requests_post(Issue.CREATE_ISSUE.format(**args), data=data)
        return Issue.parse_response(allspice_client, result)

    def get_time_sum(self, user: User) -> int:
        results = self.allspice_client.requests_get(
            Issue.GET_TIME % (self.owner.username, self.repo.name, self.number)
        )
        return sum(
            result["time"]
            for result in results
            if result and result["user_id"] == user.id
        )

    def get_times(self) -> Optional[Dict]:
        return self.allspice_client.requests_get(
            Issue.GET_TIME % (self.owner.username, self.repository.name, self.number)
        )

    def delete_time(self, time_id: str):
        path = f"/repos/{self.owner.username}/{self.repository.name}/issues/{self.number}/times/{time_id}"
        self.allspice_client.requests_delete(path)

    def add_time(self, time: int, created: str = None, user_name: User = None):
        path = f"/repos/{self.owner.username}/{self.repository.name}/issues/{self.number}/times"
        self.allspice_client.requests_post(
            path, data={"created": created, "time": int(time), "user_name": user_name}
        )

    def get_comments(self) -> List[Comment]:
        """https://hub.allspice.io/api/swagger#/issue/issueGetComments"""

        results = self.allspice_client.requests_get(
            self.GET_COMMENTS.format(
                owner=self.owner.username,
                repo=self.repo.name,
                index=self.number
            )
        )

        return [
            Comment.parse_response(self.allspice_client, result) for result in results
        ]

    def create_comment(self, body: str) -> Comment:
        """https://hub.allspice.io/api/swagger#/issue/issueCreateComment"""

        path = self.GET_COMMENTS.format(
            owner=self.owner.username,
            repo=self.repo.name,
            index=self.number
        )

        response = self.allspice_client.requests_post(path, data={"body": body})
        return Comment.parse_response(self.allspice_client, response)


class DesignReview(ApiObject):
    """
    A Design Review. See
    https://hub.allspice.io/api/swagger#/repository/repoGetPullRequest.

    Note: The base and head fields are not `Branch` objects - they are plain strings
    referring to the branch names. This is because DRs can exist for branches that have
    been deleted, which don't have an associated `Branch` object from the API. You can use
    the `Repository.get_branch` method to get a `Branch` object for a branch if you know
    it exists.
    """

    API_OBJECT = "/repos/{owner}/{repo}/pulls/{index}"
    MERGE_DESIGN_REVIEW = "/repos/{owner}/{repo}/pulls/{index}/merge"
    GET_COMMENTS = "/repos/{owner}/{repo}/issues/{index}/comments"

    OPEN = "open"
    CLOSED = "closed"

    class MergeType(Enum):
        MERGE = "merge"
        REBASE = "rebase"
        REBASE_MERGE = "rebase-merge"
        SQUASH = "squash"
        MANUALLY_MERGED = "manually-merged"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, DesignReview):
            return False
        return self.repo == other.repo and self.id == other.id

    def __hash__(self):
        return hash(self.repo) ^ hash(self.id)

    @classmethod
    def request(cls, allspice_client: 'AllSpice', owner: str, repo: str, number: str):
        api_object = cls._request(allspice_client,
                                  {"owner": owner, "repo": repo, "index": number})
        return api_object

    @classmethod
    def parse_response(cls, allspice_client, result) -> 'DesignReview':
        api_object = super().parse_response(allspice_client, result)
        cls._add_read_property(
            "repository",
            Repository.parse_response(allspice_client,
                                      result["base"]["repo"]),
            api_object
        )

        return api_object

    @classmethod
    def request(cls, allspice_client, owner: str, repo: str, number: str):
        """See https://hub.allspice.io/api/swagger#/repository/repoGetPullRequest"""
        return cls._request(allspice_client,
                            {"owner": owner, "repo": repo, "index": number})

    _fields_to_parsers = {
        "assignee": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "assignees": lambda allspice_client, us: [User.parse_response(allspice_client, u)
                                                  for u in us],
        "base": lambda allspice_client, b: b["ref"],
        "head": lambda allspice_client, h: h["ref"],
        "merged_by": lambda allspice_client, u: User.parse_response(allspice_client, u),
        "milestone": lambda allspice_client, m: Milestone.parse_response(allspice_client,
                                                                         m),
        "user": lambda allspice_client, u: User.parse_response(allspice_client, u),
    }

    _patchable_fields = {
        "allow_maintainer_edits",
        "assignee",
        "assignees",
        "base",
        "body",
        "due_date",
        "milestone",
        "state",
        "title",
    }

    _parsers_to_fields = {
        "assignee": lambda u: u.username,
        "assignees": lambda us: [u.username for u in us],
        "base": lambda b: b.name if isinstance(b, Branch) else b,
        "milestone": lambda m: m.id,
    }

    def commit(self):
        data = self.get_dirty_fields()
        if "due_date" in data and data["due_date"] is None:
            data["unset_due_date"] = True

        args = {
            "owner": self.repository.owner.username,
            "repo": self.repository.name,
            "index": self.number
        }
        self._commit(args, data)

    def merge(self, merge_type: MergeType):
        """
        Merge the pull request. See
        https://hub.allspice.io/api/swagger#/repository/repoMergePullRequest

        :param merge_type: The type of merge to perform. See the MergeType enum.
        """

        self.allspice_client.requests_put(
            self.MERGE_DESIGN_REVIEW.format(owner=self.repository.owner.username,
                                            repo=self.repository.name,
                                            index=self.number),
            data={"Do": merge_type.value},
        )

    def get_comments(self) -> List[Comment]:
        """
        Get the comments on this pull request, but not specifically on a review.

        https://hub.allspice.io/api/swagger#/issue/issueGetComments

        :return: A list of comments on this pull request.
        """

        results = self.allspice_client.requests_get(
            self.GET_COMMENTS.format(
                owner=self.repository.owner.username,
                repo=self.repository.name,
                index=self.number
            )
        )
        return [
            Comment.parse_response(self.allspice_client, result) for result in results
        ]

    def create_comment(self, body: str):
        """
        Create a comment on this pull request. This uses the same endpoint as the
        comments on issues, and will not be associated with any reviews.

        https://hub.allspice.io/api/swagger#/issue/issueCreateComment

        :param body: The body of the comment.
        :return: The comment that was created.
        """

        result = self.allspice_client.requests_post(
            self.GET_COMMENTS.format(
                owner=self.repository.owner.username,
                repo=self.repository.name,
                index=self.number
            ),
            data={"body": body}
        )
        return Comment.parse_response(self.allspice_client, result)


class Team(ApiObject):
    API_OBJECT = """/teams/{id}"""  # <id>
    ADD_REPO = """/teams/%s/repos/%s/%s"""  # <id, org, repo>
    TEAM_DELETE = """/teams/%s"""  # <id>
    GET_MEMBERS = """/teams/%s/members"""  # <id>
    GET_REPOS = """/teams/%s/repos"""  # <id>

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Team): return False
        return self.organization == other.organization and self.id == other.id

    def __hash__(self):
        return hash(self.organization) ^ hash(self.id)

    _fields_to_parsers = {
        "organization": lambda allspice_client, o: Organization.parse_response(allspice_client, o)
    }

    _patchable_fields = {
        "can_create_org_repo",
        "description",
        "includes_all_repositories",
        "name",
        "permission",
        "units",
        "units_map",
    }

    @classmethod
    def request(cls, allspice_client: 'AllSpice', id: int):
        return cls._request(allspice_client, {"id": id})

    def commit(self):
        args = {"id": self.id}
        self._commit(args)

    def add_user(self, user: User):
        """https://hub.allspice.io/api/swagger#/organization/orgAddTeamMember"""
        url = f"/teams/{self.id}/members/{user.login}"
        self.allspice_client.requests_put(url)

    def add_repo(self, org: Organization, repo: Repository):
        self.allspice_client.requests_put(Team.ADD_REPO % (self.id, org, repo.name))

    def get_members(self):
        """ Get all users assigned to the team. """
        results = self.allspice_client.requests_get(Team.GET_MEMBERS % self.id)
        return [User.parse_response(self.allspice_client, result) for result in results]

    def get_repos(self):
        """ Get all repos of this Team."""
        results = self.allspice_client.requests_get(Team.GET_REPOS % self.id)
        return [Repository.parse_response(self.allspice_client, result) for result in results]

    def delete(self):
        self.allspice_client.requests_delete(Team.TEAM_DELETE % self.id)
        self.deleted = True

    def remove_team_member(self, user_name: str):
        url = f"/teams/{self.id}/members/{user_name}"
        self.allspice_client.requests_delete(url)


class Content(ReadonlyApiObject):
    FILE = "file"

    def __init__(self, allspice_client):
        super().__init__(allspice_client)

    def __eq__(self, other):
        if not isinstance(other, Team): return False
        return self.repo == self.repo and self.sha == other.sha and self.name == other.name

    def __hash__(self):
        return hash(self.repo) ^ hash(self.sha) ^ hash(self.name)


Ref = Union[Branch, Commit, str]


class Util:
    @staticmethod
    def convert_time(time: str) -> datetime:
        """ Parsing of strange Gitea time format ("%Y-%m-%dT%H:%M:%S:%z" but with ":" in time zone notation)"""
        try:
            return datetime.strptime(time[:-3] + "00", "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return datetime.strptime(time[:-3] + "00", "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def format_time(time: datetime) -> str:
        """
        Format a datetime object to Gitea's time format.

        :param time: The time to format
        :return: Formatted time
        """

        return time.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"

    @staticmethod
    def data_params_for_ref(ref: Optional[Ref]) -> Dict:
        """
        Given a "ref", returns a dict with the ref parameter for the API call.

        If the ref is None, returns an empty dict. You can pass this to the API
        directly.
        """

        if isinstance(ref, Branch):
            return {"ref": ref.name}
        elif isinstance(ref, Commit):
            return {"ref": ref.sha}
        elif ref:
            return {"ref": ref}
        else:
            return {}
