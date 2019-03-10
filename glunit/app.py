import flask
import os
from .gitlab import GitLab
from junit2html.junit2html import Junit2HTML
from ansi2html import Ansi2HTMLConverter

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
status_map = {"error":"errored", "failed":"exclamation", "skipped":"skipped", "success": "check"}

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
    return flask.render_template("group.html", projects=projects, groupid=groupid)

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
    jobid = flask.request.args.get("job", jobs["data"][0]["id"])
    job = gitlab.get_job(projectid, jobid)
    
    unit = trace = None
    unithtml = ""
    for artifact in job['artifacts']:
        if artifact['file_type'] == 'junit':
            unit = gitlab.get_job_artifact(projectid, jobid, "{}.xml".format(jobid))
            break
    if unit:
        junit2html = app.config['junit2html']
        result = junit2html.parse_content(unit)
        unithtml = junit2html.generate_html(result, embed=True)

    conv = Ansi2HTMLConverter(dark_bg=False, inline=True, markup_lines=True)
    ansi = gitlab.get_job_trace(projectid, jobid).decode('utf8')
    trace = conv.convert(ansi, full=False, ensure_trailing_newline=True)

    return flask.render_template("pipeline.html", pipeline=pipeline, jobs=jobs, project=projectid, job=job, unithtml=unithtml, trace=trace)