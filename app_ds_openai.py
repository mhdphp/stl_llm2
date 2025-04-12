import streamlit as st
from langchain import PromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_openai import OpenAI

# Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")

# Intro: instructions
col1, col2 = st.columns(2)
with col1:
    st.markdown("Re-write your text in different styles.")
with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com) to build your AI Projects")

# Input OpenAI API Key
st.markdown("## Enter Your API Key")

def get_api_key():
    input_text = st.text_input(label="API Key", placeholder="Ex: sk-... or ds-...", 
                             key="api_key_input", type="password")
    return input_text

api_key = get_api_key()

# Model selection
st.markdown("## Choose Your AI Model")
model_provider = st.selectbox(
    'Select AI Provider',
    ('OpenAI', 'Deepseek'),
    key='model_provider'
)

# LLM loading function
def load_LLM(api_key):
    """Load the selected LLM model"""
    if not api_key:
        st.warning('Please enter your API key', icon="⚠️")
        return None
    
    try:
        if st.session_state.model_provider == "OpenAI":
            #from langchain_openai import OpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=.7, openai_api_key=api_key)
        else:
            #from langchain_community.llms import Deepseek
            llm = ChatDeepSeek(model="deepseek-chat", temperature=.7, api_key=api_key)
        return llm
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Text input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', 
                            placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

# Prompt template
template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining the company as its Chief Executive Officer. After a period of five days of conversations, discussions, and deliberations, the decision to bring back Altman, who had been previously dismissed, has been made. We are delighted to welcome Sam back to OpenAI.
    - Informal: Hey everyone, it's been a wild week! We've got some exciting news to share - Sam Altman is back at OpenAI, taking up the role of chief executive. After a bunch of intense talks, debates, and convincing, Altman is making his triumphant return to the AI startup he co-founded.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Please start the redaction with a warm introduction. Add the introduction if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)

# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not api_key:
        st.warning(f'Please insert {st.session_state.model_provider} API Key', icon="⚠️")
        st.stop()

    llm = load_LLM(api_key)
    if llm is None:
        st.stop()

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    try:
        improved_redaction = llm(prompt_with_draft)
        st.write(improved_redaction)
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")