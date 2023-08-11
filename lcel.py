import langchain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI, ChatAnthropic
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

from langchain.chat_models import ChatOpenAI


content = """Follow the below lesson plan, using information from the blog, cookbook, and interface guide.

<lesson_plan>
{lesson}
</lesson_plan>

<blog>
{blog}
</blog>

<cookbook>
{cookbook}
</cookbook>

<iterface_guide>
{interface}
<interface_guide>"""
with open("lcel/guide.md") as f:
    guide = f.read()
    
with open("lcel/interface.md") as f:
    interface = f.read()
    
with open("lcel/blog.txt") as f:
    blog = f.read()

with open("lcel/lesson.txt") as f:
    lesson = f.read()

from get_prompt import load_prompt
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory


prompt_template = load_prompt(content = content.format(cookbook=guide, interface=interface, blog=blog, lesson=lesson))

from langchain.chains import LLMChain

def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Welcome! This short course with help you started with LangChain Expression Language. In order to get started, you should have basic familiarity with LangChain and you should have Python environment set up with langchain installed. If you don't have that, please set that up. Let me know when you're ready to proceed!")]

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k")
        #model = ChatAnthropic(streaming=True, callbacks=[stream_handler], model="claude-2")
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

