from transformers import AutoModelWithLMHead, AutoTokenizer, top_k_top_p_filtering
from flask import Flask, request, Response, jsonify
import torch
from torch.nn import functional as F

from queue import Queue, Empty
import threading
import time

app = Flask(__name__)

requestQueue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

tokenizer = AutoTokenizer.from_pretrained("laxya007/gpt2_Marketingman")
model = AutoModelWithLMHead.from_pretrained("laxya007/gpt2_Marketingman", return_dict=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)


def handle_requests_by_batch():
    try:
        while True:
            request_batch = []

            while not (len(request_batch) >= BATCH_SIZE):
                try:
                    request_batch.append(requestQueue.get(timeout=CHECK_INTERVAL))
                except Empty:
                    continue

            batch_outputs = []

            for request in request_batch:
                if len(request['input']) == 2:
                    batch_outputs.append(run_short(request['input'][0], request['input'][1]))
                elif len(request['input']) == 3:
                    batch_outputs.append(run_long(request['input'][0], request['input'][1], request['input'][2]))

            for request, output in zip(request_batch, batch_outputs):
                request["output"] = output

    except Exception as e:
        while not requestQueue.empty():
            requestQueue.get()
        return jsonify({'error': 'request_handling error'}), 500


threading.Thread(target=handle_requests_by_batch).start()


def run_short(text, samples):
    try:
        text = text.strip()
        input_ids = tokenizer.encode(text, return_tensors='pt')
        input_ids = input_ids.to(device)

        next_token_logits = model(input_ids).logits[:, -1, :]

        filtered_next_token_logits = top_k_top_p_filtering(next_token_logits, top_k=50, top_p=1.0)

        probs = F.softmax(filtered_next_token_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=samples)

        result = {}

        for idx, token in enumerate(next_token.tolist()[0]):
            result[idx] = tokenizer.decode(token)

        return result

    except Exception as e:
        return jsonify({'error': e}), 500


def run_long(text, samples, length):
    try:
        text = text.strip()
        input_ids = tokenizer.encode(text, return_tensors='pt')
        input_ids = input_ids.to(device)

        min_length = len(input_ids.tolist()[0])
        length += min_length

        samples_outputs = model.generate(input_ids, pad_token_id=50256,
                                        do_sample=True,
                                        max_length=length,
                                        min_length=length,
                                        top_k=40,
                                        num_return_sequences=samples)

        result = dict()

        for idx, token in enumerate(samples_outputs):
            output = tokenizer.decode(samples_outputs.tolist()[min_length:], skip_special_tokens=True)
            result[idx] = output

        return result

    except Exception as e:
        return jsonify({'error': e}), 500


@app.route('/GPT2-marketing-man/<types>', methods=['POST'])
def generate(type):
    if type != 'short' and type != 'long':
        return jsonify({'error': 'The wrong address.'}), 400

    if requestQueue.qsize() > BATCH_SIZE:
        return jsonify({'error': 'Too Many Requests'}), 429

    try:
        args = []

        text = request.form['text']
        samples = int(request.form['samples'])

        args.append(text)
        args.append(samples)

        if type == 'long':
            length = int(request.form['length'])
            args.append(length)

    except Exception as e:
        return jsonify({'message': 'Invalid request, need args'}), 500

    req = {'input': args}
    requestQueue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])


@app.route('/healthz', methods=["GET"])
def health_check():
    return "health", 200


@app.route('/')
def main():
    return "Use API", 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')
