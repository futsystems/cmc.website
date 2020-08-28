# -*- coding: utf-8 -*-

import pika, logging
import json

logger = logging.getLogger(__name__)

class EventBublisher(object):
    def __init__(self, eventbus):
        #self._url='amqp://user:user@test.marvelsystem.net'
        self._url = 'amqp://%s:%s@%s' % (eventbus.user_name, eventbus.password, eventbus.host)
        self._broker_name = 'marvel_event_bus'
        self._subscription_client_name='cmc'
        params = pika.URLParameters(self._url)
        params.socket_timeout = 5

        self._connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
        self._channel = self._connection.channel()  # start a channel
        #self._channel.exchange_declare(exchange=self._broker_name, exchange_type='direct')
        self._channel.queue_declare(queue=self._subscription_client_name)  # Declare a queue

    def send_message(self, event):
        # send a message
        print ('send event:%s body:%s' % (event.name, event.body))
        self._channel.basic_publish(exchange=self._broker_name, routing_key=event.name, body=json.dumps(event.body))
        self._channel.close()


#rabbitmq_bus = EventBublisher()


if __name__ == "__main__":
    event_publisher = EventBublisher()
    from gateway_config_update import CMCGatewayConfigUpdate
    ev = CMCGatewayConfigUpdate('gw.api','Production')
    s= event_publisher.send_message(ev)
    print s
