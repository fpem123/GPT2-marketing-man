# GPT2-marketing-man

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/GPT2-marketing-man?branch=main)

This project generate marketing man style text using GPT-2 model.

model: https://huggingface.co/laxya007/gpt2_Marketingman

## how to use

* First, Choose wanna type!

* Second, Fill text in "text"! This will be base of marketing man style text!

* And then, Fill number in "samples"! The app generates sample number of text!

* If you select 'long' type, be fill number in "length"! The app generates text of that size

### ** Post parameter **

#### *** /GPT2-marketing-man/short ***

* text: The base text to generate a word.

* samples: How many generate word?

#### *** /GPT2-marketing-man/long ***

* text: The base text to generate marketing man style text.

* samples: How many generate text?
  
* length: Size of text.

### ** With CLI **


#### /GPT2-marketing-man/short

curl -X POST "https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/GPT2-marketing-man/short" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=Hello " -F "samples=3"

#### /GPT2-marketing-man/long

curl -X POST "https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/GPT2-marketing-man/long" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=Hello, " -F "samples=3" -F "length=50"

### ** With swagger **

Use API page: https://ainize.ai/fpem123/GPT2-marketing-man?branch=main

### ** With demo **

Use demo page: https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/

--
