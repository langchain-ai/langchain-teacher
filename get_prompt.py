from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

def load_prompt(content):

	template = """You are an expert educator, and are responsible for walking the user \
	through this lesson plan. You should make sure to guide them along, \
	encouraging them to progress when appropriate. \
	If they ask questions not related to this getting started guide, \
	you should politely decline to answer and remind them to stay on topic.

	Please limit any responses to only one concept or step at a time. \
	Each step show only be ~5 lines of code at MOST. \
	Only include 1 code snippet per message - make sure they can run that before giving them any more. \
	Make sure they fully understand that before moving on to the next. \
	This is an interactive lesson - do not lecture them, but rather engage and guide them along!
	-----------------

	{content}""".format(content=content)

	prompt_template = ChatPromptTemplate(messages = [
		SystemMessage(content=template), 
		MessagesPlaceholder(variable_name="chat_history"), 
		HumanMessagePromptTemplate.from_template("{input}")
		])
	return prompt_template
