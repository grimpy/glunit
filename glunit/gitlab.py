import requests
import urllib

class GitLab:
    def __init__(self, baseurl, token):
        self.baseurl = baseurl + "/api/v4"
        self.session = requests.Session()
        self.session.headers["PRIVATE-TOKEN"] = token

    def list_pipelines(self, project):
        url = "{}/projects/{}/pipelines".format(self.baseurl, urllib.parse.quote(project, ""))
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_pipeline(self, project, pipelineid):
        url = "{}/projects/{}/pipelines/{}".format(self.baseurl, urllib.parse.quote(project, ""), pipelineid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_pipeline_jobs(self, project, pipelineid):
        url = "{}/projects/{}/pipelines/{}/jobs/".format(self.baseurl, urllib.parse.quote(project, ""), pipelineid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_job(self, project, jobid):
        url = "{}/projects/{}/jobs/{}".format(self.baseurl, urllib.parse.quote(project, ""), jobid)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_job_artifact(self, project, jobid, artifact):
        # /projects/:id/jobs/:job_id/artifacts/*artifact_path
        url = "{}/projects/{}/jobs/{}/artifacts/{}".format(self.baseurl, urllib.parse.quote(project, ""), jobid, artifact)
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

