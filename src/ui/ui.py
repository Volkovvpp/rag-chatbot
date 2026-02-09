import logging
import gradio as gr
from src.core.config import settings
from src.core.logger import setup_logger
from src.rag.rag_llm import answer_question_with_context


setup_logger()
logger = logging.getLogger(__name__)

PASSWORD = settings.ADMIN_PASSWORD

def handle_generation(user_question):
    answer, sources = answer_question_with_context(user_question)
    return answer, sources

def check_password(pw):
    if pw == PASSWORD:
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
        )
    else:
        return (
            gr.update(),
            gr.update(value="Incorrect password ", visible=True),
            gr.update(visible=False),
        )

with gr.Blocks() as demo:
    gr.Markdown("## Login to Document QA Chatbot")

    with gr.Row():
        password_input = gr.Textbox(label="Enter password", type="password", show_label=False, placeholder="Password...")
        password_status = gr.Markdown(visible=False)

    with gr.Column(visible=False) as chat_ui:
        gr.Markdown("## Document QA Chatbot")

        question_input = gr.Textbox(label="Your question")
        generate_button = gr.Button("Generate answer")

        answer_output = gr.Textbox(label="Answer", interactive=False)
        sources_output = gr.Textbox(label="Sources", interactive=False)

        generate_button.click(
            handle_generation,
            inputs=[question_input],
            outputs=[answer_output, sources_output]
        )

    password_input.submit(
        check_password,
        inputs=[password_input],
        outputs=[password_input, password_status, chat_ui]
    )

demo.launch(server_name="127.0.0.1", server_port=7860)
