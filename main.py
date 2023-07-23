from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st


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
-----------------
{content}""".format(content=guide)

prompt_template = ChatPromptTemplate(messages = [SystemMessage(content=template), MessagesPlaceholder(variable_name="chat_history"), HumanMessagePromptTemplate.from_template("{input}")])

from langchain.chains import LLMChain

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="Welcome to the class on LangChain! Before doing this, you should have a Python environment set up. Do you have that done?")]

for msg in st.session_state["messages"]:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler])
        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain.run(input=prompt, chat_history=st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.session_state.messages.append(ChatMessage(role="assistant", content=response))