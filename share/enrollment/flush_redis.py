import redis

redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def clear_redis_data():
    try:
        # Connect to the Redis server
        r = redis.Redis(connection_pool=redis_connection_pool)

        # Flush all data in the current database
        r.flushdb()

        print("Redis data cleared successfully.")

    except Exception as e:
        print(f"Error: {e}")

clear_redis_data()