"""Read-only verification adapters; tests inject explicitly labelled MOCK adapters."""
import base64
import json
import os
import re
import urllib.parse
import urllib.request

from engine import Block, require


class GitHub:
    def __init__(self, credential):
        self.credential = credential

    def get(self, path):
        require(self.credential, 'NOT_EXECUTED GitHub credential unavailable')
        request = urllib.request.Request('https://api.github.com/' + path, headers={
            'Authorization': 'Bearer ' + self.credential,
            'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310 -- GitHub requests use the literal HTTPS api.github.com origin.
                return json.load(response)
        except Exception:
            raise Block('NOT_EXECUTED GitHub verification unavailable') from None

    def pages(self, path):
        results = []
        for page in range(1, 101):
            batch = self.get(f'{path}?per_page=100&page={page}')
            require(isinstance(batch, list), 'INVALID GitHub response')
            results.extend(batch)
            if len(batch) < 100:
                return results
        raise Block('NOT_EXECUTED GitHub pagination limit')

    def __call__(self, record):
        repo = record.get('repository', '')
        require(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo), 'INVALID GitHub repository')
        number = record.get('pull_request')
        require(type(number) is int and number > 0, 'INVALID PR number')
        path = f'repos/{repo}/pulls/{number}'
        pr = self.get(path)
        commits = self.pages(path + '/commits')
        require(type(pr.get('commits')) is int and pr['commits'] == len(commits), 'review incomplete commit list')
        return pr, commits, self.pages(path + '/reviews')


class JenkinsArchive:
    def __init__(self):
        self.base = os.environ.get('JENKINS_URL', '')

    def __call__(self, artifact):
        parsed = urllib.parse.urlsplit(self.base)
        require(parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password, 'NOT_EXECUTED Jenkins archive configuration unavailable')
        job = '/'.join('job/' + urllib.parse.quote(p, safe='') for p in str(artifact['job']).split('/'))
        require(str(artifact['build']).isdigit(), 'INVALID Jenkins build')
        path = urllib.parse.quote(artifact['path'], safe='/')
        url = self.base.rstrip('/') + f'/{job}/{artifact["build"]}/artifact/{path}'
        headers = {}
        user, credential = os.environ.get("JENKINS_API_USER"), os.environ.get("JENKINS_API_TOKEN")
        require(bool(user) == bool(credential), "NOT_EXECUTED Jenkins credential incomplete")
        if user and credential:
            headers["Authorization"] = "Basic " + base64.b64encode(f"{user}:{credential}".encode()).decode()
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310 -- Jenkins base scheme and hostname are validated above as HTTPS.
                return response.read()
        except Exception:
            raise Block('NOT_EXECUTED Jenkins archive unavailable') from None
