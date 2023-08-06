import gradio as gr
import argparse
from threading import Thread
from chatglm_src import ChatGLMLLM
par = argparse.ArgumentParser()
par.add_argument("-a","--chatglm_api", default="http://localhost:8000")

model = None

def load_model(api):
    LLM = ChatGLMLLM(remote_host=api)
    return LLM



def parse_text(text):
    """copy from https://github.com/GaiZhenbiao/ChuanhuChatGPT/"""
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>"+line
    text = "".join(lines)
    return text


def predict(input, chatbot, max_length, top_p, temperature, history, past_key_values):
    chatbot.append((input, ""))
    model.history = history
    model.max_token = max_length
    model.top_p = top_p
    model.temperature = temperature

    for msg in model.stream(input):
        response = msg["response"]
        history = msg["history"]
        chatbot[-1] = (parse_text(input), parse_text(response))

        yield chatbot, history, past_key_values


def reset_user_input():
    return gr.update(value='')


def reset_state():
    return [], [], None



def main():
    args = par.parse_args()
    global remote_host
    global model
    remote_host = args.chatglm_api
    model = load_model(remote_host)
    # start_back()
    # if args.start_graph:
    #     t = Thread(target=start_graph, args=(args,))
    #     t.start()

    with gr.Blocks() as demo:
        gr.HTML("""<h1 align="center">ChatGLM2-6B</h1>""")

        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(scale=4):
                with gr.Column(scale=12):
                    user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10).style(
                        container=False)
                with gr.Column(min_width=32, scale=1):
                    submitBtn = gr.Button("Submit", variant="primary")
            with gr.Column(scale=1):
                emptyBtn = gr.Button("Clear History")
                max_length = gr.Slider(0, 32768, value=8192, step=1.0, label="Maximum length", interactive=True)
                top_p = gr.Slider(0, 1, value=0.9, step=0.01, label="Top P", interactive=True)
                temperature = gr.Slider(0, 1, value=0.01, step=0.01, label="Temperature", interactive=True)

        history = gr.State([])
        past_key_values = gr.State(None)

        submitBtn.click(predict, [user_input, chatbot, max_length, top_p, temperature, history, past_key_values],
                        [chatbot, history, past_key_values], show_progress=True)
        submitBtn.click(reset_user_input, [], [user_input])

        emptyBtn.click(reset_state, outputs=[chatbot, history, past_key_values], show_progress=True)

    demo.queue(concurrency_count=10).launch(share=False, inbrowser=True)
    