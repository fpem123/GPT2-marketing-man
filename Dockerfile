FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-devel

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget

RUN pip install --upgrade pip
RUN pip install transformers==4.4.1
RUN pip install flask==1.1.2
RUN pip install waitress==1.4.4

RUN mkdir -p /app
WORKDIR /app
COPY . .

EXPOSE 80

CMD ['python3', 'app.py']
