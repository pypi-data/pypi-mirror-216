# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from ...aio.asyncclient import AsyncBaseClient
from ...aio.asyncclient import createApiClient
from ...aio.asyncclient import config
from ...aio.asyncclient import createTemporaryCredentials
from ...aio.asyncclient import createSession
_defaultConfig = config


class Github(AsyncBaseClient):
    """
    The github service is responsible for creating tasks in response
    to GitHub events, and posting results to the GitHub UI.

    This document describes the API end-point for consuming GitHub
    web hooks, as well as some useful consumer APIs.

    When Github forbids an action, this service returns an HTTP 403
    with code ForbiddenByGithub.
    """

    classOptions = {
    }
    serviceName = 'github'
    apiVersion = 'v1'

    async def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    async def lbheartbeat(self, *args, **kwargs):
        """
        Load Balancer Heartbeat

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["lbheartbeat"], *args, **kwargs)

    async def version(self, *args, **kwargs):
        """
        Taskcluster Version

        Respond with the JSON version object.
        https://github.com/mozilla-services/Dockerflow/blob/main/docs/version_object.md

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["version"], *args, **kwargs)

    async def githubWebHookConsumer(self, *args, **kwargs):
        """
        Consume GitHub WebHook

        Capture a GitHub event and publish it via pulse, if it's a push,
        release, check run or pull request.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["githubWebHookConsumer"], *args, **kwargs)

    async def builds(self, *args, **kwargs):
        """
        List of Builds

        A paginated list of builds that have been run in
        Taskcluster. Can be filtered on various git-specific
        fields.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["builds"], *args, **kwargs)

    async def cancelBuilds(self, *args, **kwargs):
        """
        Cancel repository builds

        Cancel all running Task Groups associated with given repository and sha or pullRequest number

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["cancelBuilds"], *args, **kwargs)

    async def badge(self, *args, **kwargs):
        """
        Latest Build Status Badge

        Checks the status of the latest build of a given branch
        and returns corresponding badge svg.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["badge"], *args, **kwargs)

    async def repository(self, *args, **kwargs):
        """
        Get Repository Info

        Returns any repository metadata that is
        useful within Taskcluster related services.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["repository"], *args, **kwargs)

    async def latest(self, *args, **kwargs):
        """
        Latest Status for Branch

        For a given branch of a repository, this will always point
        to a status page for the most recent task triggered by that
        branch.

        Note: This is a redirect rather than a direct link.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["latest"], *args, **kwargs)

    async def createStatus(self, *args, **kwargs):
        """
        Post a status against a given changeset

        For a given changeset (SHA) of a repository, this will attach a "commit status"
        on github. These statuses are links displayed next to each revision.
        The status is either OK (green check) or FAILURE (red cross),
        made of a custom title and link.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["createStatus"], *args, **kwargs)

    async def createComment(self, *args, **kwargs):
        """
        Post a comment on a given GitHub Issue or Pull Request

        For a given Issue or Pull Request of a repository, this will write a new message.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createComment"], *args, **kwargs)

    async def renderTaskclusterYml(self, *args, **kwargs):
        """
        Render .taskcluster.yml file

        This endpoint allows to render the .taskcluster.yml file for a given event or payload.
        This is useful to preview the result of the .taskcluster.yml file before pushing it to
        the repository.
        Read more about the .taskcluster.yml file in the [documentation](https://docs.taskcluster.net/docs/reference/integrations/github/taskcluster-yml-v1)

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["renderTaskclusterYml"], *args, **kwargs)

    async def heartbeat(self, *args, **kwargs):
        """
        Heartbeat

        Respond with a service heartbeat.

        This endpoint is used to check on backing services this service
        depends on.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["heartbeat"], *args, **kwargs)

    funcinfo = {
        "badge": {
            'args': ['owner', 'repo', 'branch'],
            'method': 'get',
            'name': 'badge',
            'route': '/repository/<owner>/<repo>/<branch>/badge.svg',
            'stability': 'experimental',
        },
        "builds": {
            'args': [],
            'method': 'get',
            'name': 'builds',
            'output': 'v1/build-list.json#',
            'query': ['continuationToken', 'limit', 'organization', 'repository', 'sha', 'pullRequest'],
            'route': '/builds',
            'stability': 'stable',
        },
        "cancelBuilds": {
            'args': ['owner', 'repo'],
            'method': 'post',
            'name': 'cancelBuilds',
            'output': 'v1/build-list.json#',
            'query': ['sha', 'pullRequest'],
            'route': '/builds/<owner>/<repo>/cancel',
            'stability': 'stable',
        },
        "createComment": {
            'args': ['owner', 'repo', 'number'],
            'input': 'v1/create-comment.json#',
            'method': 'post',
            'name': 'createComment',
            'route': '/repository/<owner>/<repo>/issues/<number>/comments',
            'stability': 'stable',
        },
        "createStatus": {
            'args': ['owner', 'repo', 'sha'],
            'input': 'v1/create-status.json#',
            'method': 'post',
            'name': 'createStatus',
            'route': '/repository/<owner>/<repo>/statuses/<sha>',
            'stability': 'experimental',
        },
        "githubWebHookConsumer": {
            'args': [],
            'method': 'post',
            'name': 'githubWebHookConsumer',
            'route': '/github',
            'stability': 'stable',
        },
        "heartbeat": {
            'args': [],
            'method': 'get',
            'name': 'heartbeat',
            'route': '/__heartbeat__',
            'stability': 'stable',
        },
        "latest": {
            'args': ['owner', 'repo', 'branch'],
            'method': 'get',
            'name': 'latest',
            'route': '/repository/<owner>/<repo>/<branch>/latest',
            'stability': 'stable',
        },
        "lbheartbeat": {
            'args': [],
            'method': 'get',
            'name': 'lbheartbeat',
            'route': '/__lbheartbeat__',
            'stability': 'stable',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
        "renderTaskclusterYml": {
            'args': [],
            'input': 'v1/render-taskcluster-yml-input.json#',
            'method': 'post',
            'name': 'renderTaskclusterYml',
            'output': 'v1/render-taskcluster-yml-output.json#',
            'route': '/taskcluster-yml',
            'stability': 'experimental',
        },
        "repository": {
            'args': ['owner', 'repo'],
            'method': 'get',
            'name': 'repository',
            'output': 'v1/repository.json#',
            'route': '/repository/<owner>/<repo>',
            'stability': 'experimental',
        },
        "version": {
            'args': [],
            'method': 'get',
            'name': 'version',
            'route': '/__version__',
            'stability': 'stable',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Github']
