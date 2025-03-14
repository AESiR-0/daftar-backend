from redis import Redis

r = Redis(
    host='redis-16927.c99.us-east-1-4.ec2.redns.redis-cloud.com',
    port=16927,
    decode_responses=True,
    username="default",
    password="4dVEpmNXAQUtu6mZS61opGvqSX4l1JdO",
)

success = r.set('foo', 'bar')

result = r.get('foo')
print(result)