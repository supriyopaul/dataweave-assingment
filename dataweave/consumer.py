import json

import pika
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dataweave.models import ProductModel, MetaInfoModel, engine


class RabbitMQConsumer:
    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def transform_and_store_message(self, session, message):
        meta_info_data = eval(message['meta_info'])
        product_data = {
            'reference_product_id': meta_info_data['reference_product_id'],
            'available_price': float(message['available_price']),
            'in_stock': True if message['stock'] == 'In Stock' else False,
            'source': message['source']
        }
        product = ProductModel(**product_data)

        # Serialize complex types to JSON strings
        for key in ['bundle_variant_field_mapping', 'bundle_definition', 'fulfilment_modes']:
            if key in meta_info_data:
                meta_info_data[key] = json.dumps(meta_info_data[key])

        meta_info_data['product'] = product
        meta_info = MetaInfoModel(**meta_info_data)

        session.add(product)
        session.add(meta_info)
        session.commit()

    def on_message(self, channel, method_frame, header_frame, body):
        session = sessionmaker(bind=engine)()
        try:
            message = json.loads(body)
            print(f"Received message: {message}")

            # Transform and store the message
            self.transform_and_store_message(session, message)

            # Acknowledge the message
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            #TODO: Handle separately (sqlite3.IntegrityError) UNIQUE constraint failed: products.index
            print(f"Error processing message: {e}")
        finally:
            session.close()

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=False)
        print(f"Starting consumer on queue '{self.queue_name}'. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()
            print("Consumer stopped.")

if __name__ == '__main__':
    rabbit_mq = 'localhost:15672'
    queue = 'products'
    rabbit_mq_host = rabbit_mq.split(':')[0] 
    consumer = RabbitMQConsumer(rabbit_mq_host, queue)
    consumer.connect()
    consumer.start_consuming()
