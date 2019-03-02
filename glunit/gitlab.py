import requests
import urllib
from flask import request

class GitLab:
    def __init__(self, baseurl, token):
        self.baseurl = baseurl + "/api/v4"
        self.session = requests.Session()
        self.session.headers["PRIVATE-TOKEN"] = token

    def list_pipelines(self, project):
        url = "{}/projects/{}/pipelines".format(self.baseurl, urllib.parse.quote(project, ""))
        return self.list(url)[0]

    def list(self, url):
        page = request.args.get('page', 1)
        response = self.session.get(url, params={'page': page})
        response.raise_for_status()
        return response.json(), response.headers['X-Total-Pages']

    def list_projects(self):
        url = "{}/projects/".format(self.baseurl)
        return self.list(url)[0]

    def list_group_projects(self, group):
        url = "{}/groups/{}/projects/".format(self.baseurl, group)
        return self.list(url)[0]

    def list_groups(self):
        url = "{}/groups/".format(self.baseurl)
        return self.list(url)[0]

    def get_pipeline(self, project, pipelineid):
        url = "{}/projects/{}/pipelines/{}".format(self.baseurl, urllib.parse.quote(project, ""), pipelineid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_pipeline_jobs(self, project, pipelineid):
        url = "{}/projects/{}/pipelines/{}/jobs/".format(self.baseurl, urllib.parse.quote(project, ""), pipelineid)
        return self.list(url)[0]

    def get_job(self, project, jobid):
        url = "{}/projects/{}/jobs/{}".format(self.baseurl, urllib.parse.quote(project, ""), jobid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_job_artifact(self, project, jobid, artifact):
        url = "{}/projects/{}/jobs/{}/artifacts/{}".format(self.baseurl, urllib.parse.quote(project, ""), jobid, artifact)
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def get_job_trace(self, project, jobid):
        url = "{}/projects/{}/jobs/{}/trace".format(self.baseurl, urllib.parse.quote(project, ""), jobid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

