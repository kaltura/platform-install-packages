#!/bin/sh

FG_CYAN=36
CYAN="\033[${DULL};${FG_CYAN}m"
NORMAL="\033[m"

set -e
/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management
wget  http://localhost:15672/cli/rabbitmqadmin -O /usr/local/bin/rabbitmqadmin
chmod +x /usr/local/bin/rabbitmqadmin
echo -e "${CYAN}mRabbitMQ Admin username:${NORMAL}"
read -e RABBIT_USER
echo -e "${CYAN}mRabbitMQ Admin passwd:${NORMAL}"
read -s RABBIT_PASSWD
rabbitmqctl add_user $RABBIT_USER "$RABBIT_PASSWD"
rabbitmqctl set_user_tags $RABBIT_USER administrator
rabbitmqctl set_permissions -p / rabbit ".*" ".*" ".*"
rabbitmqctl -n rabbit stop_app
rabbitmqctl -n rabbit start_app

set +e
# in older versions, this is the expected syntax
rabbitmqctl set_policy ha-all ".*"  '{"ha-mode":"all","ha-sync-mode":"automatic"}'  0 > /dev/null 2>&1
# if this failed, use this syntax instead:
if [ $? -ne 0 ];then
        rabbitmqctl set_policy --priority 0 --apply-to all ha-all ".*"  '{"ha-mode":"all","ha-sync-mode":"automatic"}'
fi
set -e
rabbitmqadmin declare exchange name=kaltura_exchange type=fanout durable=true
rabbitmqadmin declare queue name=`hostname` durable=true 'arguments={"x-message-ttl":86400000}'

