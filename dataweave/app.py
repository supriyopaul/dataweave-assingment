import json
import os

from dotenv import load_dotenv
import pika
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from sqlalchemy.sql import func, case
from sqlalchemy.orm import sessionmaker
import uvicorn

from dataweave.models import engine, ProductModel, MetaInfoModel

load_dotenv()
Q_HOST = os.getenv('Q_HOST', 'localhost')
Q_NAME = os.getenv('Q_NAME', 'products')

app = FastAPI()
Session = sessionmaker(bind=engine)
session = Session()

def send_to_rabbitmq(queue_name, message):
    #TODO: Use TLS
    #FIXME: Create a persistent connection
    connection = pika.BlockingConnection(pika.ConnectionParameters())
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()

def process_file(file_path, queue_name):
    total_records = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            buffer = ""
            for line in file:
                buffer += line.strip()
                if buffer.endswith('}'):
                    record = json.loads(buffer)
                    send_to_rabbitmq(queue_name, record)
                    total_records += 1
                    buffer = ""
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"Error processing file: {str(e)}")
        return None
    return total_records

@app.post("/ingest/")
async def ingest(file: UploadFile = File(...)):
    if file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JSON file.")

    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    total_records = process_file(file_location, Q_NAME)
    if total_records is None:
        raise HTTPException(status_code=500, detail="Error processing file")

    os.remove(file_location)  # Clean up the temporary file
    return {"detail": f"File ingested successfully with {total_records} records."}

@app.get("/products")
def get_products(limit: int = Query(default=20, ge=1), offset: int = Query(default=0, ge=0)):
    session = Session(bind=engine)
    products_with_meta = (
        session.query(ProductModel, MetaInfoModel)
        .join(MetaInfoModel, ProductModel.reference_product_id == MetaInfoModel.product_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    session.close()

    # Format the response to include details from both ProductModel and MetaInfoModel
    result = []
    for product, meta_info in products_with_meta:
        product_dict = {
            'reference_product_id': product.reference_product_id,
            'available_price': str(product.available_price),
            'in_stock': product.in_stock,
            'source': product.source,
            'meta_info': {**meta_info.__dict__}
        }
        # Exclude internal SQLAlchemy attributes
        product_dict['meta_info'].pop('_sa_instance_state', None)
        result.append(product_dict)

    return result

@app.get("/score/")
def get_overall_availability_score():
    session = Session(bind=engine)
    # Calculate the overall availability score
    total_products = session.query(func.count(ProductModel.reference_product_id)).scalar()
    in_stock_products = session.query(func.count(ProductModel.reference_product_id))\
                               .filter(ProductModel.in_stock == True).scalar()
    session.close()

    # Calculate the score
    availability_score = in_stock_products / total_products if total_products > 0 else 0

    return {"overall_availability_score": availability_score}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
