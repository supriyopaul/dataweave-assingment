import argparse
import subprocess
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dataweave.models import Base
from dotenv import load_dotenv

from dataweave.app import app, process_file
from dataweave.consumer import RabbitMQConsumer

load_dotenv()

def runserver(args):
    uvicorn_command = [
        sys.executable, '-m', 'uvicorn',
        'dataweave:app',
        '--host', '0.0.0.0',
        '--port', str(args.port),
        '--workers', str(args.workers)
    ]
    subprocess.run(uvicorn_command)

def runconsumer(args):
    rabbit_mq_host = args.rabbit_mq.split(':')[0]  # Assuming format 'host:port'

    consumer = RabbitMQConsumer(rabbit_mq_host, args.queue)
    consumer.connect()
    consumer.start_consuming()

def ingest(args):
    print(f"Ingesting from file {args.fpath} to RabbitMQ at {args.rabbit_mq} and queue '{args.queue}'.")
    total_records = process_file(args.fpath, args.queue)
    if total_records is not None:
        print(f"File ingested successfully with {total_records} records.")
    else:
        print("Failed to ingest file.")

def create_database(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print(f"Database created at {db_url}")

def delete_database(db_url):
    engine = create_engine(db_url)
    try:
        Base.metadata.drop_all(engine)
        print(f"Database at {db_url} deleted.")
    except OperationalError as e:
        print(f"Error deleting database: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for managing server and RabbitMQ tasks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(help='commands')

    # Runserver command
    runserver_parser = subparsers.add_parser('runserver', help='Run the server')
    default_workers = os.getenv('WORKERS', 1)
    default_port = os.getenv('PORT', 8000)
    runserver_parser.add_argument('--workers', type=int, default=default_workers, help=f'Number of workers (default: {default_workers})')
    runserver_parser.add_argument('--port', type=int, default=default_port, help=f'Port to run the server on (default: {default_port})')
    runserver_parser.set_defaults(func=runserver)

    # Runconsumer command
    runconsumer_parser = subparsers.add_parser('runconsumer', help='Run the RabbitMQ consumer')
    default_rabbit_mq = os.getenv('RABBIT_MQ', 'localhost:15672')
    default_queue = os.getenv('QUEUE', 'products')
    runconsumer_parser.add_argument('--rabbit-mq', default=default_rabbit_mq, help=f"RabbitMQ server address (default: '{default_rabbit_mq}')")
    runconsumer_parser.add_argument('--queue', default=default_queue, help=f"Queue name (default: '{default_queue}')")
    runconsumer_parser.set_defaults(func=runconsumer)

    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest data')
    ingest_parser.add_argument('--fpath', required=True, help='File path to ingest data from')
    ingest_parser.add_argument('--rabbit-mq', default=default_rabbit_mq, help=f"RabbitMQ server address (default: '{default_rabbit_mq}')")
    ingest_parser.add_argument('--queue', default=default_queue, help=f"Queue name (default: '{default_queue}')")
    ingest_parser.set_defaults(func=ingest)

    # Create-db command
    default_db_url = os.getenv('DB_URL', 'sqlite:///products.db')
    create_db_parser = subparsers.add_parser('create-db', help='Create the database')
    create_db_parser.add_argument('--db-url', default=default_db_url, help=f'Database URL (default: "{default_db_url}")')
    create_db_parser.set_defaults(func=lambda args: create_database(args.db_url))

    # Delete-db command
    delete_db_parser = subparsers.add_parser('delete-db', help='Delete the database')
    delete_db_parser.add_argument('--db-url', default=default_db_url, help=f'Database URL (default: "{default_db_url}")')
    delete_db_parser.set_defaults(func=lambda args: delete_database(args.db_url))

    # Parse arguments
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
