
FROM redis:latest
# Copy your custom Redis config
COPY ./redis.conf /usr/local/etc/redis/redis.conf

# Start Redis server with custom config
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]