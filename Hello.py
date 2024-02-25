import os
import anthropic
import streamlit as st

async def start_chat():
    st.user_session.set(
        "prompt_history",
        "",
    )
    await st.Avatar(
        name="Claude",
        url="https://www.anthropic.com/images/icons/apple-touch-icon.png",
    ).send()
    await get_conversation_theme()


def ask_name():
    name = st.text_input("Mind Craft: What's your name?", "")
    if name:
        st.write(f"Hello, {name}!")


async def get_conversation_theme():
    topic = await st.AskUserMessage(
        content="Hello, what would you like to learn about today?",
        timeout=30).send()
    style = await st.AskUserMessage(
         content="What style of learning would you like to use?",
        timeout=30).send()
    interests = await st.AskUserMessage(
        content=
        "Is there anything you are particularly passionate about as well?",
        timeout=30).send()
    st.user_session.set("topic", topic)
    st.user_session.set("level", level)
    st.user_session.set("interests", interests)


#@st.step(name="Claude", type="llm", root=True)
async def call_claude(query: str):
    prompt_history = cl.user_session.get("prompt_history")

    # basic example prompt
    prompt = f"{prompt_history}{anthropic.HUMAN_PROMPT}{query}{anthropic.AI_PROMPT}"

    level = '<LEVEL>{st.user_session.get("level"))</LEVEL>'
    why = '<WHY>{st.user_session.get("why")}</WHY>'
    interest = 0
    promppt = f"{level}{why}"
    # Example teaching oriented prompt
    prompt = f"Your past messages are demarcated in <HISTORY></HISTORY> <HISTORY>{prompt_history}</HISTORY>" \
            f'{anthropic.HUMAN_PROMPT}Become an expert technical writer and educator capable of teaching anything to anyone at any <LEVEL>{st.user_session.get("level")}"</LEVEL> with any context. Where possible tailor the content based on the reason {why}" they want to learn the subject (indicated by the why tags), their background information (indicated by context tags), and their <INTERESTS>{st.user_session.get("interests")}</INTERESTS>.' \
            f'Please provide a detailed and informative response to the students question or requwstgrounded in the context of <TOPIC>{st.user_session.get("topic")}</TOPIC>' \
            f'{anthropic.HUMAN_PROMPT}You are an expert technical writer and teacher. ' \
            f'A student has asked you to help them understand the following topic: <TOPIC>{st.user_session.get("topic")}</TOPIC>'

    settings = {
        "stop_sequences": [anthropic.HUMAN_PROMPT],
        "max_tokens_to_sample": 1000,
        "model": "claude-2.1",
    }

    stream = await c.completions.create(
        prompt=prompt,
        stream=True,
        **settings,
    )

    async for data in stream:
        token = data.completion
    await st.context.current_step.stream_token(token)

    st.context.current_step.generation = cl.CompletionGeneration(
        formatted=prompt,
        completion=cl.context.current_step.output,
        settings=settings,
        provider=Anthropic.id,
    )

    cl.user_session.set("prompt_history",
                        prompt + cl.context.current_step.output)


@cl.on_message
async def chat(message: cl.Message):
    await call_claude(message.content)

if __name__ == "__main__":
    with st.sidebar:
        anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    #streamlit UI
    st.title("Mind Craft 🧠")
    st.write("Welcome to Mind Craft! This is your personalized learnig journey. Craft your learning to your mind!")

if start_chat and not anthropic_api_key:
    st.info("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")
    
    if start_chat and anthropic_api_key:
        pass # fix