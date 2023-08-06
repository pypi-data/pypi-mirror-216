import asyncio
import aioredis

class AIORedisORM:
    def __init__(self, host='localhost', port=6379, db=0, username=None, password=None, key_prefix=''):
        self.client = None
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.key_prefix = key_prefix

    async def connect(self):
        if self.username and self.password:
            url = f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
        else:
            url = f"redis://{self.host}:{self.port}/{self.db}"
        self.client = await aioredis.from_url(url)

    def add_prefix(self, key):
        if self.key_prefix:
            return f"{self.key_prefix}:{key}"
        return key

    async def close(self):
        if self.client:
            await self.client.close()

    async def set_value(self, key, value, ex=None):
        await self.client.set(key, value)
        if ex is not None:
            await self.client.expire(key, ex)

    async def get_value(self, key):
        return await self.client.get(key)

    async def set_hash(self, key, mapping, ex=None):
        await self.client.hset(key, mapping=mapping)
        if ex is not None:
            await self.client.expire(key, ex)

    async def get_hash(self, key):
        return await self.client.hgetall(key)

    async def set_set(self, key, *values, ex=None):
        await self.client.sadd(key, *values)
        if ex is not None:
            await self.client.expire(key, ex)

    async def get_set(self, key):
        return await self.client.smembers(key)

    async def set_list(self, key, *values, ex=None):
        await self.client.rpush(key, *values)
        if ex is not None:
            await self.client.expire(key, ex)

    async def get_list(self, key):
        return await self.client.lrange(key, 0, -1)

    async def execute_transaction(self, commands):
        async with self.client.pipeline(transaction=True) as pipe:
            for command in commands:
                getattr(pipe, command[0])(*command[1:])
            results = await pipe.execute()
            return results

    async def get_key_expiration(self, key):
        ttl = await self.client.ttl(key)
        pttl = await self.client.pttl(key)
        return ttl, pttl

    async def delete_key(self, key):
        await self.client.delete(key)

# Example usage
async def main():
    redis_client = AIORedisORM(key_prefix='my_prefix')
    await redis_client.connect()

    # Set a value
    await redis_client.set_value('my_key', 'my_value', ex=12)

    # Get a value
    result = await redis_client.get_value('my_key')
    print(result)  # Output: b'my_value'

    await redis_client.set_hash('my_hash', {'key1': 'value1', 'key2': 'value2', 'key3': 13})

    # Set a hash with expiration
    await redis_client.set_hash('my_hash', {'key1': 'value1', 'key2': 'value2', 'key3': 13}, ex=60)

    # Get a hash
    hash_result = await redis_client.get_hash('my_hash')
    print(hash_result)  # Output: {b'key1': b'value1', b'key2': b'value2', b'key3': b'123'}

    await asyncio.sleep(5)  # Wait for the expiration to pass

    hash_result = await redis_client.get_hash('my_hash')
    print(hash_result)  # Output: {}

    await redis_client.close()
    # You can decode the bytes to a string if needed
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

    await redis_client.close()

# Run the async example
asyncio.run(main())


