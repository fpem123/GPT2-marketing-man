# GPT2-marketing-man

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/GPT2-marketing-man?branch=main)

This project generate marketing man style text using GPT-2 model.

model: [laxya007/gpt2_Marketingman](https://huggingface.co/laxya007/gpt2_Marketingman)

## how to use

* First, Choose wanna type!

* Second, Fill text in "text"! This will be base of marketing man style text!

* And then, Fill number in "num_samples"! The app generates sample number of text!

* If you select 'long' type, be fill number in "length"! The app generates text of that size


### ** Post parameter **

#### /infer/GPT2-marketing-man

    text: The base text to generate marketing man style text.
    num_samples: How many generate text?
    length: Size of text.

### ** With CLI **

#### /infer/GPT2-marketing-man

Input example

    curl -X POST "https://feature-add-torch-serve-gpt-2-server-gkswjdzz.endpoint.ainize.ai/infer/GPT2-marketing-man" -H "accept: */*" -H "Content-Type: application/json" -d "{\"text\":\"Hi There is a Test.\",\"num_samples\":5,\"length\":20}"


Output example

    {
        "0": "Hi There is a Test. What Can I Do? The first thing you should do is to know that there is a problem!",
        "1": "Hi There is a Test. It Is a Good Idea…\nTest your relationship knowledge with a book test. This is a great",
        "2": "Hi There is a Test. You must answer the quiz correctly to proceed. 0 points: You must answer correctly to proceed. 2",
        "3": "Hi There is a Test. I mean, what is the difference? There is no such thing as an absolute test but if you",
        "4": "Hi There is a Test. A customer ’ s satisfaction with a service firm is based on how he perceives that the firm"
    }
  

### ** With swagger **

Use API page: [Ainize](https://ainize.ai/fpem123/GPT2-marketing-man?branch=main)

### ** With demo **

Use demo page: [End point](https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/)

--
