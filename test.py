from transformers import AutoTokenizer, AutoModelForCausalLM
import time

tokenizer = AutoTokenizer.from_pretrained("laxya007/gpt2_Marketingman")
model = AutoModelForCausalLM.from_pretrained("laxya007/gpt2_Marketingman")

prompt = "Hello, customer. My name is kent. In case I"

input_ids = tokenizer.encode(prompt, return_tensors='pt')
length = 200
length += len(input_ids.tolist()[0])
print(input_ids)
print(len(input_ids.tolist()[0]))
print(length)
print("-----------------------")

s = time.time()
sample_outputs = model.generate(input_ids, pad_token_id=50256,
                                do_sample=True,
                                max_length=length,
                                min_length=int(length / 1.5),
                                top_k=40,
                                num_return_sequences=1)
print("{}초 경과 -----------------------".format(time.time()-s))

for i, sample_output in enumerate(sample_outputs):
    print("{} >> {}".format(i+1, tokenizer.decode(sample_output.tolist(), skip_special_tokens=True)))
    print("**************************")