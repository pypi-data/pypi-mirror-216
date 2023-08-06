# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyterhub_nomad_spawner',
 'jupyterhub_nomad_spawner.consul',
 'jupyterhub_nomad_spawner.nomad']

package_data = \
{'': ['*'], 'jupyterhub_nomad_spawner': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'attrs>=23.1.0,<24.0.0',
 'httpx>=0.24.0,<0.25.0',
 'jupyterhub>=4.0.1,<5.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'traitlets>=5.1.1,<6.0.0']

entry_points = \
{'jupyterhub.spawners': ['nomad-spawner = '
                         'jupyterhub_nomad_spawner.spawner:NomadSpawner']}

setup_kwargs = {
    'name': 'jupyterhub-nomad-spawner',
    'version': '0.2.0',
    'description': 'A JupyterHub Spawner that launches isolated notebooks as job',
    'long_description': '# Nomad Jupyter Spawner\n\n\n> **Warning**\n> This project is currently in beta\n\nSpawns a Jupyter Notebook via Jupyterhub.\n\nUsers can select and image, resource and connect it with volumes (csi / host)\n\n```sh\npip install jupyterhub-nomad-spawner\n```\n\n## Show Case\nhttps://user-images.githubusercontent.com/1607547/182332760-b0f96ba2-faa8-47b6-9bd7-db93b8d31356.mp4\n\n\nTODOs:\n- Document setup\n- Namespace support\n\n\n## Usage\n\n### Config\n```python\n\nimport json\nimport os\nimport socket\n\nfrom jupyterhub.auth import DummyAuthenticator\nimport tarfile\nc.JupyterHub.spawner_class = "nomad-spawner"\nc.JupyterHub.bind_url = "http://0.0.0.0:8000"\nc.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"\nc.JupyterHub.hub_connect_url = f"http://{os.environ.get(\'NOMAD_IP_api\')}:{os.environ.get(\'NOMAD_HOST_PORT_api\')}"\n\nc.JupyterHub.allow_named_servers = True\nc.JupyterHub.named_server_limit_per_user = 5\n\nc.JupyterHub.authenticator_class = DummyAuthenticator\n\nc.NomadSpawner.mem_limit = "2G"\nc.NomadSpawner.datacenters = ["dc1", "dc2", "dc3"]\n\n```\n\n\n### Nomad Job\n\n\n```hcl\n\njob "jupyterhub" {\n    type = "service"\n\n    datacenters = ["dc1"]\n\n    group "jupyterhub" {\n\n        network {\n            mode = "host"\n            port "hub" {\n                to = 8000\n                static = 8000\n            }\n            port "api" {\n                to = 8081\n            }\n        }\n        task "jupyterhub" {\n            driver = "docker"\n\n            config {\n                image = "mxab/jupyterhub:1"\n                auth_soft_fail = false\n\n                args = [\n                        "jupyterhub",\n                        "-f",\n                        "/local/jupyterhub_config.py",\n                    ]\n                ports = ["hub", "api"]\n\n            }\n            template {\n                destination = "/local/nomad.env"\n                env = true\n                data = <<EOF\n\nNOMAD_ADDR=http://host.docker.internal:4646\nCONSUL_HTTP_ADDR=http://host.docker.internal:8500\n    EOF\n            }\n            template {\n                destination = "/local/jupyterhub_config.py"\n\n                data = <<EOF\nimport json\nimport os\nimport socket\n\nfrom jupyterhub.auth import DummyAuthenticator\nimport tarfile\nc.JupyterHub.spawner_class = "nomad-spawner"\nc.JupyterHub.bind_url = "http://0.0.0.0:8000"\nc.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"\n\nc.JupyterHub.hub_connect_url = f"http://{os.environ.get(\'NOMAD_IP_api\')}:{os.environ.get(\'NOMAD_HOST_PORT_api\')}"\nc.JupyterHub.log_level = "DEBUG"\nc.ConfigurableHTTPProxy.debug = True\n\n\nc.JupyterHub.allow_named_servers = True\nc.JupyterHub.named_server_limit_per_user = 3\n\nc.JupyterHub.authenticator_class = DummyAuthenticator\n\nc.NomadSpawner.datacenters = ["dc1"]\n\nc.NomadSpawner.mem_limit = "2G"\n\n\nc.NomadSpawner.common_images = ["jupyter/minimal-notebook:2022-08-20"]\n\ndef csi_volume_parameters(spawner):\n    if spawner.user_options["volume_csi_plugin_id"] == "nfs":\n        return {\n            "gid" : "1000",\n            "uid" : "1000"\n        }\n    else:\n        return None\nc.NomadSpawner.csi_volume_parameters = csi_volume_parameters\n\n\ndef vault_policies(spawner):\n    return [f"my-policy-{spawner.user.name}"]\nc.NomadSpawner.vault_policies = vault_policies\n\n                EOF\n\n\n            }\n\n            resources {\n                memory = "512"\n            }\n\n        }\n\n        service {\n            name = "jupyter-hub"\n            port = "hub"\n\n            check {\n                type     = "tcp"\n                interval = "10s"\n                timeout  = "2s"\n            }\n\n        }\n        service {\n            name = "jupyter-hub-api"\n            port = "api"\n            check {\n                type     = "tcp"\n                interval = "10s"\n                timeout  = "2s"\n            }\n\n        }\n    }\n}\n\n\n```\n',
    'author': 'Max Fröhlich',
    'author_email': 'maxbruchmann@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
