from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage


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

	{content}

	-----------------
	End of Content.

	Now remember short response with only 1 code snippet per message.""".format(content=content)

    prompt_template = ChatPromptTemplate(messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template


def load_prompt_with_questions(content):
    template = """You are an expert educator, and are responsible for walking the user \
	through this lesson plan. You should make sure to guide them along, \
	encouraging them to progress when appropriate. \
	If they ask questions not related to this getting started guide, \
	you should politely decline to answer and remind them to stay on topic.\
	You should ask them questions about the instructions after each instructions \
	and verify their response is correct before proceeding to make sure they understand \
	the lesson. If they make a mistake, give them good explanations and encourage them \
	to answer your questions, instead of just moving forward to the next step. 

	Please limit any responses to only one concept or step at a time. \
	Each step show only be ~5 lines of code at MOST. \
	Only include 1 code snippet per message - make sure they can run that before giving them any more. \
	Make sure they fully understand that before moving on to the next. \
	This is an interactive lesson - do not lecture them, but rather engage and guide them along!\
	-----------------

	{content}


	-----------------
	End of Content.

	Now remember short response with only 1 code snippet per message and ask questions\
	to test user knowledge right after every short lesson.

	Your teaching should be in the following interactive format:

	Short lesson 3-5 sentences long
	Questions about the short lesson (1-3 questions)

	Short lesson 3-5 sentences long
	Questions about the short lesson (1-3 questions)
	...

	 """.format(content=content)

    prompt_template = ChatPromptTemplate(messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template


def get_lesson_guide():
    lesson_guides = {
        "Lesson 1: Getting Started with LangChain": {
            "file": "lc_guides/getting_started_guide.txt",
            "description": "This lesson covers the basics of getting started with LangChain."
        },
        "Lesson 2: Creating a Chatbot": {
            "file": "lc_guides/creating_a_chatbot.txt",
            "description": "Learn how to create your own interactive chatbot using LangChain."
        },
        "Lesson 3: Building a Language Model": {
            "file": "lc_guides/building_a_language_model.txt",
            "description": "Explore the process of building a language model with LangChain."
        },
        "Lesson 4: Generating Creative Text Formats": {
            "file": "lc_guides/generating_creative_text_formats.txt",
            "description": "Discover how to generate various creative text formats using LangChain."
        },
        "Lesson 5: Deploying Your LangChain Model": {
            "file": "lc_guides/deploying_your_langchain_model.txt",
            "description": "Learn how to deploy your LangChain model to make it accessible to others."
        }
    }
    return lesson_guides
