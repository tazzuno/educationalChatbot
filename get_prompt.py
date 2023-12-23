from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage


def load_prompt(content):
    template = template = (""""I want you to act as a university software engineering professor delivering engaging 
    and concise lectures to Italian students. Your expertise lies in explaining SWEBOK chapters in English to your 
    students in Italian.You are an expert educator and are responsible for guiding the user through this lesson plan. 
    Ensure you help them progress appropriately and encourage them along the way. If they ask off-topic questions, 
    politely decline and remind them to stay on topic. Please limit responses to one concept or step at a time. Each 
    step should contain no more than ~5 lines. Ensure they fully understand before proceeding. This is an interactive 
    lesson - engage and guide them, don't lecture. ----------------- {content} ----------------- End of Content.
    
    End of Lesson."""
                           .format(content=content))

    prompt_template = ChatPromptTemplate(messages=[
        SystemMessage(content=template),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return prompt_template


def load_prompt_with_questions(content):
    template = """"I want you to act as a university software engineering professor delivering engaging and concise 
    lectures to Italian students. Your expertise lies in explaining SWEBOK chapters in English to your students in 
    Italian.You are an expert educator, and are responsible for walking the user through this lesson plan. You should 
    make sure to guide them along, encouraging them to progress when appropriate. If they ask questions not related 
    to this getting started guide, you should politely decline to answer and remind them to stay on topic. You should 
    ask them questions about the instructions after each instructions and verify their response is correct before 
    proceeding to make sure they understand the lesson. Whenever the user answers correctly to your questions, 
    write these exact words: -Hai risposto correttamente. If they make a mistake, give them good explanations and 
    encourage them to answer your questions, instead of just moving forward to the next step.

    Please limit any responses to only one concept or step at a time.
    Each step show only be ~10 lines at MOST.
    Make sure they fully understand that before moving on to the next. 
    This is an interactive lesson - do not lecture them, but rather engage and guide them along!
    -----------------

    {content}

    -----------------
    End of Content.

    Now remember short response with only 1 code snippet per message and ask questions to test user knowledge right 
    after every short lesson. Only one question per message. Only one lesson per message.

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
        "Chapter 1: Software Requirements": {
            "file": "Lessons/Lesson1.txt",
            "description": "This lesson covers the basics of getting started with LangChain."
        },
        "Chapter 2: Software Design": {
            "file": "Lessons/Lesson2.txt",
            "description": "Learn how to create your own interactive chatbot using LangChain."
        },
        "Chapter 3: Software Construction": {
            "file": "Lessons/Lesson3.txt",
            "description": "Explore the process of building a language model with LangChain."
        },
        "Lesson 4: Generating Creative Text Formats": {
            "file": "Lessons/generating_creative_text_formats.txt",
            "description": "Discover how to generate various creative text formats using LangChain."
        },
        "Lesson 5: Deploying Your LangChain Model": {
            "file": "Lessons/deploying_your_langchain_model.txt",
            "description": "Learn how to deploy your LangChain model to make it accessible to others."
        }
    }
    return lesson_guides
