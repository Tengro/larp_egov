from fabric import Connection
from fabric import task


@task
def deploy(ctx):
    host = "159.89.14.43"
    user = "larp_egov"
    project_dir = "/home/larp_egov/larp_egov/larp_egov/api/"
    conn = Connection(f"{user}@{host}")
    with conn.cd(project_dir):
        conn.run("git pull --rebase origin master")
        conn.run("workon larp_egov && ./manage.py migrate")
        conn.run("sudo systemctl restart gunicorn celery nginx celerybeat", pty=True)
