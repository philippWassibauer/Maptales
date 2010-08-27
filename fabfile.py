from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
import settings as settings

env.hosts = ['root@maptales.com']
env.shell = "/bin/bash -li -c"

dev_url = "maptales.com"

def deploy():
    with cd('/home/maptales/'):
        run('/etc/init.d/apache2 stop')
        run('git pull origin master')
        
        #run("workon zweitwelt; pip install -r requirements/project.txt")
        run("source /home/pinax-master/bin/activate; python manage.py build_static --noinput;")
        run('/etc/init.d/apache2 start')
        #run("workon zweitwelt; python manage.py loaddata cms.json")
        #run("pkill -f run_gunicorn;")
        #run("workon zweitwelt; nohup python manage.py run_gunicorn %s"%(dev_url,))
        
