from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langsmith import Client
client = Client()



st.set_page_config(page_title="LangChain: Getting Started Class", page_icon="🦜")
st.title("🦜 LangChain: Getting Started Class")
button_css =""".stButton>button {
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

with open("guide.txt", "r") as f:
    guide = f.read()
from langchain.chat_models import ChatOpenAI



from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

template = """The below is a "Getting Started" guide for LangChain. You are an expert educator, and are responsible for walking the user through this getting started guide. You should make sure to guide them along, encouraging them to progress when appropriate. If they ask questions not related to this getting started guide, you should politely decline to answer and resume trying to teach them about LangChain!

Please limit any responses to only one concept or step at a time. Make sure they fully understand that before moving on to the next. This is an interactive lesson - do not lecture them, but rather engage and guide them along!

When they have finished the guide, congragulate them and tell them to move onto the next section.
-----------------
{content}""".format(content=guide)

prompt_template = ChatPromptTemplate(messages = [SystemMessage(content=template), MessagesPlaceholder(variable_name="chat_history"), HumanMessagePromptTemplate.from_template("{input}")])

from langchain.chains import LLMChain

def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Welcome! This short course with help you started with LangChain, and will cover LLMs, prompts, output parsers, and LLMChains.Before doing this, you should have a Python environment set up. Do you have that done?")]

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-4")
        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain({"input":prompt, "chat_history":st.session_state.messages[-20:]}, include_run_info=True)
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
        run_id = response["__run"].run_id

        col_blank, col_text, col1, col2 = st.columns([10, 2,1,1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))

