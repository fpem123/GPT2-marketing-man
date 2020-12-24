FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
EXPOSE 80
COPY . .

CMD python3 app.py
