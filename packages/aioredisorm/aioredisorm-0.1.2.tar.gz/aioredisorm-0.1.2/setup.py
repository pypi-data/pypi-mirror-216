# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioredisorm']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.1,<3.0.0', 'asyncio>=3.4.3,<4.0.0']

setup_kwargs = {
    'name': 'aioredisorm',
    'version': '0.1.2',
    'description': 'A Python class for interacting with Redis using asyncio and aioredis.',
    'long_description': '## AIORedisORM\n\nA Python class for interacting with Redis using asyncio and aioredis.\n\n### Installation\n\nYou can install AIORedisORM using pip:\n\n```\npip install aioredisorm\n```\n\n### Example Usage\n\nHere is an example that demonstrates the usage of the AIORedisORM class:\n\n```python\nimport asyncio\nfrom aioredisorm import AIORedisORM\n\nasync def main():\n    redis_client = AIORedisORM(key_prefix=\'my_prefix\')\n    await redis_client.connect()\n\n    # Set a value\n    await redis_client.set_value(\'my_key\', \'my_value\', ex=12)\n\n    # Get a value\n    result = await redis_client.get_value(\'my_key\')\n    print(result)  # Output: b\'my_value\'\n\n    # Set a hash\n    await redis_client.set_hash(\'my_hash\', {\'key1\': \'value1\', \'key2\': \'value2\', \'key3\': 13})\n\n    # Set a hash with expiration\n    await redis_client.set_hash(\'my_hash\', {\'key1\': \'value1\', \'key2\': \'value2\', \'key3\': 13}, ex=5)\n\n    # Get a hash\n    hash_result = await redis_client.get_hash(\'my_hash\')\n    print(hash_result)  # Output: {b\'key1\': b\'value1\', b\'key2\': b\'value2\', b\'key3\': b\'123\'}\n\n    await asyncio.sleep(5)  # Wait for the expiration to pass\n\n    hash_result = await redis_client.get_hash(\'my_hash\')\n    print(hash_result)  # Output: {}\n\n    # Close the connection\n    await redis_client.close()\n\n    # Decode the bytes to a string if needed\n    result = result.decode(\'utf-8\')\n    print(result)  # Output: \'my_value\'\n\n    # Set a set\n    await redis_client.set_set(\'my_set\', \'value1\', \'value2\', \'value3\')\n\n    # Get a set\n    set_result = await redis_client.get_set(\'my_set\')\n    print("set_result", set_result)  # Output: {b\'value1\', b\'value2\', b\'value3\'}\n\n    # Transaction example\n    commands = [\n        (\'set\', \'key1\', \'value1\'),\n        (\'set\', \'key2\', \'value2\')\n    ]\n    results = await redis_client.execute_transaction(commands)\n    print(results)  # Output: [(True, True)]\n\n    # Set a list\n    await redis_client.set_list(\'my_list\', \'value1\', \'value2\', \'value3\')\n\n    # Get a list\n    list_result = await redis_client.get_list(\'my_list\')\n    print(list_result)  # Output: [b\'value1\', b\'value2\', b\'value3\']\n\n    # Get the expiration time of a key\n    ttl, pttl = await redis_client.get_key_expiration(\'key1\')\n    print(f"TTL of \'my_key\': {ttl} seconds")\n    print(f"PTTL of \'my_key\': {pttl} milliseconds")\n\n    # Close the connection\n    await redis_client.close()\n\n# Run the async example\nasyncio.run(main())\n```\n\nMake sure to import the AIORedisORM class and replace \'my_prefix\' with your desired key prefix.\n',
    'author': 'fadedreams7',
    'author_email': 'fadedreams7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
