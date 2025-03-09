# Use the official MySQL image
FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=esd-clinic-db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Copy custom MySQL configuration
COPY my.cnf /etc/mysql/conf.d/my.cnf

# Expose MySQL default port
EXPOSE 3306

# Start MySQL service
CMD ["mysqld"]
