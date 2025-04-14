# Use minimal possible env
FROM alpine:latest

# Set the working directory
WORKDIR /db

# Install mysql
RUN apk add --update --no-cache mysql mysql-client

# Set custom config
COPY my.cnf /etc/mysql/my.cnf
    
COPY startup.sh .

# Make port 3306 available to the world outside this container
EXPOSE 3306

# Run mysql server when the container launches
ENTRYPOINT ["sh"]
CMD ["startup.sh"]
