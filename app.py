import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast
import chainlit as cl
from src.prompt import system_instruction

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

@cl.on_chat_start
async def on_chat_start():
    # Initialize the chat history
    cl.user_session.set("chat_history", [])

    model = ChatGroq(
        model = 'llama-3.3-70b-versatile',
        temperature = 0.0,
        streaming=True,
        cache=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_instruction),
            ("assistant", "{chat_history}"),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable
    chat_history = cl.user_session.get("chat_history")
    
    # Format chat history
    formatted_history = "\n".join(chat_history)

    msg = cl.Message(content="")
    async for chunk in runnable.astream(
        {
            "question": message.content,
            "chat_history": formatted_history
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    # Update chat history
    chat_history.append(f"Human: {message.content}")
    chat_history.append(f"Assistant: {msg.content}")
    cl.user_session.set("chat_history", chat_history)

    await msg.send()
