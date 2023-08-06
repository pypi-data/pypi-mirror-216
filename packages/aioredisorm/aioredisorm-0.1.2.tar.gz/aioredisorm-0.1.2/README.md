## AIORedisORM

A Python class for interacting with Redis using asyncio and aioredis.

### Installation

You can install AIORedisORM using pip:

```
pip install aioredisorm
```

### Example Usage

Here is an example that demonstrates the usage of the AIORedisORM class:

```python
import asyncio
from aioredisorm import AIORedisORM

async def main():
    redis_client = AIORedisORM(key_prefix='my_prefix')
    await redis_client.connect()

    # Set a value
    await redis_client.set_value('my_key', 'my_value', ex=12)

    # Get a value
    result = await redis_client.get_value('my_key')
    print(result)  # Output: b'my_value'

    # Set a hash
    await redis_client.set_hash('my_hash', {'key1': 'value1', 'key2': 'value2', 'key3': 13})

    # Set a hash with expiration
    await redis_client.set_hash('my_hash', {'key1': 'value1', 'key2': 'value2', 'key3': 13}, ex=5)

    # Get a hash
    hash_result = await redis_client.get_hash('my_hash')
    print(hash_result)  # Output: {b'key1': b'value1', b'key2': b'value2', b'key3': b'123'}

    await asyncio.sleep(5)  # Wait for the expiration to pass

    hash_result = await redis_client.get_hash('my_hash')
    print(hash_result)  # Output: {}

    # Close the connection
    await redis_client.close()

    # Decode the bytes to a string if needed
    result = result.decode('utf-8')
    print(result)  # Output: 'my_value'

    # Set a set
    await redis_client.set_set('my_set', 'value1', 'value2', 'value3')

    # Get a set
    set_result = await redis_client.get_set('my_set')
    print("set_result", set_result)  # Output: {b'value1', b'value2', b'value3'}

    # Transaction example
    commands = [
        ('set', 'key1', 'value1'),
        ('set', 'key2', 'value2')
    ]
    results = await redis_client.execute_transaction(commands)
    print(results)  # Output: [(True, True)]

    # Set a list
    await redis_client.set_list('my_list', 'value1', 'value2', 'value3')

    # Get a list
    list_result = await redis_client.get_list('my_list')
    print(list_result)  # Output: [b'value1', b'value2', b'value3']

    # Get the expiration time of a key
    ttl, pttl = await redis_client.get_key_expiration('key1')
    print(f"TTL of 'my_key': {ttl} seconds")
    print(f"PTTL of 'my_key': {pttl} milliseconds")

    # Close the connection
    await redis_client.close()

# Run the async example
asyncio.run(main())
```

Make sure to import the AIORedisORM class and replace 'my_prefix' with your desired key prefix.
