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


def request_handling():
    while True:
        requestBatch = []

        while not (len(requestBatch) >= BATCH_SIZE):
            try:
                requestBatch.append(requestQueue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in requestBatch:
                if len(requests['input']) == 2:
                    requests['output'] = run_short(requests['input'][0], requests['input'][1])
                elif len(requests['input']) == 3:
                    requests['output'] = run_long(requests['input'][0], requests['input'][1], requests['input'][2])

threading.Thread(target=request_handling).start()

def run_short(base, samples):
    try:
        base = base.strip()
        inputIds = tokenizer.encode(base, return_tensors='pt')
        inputIds = inputIds.to(device)

        nextTokenLogits = model(inputIds).logits[:, -1, :]

        filteredNextTokenLogits = top_k_top_p_filtering(nextTokenLogits, top_k=50, top_p=1.0)

        probs = F.softmax(filteredNextTokenLogits, dim=1)
        nextToken = torch.multinomial(probs, num_samples=samples)

        result = {}

        for idx, token in enumerate(nextToken.tolist()[0]):
            result[idx] = tokenizer.decode(token)

        return result

    except Exception:
        return jsonify({'error': Exception}), 500

def run_long(base, samples, length):
    try:
        base = base.strip()
        inputIds = tokenizer.encode(base, return_tensors='pt')
        inputIds = inputIds.to(device)

        minLength = len(inputIds.tolist()[0])
        length += minLength

        samplesOutputs = model.generate(inputIds, pad_token_id=50256,
                                        do_sample=True,
                                        max_length=length,
                                        min_length=length,
                                        top_k=40,
                                        num_return_sequences=samples)

        result = dict()

        for idx, token in enumerate(samplesOutputs):
            result[idx] = tokenizer.decode(samplesOutputs.tolist()[minLength:], skip_special_tokens=True)

        return result

    except Exception:
        return jsonify({'error': Exception}), 500


@app.route('/GPT2-marketing-man/<tpyes>', methods=['POST'])
def run_GPT2(type):
    if type != 'short' and type != 'long':
        return jsonify({'error': 'The wrong address.'}), 400

    if requestQueue.qsize() >BATCH_SIZE:
        return jsonify({'error': 'Too Many Requests'}), 429

    try:
        args = []
        text = request.form['base']
        samples = int(request.form['samples'])

        args.append(text)
        args.append(samples)

        if type == 'long':
            length = int(request.form['length'])
            args.append(length)

    except Exception:
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
