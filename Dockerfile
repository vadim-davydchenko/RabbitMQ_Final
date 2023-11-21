FROM rabbitmq:3.12.8-management
ADD /rabbitmq/definitions.json /etc/rabbitmq
ADD /rabbitmq/rabbitmq.conf /etc/rabbitmq
