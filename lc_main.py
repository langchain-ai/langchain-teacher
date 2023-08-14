import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langsmith import Client
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from get_prompt import load_prompt, load_prompt_with_questions

st.set_page_config(page_title="LangChain: Getting Started Class", page_icon="🦜")
st.title("🦜 LangChain: Getting Started Class")
button_css = """.stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 2em;
    width: 2em;
    font-size: 4px;
}"""
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Load guides
with open("guide.txt", "r") as f:
    guide = f.read()
with open("lc_guides/prompt_guide.txt", "r") as f:
    prompt_guide = f.read()
with open("lc_guides/models_guide.txt", "r") as f:
    models_guide = f.read()
with open("lc_guides/memory_guide.txt", "r") as f:
    memory_guide = f.read()

# Initialize LangSmith client
client = Client()

# Lesson selection sidebar
lesson_selection = st.sidebar.selectbox("Select Lesson", [
    "Lesson 1: Getting Started with LangChain",
    "Lesson 2: Prompts",
    "Lesson 3: Language Models",
    "Lesson 4: Memory"
])

# Display lesson content and description based on selection
if lesson_selection == "Lesson 1: Getting Started with LangChain":
    lesson_content = guide
    lesson_description = "This lesson covers the basics of getting started with LangChain."
elif lesson_selection == "Lesson 2: Prompts":
    lesson_content = prompt_guide
    lesson_description = "This lesson focuses on prompts and their usage."
elif lesson_selection == "Lesson 3: Language Models":
    lesson_content = models_guide
    lesson_description = "This lesson provides an overview of language models."
else:
    lesson_content = memory_guide
    lesson_description = "This lesson is about Memory."

prompt_template = load_prompt(content=lesson_content)

# Radio buttons for lesson type selection
lesson_type = st.sidebar.radio("Select Lesson Type", ["Instructions based lesson", "Interactive lesson with questions"])

# Clear chat session if dropdown option or radio button changes
if st.session_state.get("current_lesson") != lesson_selection or st.session_state.get("current_lesson_type") != lesson_type:
    st.session_state["current_lesson"] = lesson_selection
    st.session_state["current_lesson_type"] = lesson_type
    st.session_state["messages"] = [AIMessage(content="Welcome! This short course will help you get started with LangChain.")]

# Display lesson name and description
st.markdown(f"**{lesson_selection}**")
st.write(lesson_description)

# Message handling and interaction
def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo")

        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain(
            {"input": prompt, "chat_history": st.session_state.messages[-20:]},
            include_run_info=True,
            tags=[lesson_selection]
        )
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
        run_id = response["__run"].run_id

        col_blank, col_text, col1, col2 = st.columns([10, 2, 1, 1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))
