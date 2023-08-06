# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto',
 'aserto.client',
 'aserto.client.api',
 'aserto.client.api.authorizer',
 'aserto.client.directory']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'aserto-authorizer==0.20.0',
 'aserto-directory',
 'grpcio>=1.49.1,<2.0.0',
 'protobuf>=4.21.7,<5.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'aserto',
    'version': '0.21.0',
    'description': 'Aserto API client',
    'long_description': '# Aserto API client\n\nHigh-level client interface to Aserto\'s APIs.\n\nAt the moment this only supports interacting with Aserto\'s [Authorizer service](https://docs.aserto.com/docs/authorizer-guide/overview).\n\n## Installation\n\n### Using Pip\n\n```sh\npip install aserto\n```\n\n### Using Poetry\n\n```sh\npoetry add aserto\n```\n\n## Usage\n\n```py\nfrom aserto.client import AuthorizerOptions, Identity\nfrom aserto.client.api.authorizer import AuthorizerClient\n\n\nclient = AuthorizerClient(\n    identity=Identity(type="NONE"),\n    options=AuthorizerOptions(\n        api_key=ASERTO_API_KEY,\n        tenant_id=ASERTO_TENANT_ID,\n        service_type="gRPC",\n    ),\n)\n\nresult = await client.decision_tree(\n    decisions=["visible", "enabled", "allowed"],\n    policy_instance_name=ASERTO_POLICY_INSTANCE_NAME,\n    policy_instance_label=ASERTO_POLICY_INSTANCE_LABEL,\n    policy_path_root=ASERTO_POLICY_PATH_ROOT,\n    policy_path_separator="DOT",\n)\n\nassert result == {\n    "GET.your.policy.path": {\n        "visible": True,\n        "enabled": True,\n        "allowed": False,\n    },\n}\n```\n\n## Directory\n\nThe Directory APIs can be used to get or set object instances and relation instances. They can also be used to check whether a user has a permission or relation on an object instance.\n\n### Directory Client\n\nYou can initialize a directory client as follows:\n\n```py\nfrom aserto.client.directory import Directory\n\nds = Directory.connect(api_key="my_api_key", tenant_id="1234", address="localhost:9292")\n```\n\n- `address`: hostname:port of directory service (_required_)\n- `api_key`: API key for directory service (_required_ if using hosted directory)\n- `tenant_id`: Aserto tenant ID (_required_ if using hosted directory)\n- `cert`: Path to the grpc service certificate when connecting to local topaz instance.\n\n#### \'get_object\' function\n\nGet a directory object instance with the type and the key.\n\n```py\nuser = ds.get_object(type="user", key="euang@acmecorp.com")\n```\n\n#### \'get_objects\' function\n\nGet object instances with an object type type and page size.\n\n```py\nfrom aserto.client.directory import PaginationRequest\n\nusers = ds.get_objects(object_type="user", page=PaginationRequest(size=10))\n```\n\n#### \'set_object\' function\n\nCreate an object instance with the specified fields. For example:\n\n```py\nfrom google.protobuf.json_format import ParseDict\nfrom google.protobuf.struct_pb2 import Struct\n\nproperties = ParseDict({"displayName": "test object"}, Struct())\n\nuser = ds.set_object(object={\n    "type": "user",\n    "key": "test-object",\n    "properties": properties,\n})\n```\n\n#### \'delete_object\' function\n\nDelete an object instance using its type and key:\n\n```py\nds.delete_object(type="user", key="test-object")\n```\n\n## License\n\nThis project is licensed under the MIT license. See the [LICENSE](https://github.com/aserto-dev/aserto-python/blob/main/LICENSE) file for more info.\n',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': 'authereal',
    'maintainer_email': 'authereal@aserto.com',
    'url': 'https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
