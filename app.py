from transformers import AutoModelWithLMHead, AutoTokenizer, top_k_top_p_filtering
from flask import Flask, request, Response, jsonify
import torch
from torch.nn import functional as F

from queue import Queue, Empty
import threading
import time

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("laxya007/gpt2_Marketingman")
model = AutoModelWithLMHead.from_pretrained("laxya007/gpt2_Marketingman", return_dict=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

request_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1


def handle_requests_by_batch():
    while True:
        request_batch = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(request_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:
                if len(requests['input']) == 2:
                    requests["output"] = run_short(requests['input'][0], requests['input'][1])
                elif len(requests['input']) == 3:
                    requests["output"] = run_long(requests['input'][0], requests['input'][1], requests['input'][2])


threading.Thread(target=handle_requests_by_batch).start()


def run_short(text, samples):
    try:
        print('Start short GPT2')

        input_ids = tokenizer.encode(text, return_tensors='pt')

        input_ids = input_ids.to(device)

        next_token_logits = model(input_ids).logits[:, -1, :]

        filtered_next_token_logits = top_k_top_p_filtering(next_token_logits, top_k=50, top_p=1.0)

        probs = F.softmax(filtered_next_token_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=samples)

        result = dict()

        for idx, token in enumerate(next_token.tolist()[0]):
            result[idx] = tokenizer.decode(token)

        print('Done')

        return result

    except Exception as e:
        print('Oh no!', e)
        return jsonify({'error': e}), 500


def run_long(text, samples, length):
    try:
        print('Start long GPT2')

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
            result[idx] = tokenizer.decode(samples_outputs.tolist()[min_length:], skip_special_tokens=True)

        print('Done')

        return result

    except Exception as e:
        print('Oh no!', e)
        return jsonify({'error': e}), 500


@app.route('/GPT2-marketing-man/<types>', methods=['POST'])
def generate(types):
    if types != 'short' and types != 'long':
        return jsonify({'error': 'The wrong address.'}), 400

    if request_queue.qsize() > BATCH_SIZE:
        return jsonify({'error': 'Too Many Requests'}), 429

    try:
        args = []

        text = request.form['text']
        samples = int(request.form['samples'])

        args.append(text)
        args.append(samples)

        if types == 'long':
            length = int(request.form['length'])
            args.append(length)

    except Exception as e:
        return jsonify({'message': 'Invalid request'}), 500

    req = {'input': args}
    request_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])


@app.route('/Debug_queue_clear')
def queue_clear():
    with request_queue.mutex:
        request_queue.queue.clear()

    return "Clear", 200


@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


@app.route('/')
def main():
    return "200 OK", 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')
