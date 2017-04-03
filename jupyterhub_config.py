import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({'command': spawn_cmd})
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = {'network_mode': network_name}
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir}
c.DockerSpawner.extra_create_kwargs.update({'volume_driver': 'local'})
# vocloud filesystem and jobs volumes
filesystem_path = os.environ.get('VOCLOUD_FILESYSTEM_PATH')
jobs_path = os.environ.get('VOCLOUD_JOBS_PATH')
vocloud_volumes = dict()
if filesystem_path is not None:
    vocloud_volumes[filesystem_path] = os.path.join(notebook_dir, 'filesystem')
if jobs_path is not None:
    vocloud_volumes[jobs_path] = os.path.join(notebook_dir, 'jobs')
c.DockerSpawner.read_only_volumes = vocloud_volumes
# Set space for every user's notebook if necessary
# c.Spawner.mem_limit = '2G'
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# c.JupyterHub.log_level = 'DEBUG'  # to increase log level for debugging purposes

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = os.environ['DOCKER_CONTAINER_NAME']
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 80
# c.JupyterHub.ssl_key = os.environ['SSL_KEY']
# c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'vocloud_authenticator.VocloudAuthenticator'
c.VocloudAuthenticator.vocloud_url = os.environ['VOCLOUD_URL']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.base_url = os.environ.get('JUPYTERHUB_BASE_URL')
c.JupyterHub.db_url = os.path.join('sqlite:///', data_dir, 'jupyterhub.sqlite')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
                                               'jupyterhub_cookie_secret')

# Add service to kill idle notebooks
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python cull_idle_servers.py --timeout=3600'.split(),
    }
]

# # Whitlelist users and admins
# c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = {'admin'}
c.JupyterHub.admin_access = True
# pwd = os.path.dirname(__file__)
# with open(os.path.join(pwd, 'userlist')) as f:
#     for line in f:
#         if not line:
#             continue
#         parts = line.split()
#         name = parts[0]
#         whitelist.add(name)
#         if len(parts) > 1 and parts[1] == 'admin':
#             admin.add(name)
