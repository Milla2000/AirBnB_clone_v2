#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""
import os
from fabric.api import *
from datetime import datetime

env.hosts = ['54.234.89.183', '100.26.165.1']  
env.user = 'ubuntu'  

def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder. """
    try:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')
        file_path = 'versions/web_static_{}.tgz'.format(now)
        local('tar -cvzf {} web_static'.format(file_path))
        return file_path
    except:
        return None

def do_deploy(archive_path):
    """ Distributes an archive to your web servers. """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    file_no_ext = os.path.splitext(file_name)[0]

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(file_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(file_name, file_no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'
            .format(file_no_ext, file_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(file_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(file_no_ext))
        return True
    except:
        return False

def deploy():
    """ Full deployment process. """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
