
"""

"C:/Users/username/AppData/Local/nomic.ai/GPT4All/ggml-gpt4all-l13b-snoozy.bin"

Prompt-Templates:
 ### Response:

gpt4all.GPT4All.download_model('ggml-gpt4all-l13b-snoozy.bin','.')
 
"""
import sys
import os.path

class TransientGpt4All:
    model = ''
    def __init__(self, model):
        self.model = model
    def chat_completion(self, **kwargs):
        gptj = GPT4All(self.model)
        return gptj.chat_completion(**kwargs)

class LlmExecutor:
    chat = None
    def __init__(self, chat):
        self.chat = chat
    def __call__(self, data):
        prompt = data['prompt']
        messages = [{"role": "user", "content": prompt}]
        res = {'success': True}
        res['chat'] = messages
        if self.chat.__class__.__name__=='GPT4ALL':
            result = self.chat.chat_completion(messages, default_prompt_header=False,  default_prompt_footer=False, streaming=False)
            response = result['choices'][0]['message']['content']
        else:
            response = 'No Backend to answer.'
            res['success'] = False
        res['response'] = response
        res['input'] = data
        return res 

def load_gpt4all(file):
    from gpt4all import GPT4All
    if os.path.isfile(file):
        if '-transient' in sys.argv or '-t' in sys.argv:
            gptj = TransientGpt4All(file)
        else:
            gptj = GPT4All(file)
        return gptj
    else:
        print("Error: Model File Not Found.")
        exit()

def main():
    print("LLM")
    gptj = load_gpt4all(sys.argv[1])
    executor = LlmExecutor(chat=gptj)
    if len(sys.argv)>2:
        infile = sys.argv[2]
        outfile = sys.argv[3]
        runner = JobRunner(executor)
        if infile == 'rest':
            runner.execute_rest()
        else:
            runner.execute_file(infile, outfile)
    else:
        print("python -m nwebclient.llm model_file")
        print("Usage: model_file infile outfile")
        print("Usage: model_file rest api")
        print("Option: -t --transient fuer TransientGpt4All")
        
if __name__ == '__main__':
    main()