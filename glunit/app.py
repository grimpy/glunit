import flask
import os
from .gitlab import GitLab
from junit2html.junit2html import Junit2HTML

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)


def run():
    app.config.from_object('config')
    app.config['gitlab'] = GitLab(app.config["GITLAB_URL"], app.config["GITLAB_TOKEN"])
    app.config['junit2html'] = Junit2HTML()
    app.run(host="0.0.0.0", port=8080, debug=False)


@app.route("/", methods=["GET"])
def index():
    gitlab = app.config["gitlab"]
    groups = gitlab.list_groups()
    return flask.render_template("index.html", groups=groups)

@app.route("/groups/<groupid>", methods=["GET"])
def group(groupid):
    gitlab = app.config["gitlab"]
    projects = gitlab.list_group_projects(groupid)
    return flask.render_template("group.html", projects=projects)

@app.route("/projects/<projectid>", methods=["GET"])
def pipelines(projectid):
    gitlab = app.config["gitlab"]
    pipelines = gitlab.list_pipelines(projectid)
    return flask.render_template("project.html", pipelines=pipelines, project=projectid)

@app.route("/projects/<projectid>/pipelines/<pipelineid>")
def pipeline(projectid, pipelineid):
    gitlab = app.config["gitlab"]
    pipeline = gitlab.get_pipeline(projectid, pipelineid)
    jobs = gitlab.list_pipeline_jobs(projectid, pipelineid)
    return flask.render_template("pipeline.html", pipeline=pipeline, jobs=jobs, project=projectid)

@app.route("/projects/<projectid>/jobs/<jobid>")
def job(projectid, jobid):
    gitlab = app.config["gitlab"]
    job = gitlab.get_job(projectid, jobid)
    unit = None
    unithtml = ""
    for artifact in job['artifacts']:
        if artifact['file_type'] == 'junit':
            unit = gitlab.get_job_artifact(projectid, jobid, "{}.xml".format(jobid))
            break
    if unit:
        junit2html = app.config['junit2html']
        result = junit2html.parse_content(unit)
        unithtml = junit2html.generate_html(result)
    return flask.render_template("job.html", pipeline=pipeline, job=job, project=projectid, unithtml=unithtml)

