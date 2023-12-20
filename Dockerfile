
FROM python:3.9-slim


WORKDIR /usr/src/app
COPY . .
RUN pip install .


EXPOSE 8000
ENV PORT=8000
ENV RABBIT_MQ=rabbitmq:15672
CMD ["dataweave", "runserver"]
