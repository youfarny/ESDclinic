# ESDclinic
we will solve all your problems and give you MC


# TO RUN:

On Machine 1:
- run docker-compose on "Machine 1 - Atomics". This will start all atomic services.
- run docker-compose on mysql, rabbitmq, and kong-postgresql
- load dummy data using db.sql

On Machine 2:
- run docker-compose on "Machine 2 - Composites + Kong". This will start the composite microservice ProcessAppointment and Kong API Gateway.
- run "npm run dev" on the vue app

# Logins:

mysql: 3306
root
ESD213password!

rabbitmq: 5672/15672
admin
ESD213password!

grafana: 3000
admin
ESD213password!

