import redis
import json

redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=redis_connection_pool)

def addSubscription(section_id, user_id, callback_url, email):
    redis_key = f"subscriptions:{user_id}"
    
    # Store a JSON-encoded string as a single element in the set
    subscription_data = {'section_id': section_id, 'callback_url': callback_url, "email": email}
    subscription_data_str = json.dumps(subscription_data)
    r.sadd(redis_key, subscription_data_str)

def getAllSubscriptions(user_id):
    redis_key = f"subscriptions:{user_id}"
    subscriptions_set = r.smembers(redis_key)

    return [json.loads(member) for member in subscriptions_set]

def deleteSubscription(user_id, section_id):
    redis_key = f"subscriptions:{user_id}"
    # Iterate over the set and remove items with the specified section_id
    for member in r.smembers(redis_key):
        subscription_data = json.loads(member)
        if subscription_data.get('section_id') == section_id:
            r.srem(redis_key, member)

def getSubscription(user_id, section_id):
        redis_key = f"subscriptions:{user_id}"
        for member in r.smembers(redis_key):
            subscription_data = json.loads(member)
            if subscription_data.get('section_id') == section_id:
                return subscription_data
        return None


def printAllRedisData():
    r = redis.Redis()

    # Get all keys in the Redis database
    all_keys = r.keys('*')

    # Iterate over keys and print values
    for key in all_keys:
        key_str = key.decode('utf-8')  # Convert bytes to string
        value_type = r.type(key_str)

        print(f"Key: {key_str}, Type: {value_type.decode('utf-8')}")

        # Print values based on their type
        if value_type == b'string':
            print(f"  Value: {r.get(key_str).decode('utf-8')}")
        elif value_type == b'list':
            print(f"  Values: {r.lrange(key_str, 0, -1)}")
        elif value_type == b'set':
            print(f"  Members: {r.smembers(key_str)}")
        elif value_type == b'zset':
            print(f"  Members with Scores: {r.zrange(key_str, 0, -1, withscores=True)}")
        elif value_type == b'hash':
            print(f"  Field-Value Pairs: {r.hgetall(key_str)}")