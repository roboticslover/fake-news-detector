import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
import time
import json

# Load environment variables - works in local environment
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Real-Time Multilingual Fake News Detector",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    .fake-tag {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 0.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .real-tag {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 0.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .uncertain-tag {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .search-result {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='main-header'>🔍 Real-Time Multilingual Fake News Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Analyze news content in multiple languages using AI to determine authenticity</p>", unsafe_allow_html=True)

# Check for required packages
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    search_tool_available = True
except ImportError:
    search_tool_available = False
    st.warning("DuckDuckGo search package is not installed. Run 'pip install -U duckduckgo-search' to enable web search functionality.")

# GitHub repository link
st.sidebar.markdown("[View Source Code](https://github.com/roboticslover/fake-news-detector)")

# Sidebar for API keys and settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Get API key - handle both local and cloud environments safely
    try:
        # Try to get from Streamlit secrets first (for cloud deployment)
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        st.success("OpenAI API key detected from Streamlit secrets! ✅")
    except Exception:
        # Fall back to environment variables (for local development)
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # If still no API key, allow manual entry
        if not openai_api_key:
            st.warning("No API key found. Please enter your OpenAI API key below.")
            openai_api_key = st.text_input("OpenAI API Key", 
                                          value="",
                                          type="password", 
                                          help="Required for analysis")
        else:
            st.success("OpenAI API key detected from environment variables! ✅")
    
    model_choice = st.selectbox(
        "Select OpenAI Model",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    # Language selection
    language_choice = st.selectbox(
        "Select Analysis Language",
        ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Arabic", "Russian", "Japanese", "Portuguese"],
        index=0
    )
    
    if not search_tool_available:
        st.error("DuckDuckGo search is not available. Some functionality will be limited.")
        st.markdown("""
        To fix, open your terminal and run:
        ```
        pip install -U duckduckgo-search
        ```
        Then restart the app.
        """)
    
    st.divider()
    st.markdown("### How it works")
    st.markdown("""
    1. Enter news text in any language
    2. Select the language for analysis results
    3. The system searches multiple sources
    4. AI analyzes the information in real-time
    5. Results show why content might be fake or confirmed as real
    """)

# Initialize search tools
if search_tool_available:
    from langchain_community.tools import DuckDuckGoSearchRun
    search = DuckDuckGoSearchRun(name="Search")
else:
    search = None

wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# Function to run search queries
def run_search(query):
    results = []
    
    # Run DuckDuckGo search if available
    if search_tool_available:
        try:
            st.write("🔎 Searching web sources...")
            search_result = search.run(query)
            results.append(("Web Search", search_result))
        except Exception as e:
            st.error(f"Error during web search: {str(e)}")
    
    # Run Wikipedia search
    try:
        st.write("📚 Searching Wikipedia...")
        wiki_result = wiki.run(query)
        results.append(("Wikipedia", wiki_result))
    except Exception as e:
        st.error(f"Error during Wikipedia search: {str(e)}")
    
    return results

# Function to verify news with search results
def verify_news(content, language="English", search_results=None):
    if not openai_api_key:
        st.error("Please provide an OpenAI API key in the sidebar or set it in Streamlit Cloud secrets")
        return None
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=model_choice,
        api_key=openai_api_key,
        temperature=0
    )
    
    # Language-specific instructions
    lang_instructions = {
        "English": "Provide your response in English.",
        "Spanish": "Proporciona tu respuesta en español.",
        "French": "Fournissez votre réponse en français.",
        "German": "Geben Sie Ihre Antwort auf Deutsch.",
        "Hindi": "अपना जवाब हिंदी में दें।",
        "Chinese": "用中文提供您的回答。",
        "Arabic": "قدم إجابتك باللغة العربية.",
        "Russian": "Предоставьте ваш ответ на русском языке.",
        "Japanese": "日本語で回答してください。",
        "Portuguese": "Forneça sua resposta em português."
    }
    
    # Format search results for the prompt
    search_context = ""
    if search_results:
        for source, result in search_results:
            search_context += f"--- {source} Results ---\n{result}\n\n"
    
    # Prepare system prompt
    system_prompt = f"""You are an expert fact-checker. You need to analyze news content and determine if it's REAL, FAKE, or UNCERTAIN.

IMPORTANT: You must provide a clear verdict of either REAL, FAKE, or UNCERTAIN. 
Reserve "UNCERTAIN" only for cases where there is genuinely insufficient information to make a determination.

Here are the search results found for this claim:

{search_context}

Analyze the claim against these search results and determine if the claim is REAL, FAKE, or UNCERTAIN.

Your response must be in JSON format with the following structure:
{{
    "verdict": "REAL/FAKE/UNCERTAIN",
    "confidence": "high/medium/low",
    "explanation": "Your detailed explanation",
    "supporting_facts": ["fact 1", "fact 2", ...],
    "contradicting_facts": ["contradiction 1", "contradiction 2", ...],
    "red_flags": ["red flag 1", "red flag 2", ...]
}}

{lang_instructions.get(language, "Provide your response in English.")}
"""
    
    # User prompt with the news content
    user_prompt = f"NEWS CLAIM TO VERIFY: {content}"
    
    try:
        # Get response
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        # Parse the JSON response
        try:
            return json.loads(response.content)
        except:
            # If JSON parsing fails, return the raw response
            st.error("Error parsing the analysis results. Showing raw response.")
            return {"verdict": "ERROR", "explanation": response.content}
            
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None

# Real-time analysis indicator
def show_real_time_indicator():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(101):
        # Update progress bar and status
        progress_bar.progress(i)
        if i < 30:
            status_text.text("Searching for relevant sources...")
        elif i < 60:
            status_text.text("Cross-referencing information...")
        elif i < 90:
            status_text.text("Analyzing content authenticity...")
        else:
            status_text.text("Finalizing verdict...")
        
        time.sleep(0.03)  # Simulate real-time processing
    
    # Clear the temporary elements once done
    progress_bar.empty()
    status_text.empty()

# Main interface for text input
news_text = st.text_area(
    "Enter the news text or claim to verify (in any language):",
    height=150,
    placeholder="Paste the news content or claim that you want to fact-check..."
)

verify_text_button = st.button("Verify News", type="primary", use_container_width=True)

if verify_text_button and news_text:
    # Check if we have required components
    if not search_tool_available:
        st.warning("Search functionality is limited. Install duckduckgo-search package for better results.")
        
    # Get the selected language from sidebar
    selected_language = language_choice
    
    with st.spinner("Initializing analysis..."):
        # First run searches and display results progressively
        search_results = run_search(news_text)
        
        # Show search results
        st.subheader("Search Results")
        for source, result in search_results:
            with st.expander(f"{source} Results", expanded=False):
                st.markdown(f"<div class='search-result'>{result}</div>", unsafe_allow_html=True)
        
        # Show real-time analysis indicator
        st.subheader("Analysis Progress")
        show_real_time_indicator()
        
        # Verify the news with the search results
        analysis_result = verify_news(news_text, selected_language, search_results)
        
        if analysis_result:
            st.subheader("Analysis Results")
            
            # Display verdict with appropriate styling
            verdict = analysis_result.get("verdict", "UNCERTAIN").upper()
            if "FAKE" in verdict:
                st.markdown("<p class='fake-tag'>VERDICT: FAKE</p>", unsafe_allow_html=True)
            elif "REAL" in verdict:
                st.markdown("<p class='real-tag'>VERDICT: REAL</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='uncertain-tag'>VERDICT: UNCERTAIN</p>", unsafe_allow_html=True)
            
            # Display confidence level if available
            if "confidence" in analysis_result:
                st.write(f"**Confidence Level:** {analysis_result['confidence'].capitalize()}")
            
            # Display explanation
            if "explanation" in analysis_result:
                st.write("### Explanation")
                st.write(analysis_result["explanation"])
            
            # Display supporting facts if available
            if "supporting_facts" in analysis_result and analysis_result["supporting_facts"]:
                st.write("### Supporting Facts")
                for fact in analysis_result["supporting_facts"]:
                    st.markdown(f"✅ {fact}")
            
            # Display contradicting facts if available
            if "contradicting_facts" in analysis_result and analysis_result["contradicting_facts"]:
                st.write("### Contradicting Facts")
                for fact in analysis_result["contradicting_facts"]:
                    st.markdown(f"❌ {fact}")
            
            # Display red flags if available
            if "red_flags" in analysis_result and analysis_result["red_flags"]:
                st.write("### Red Flags")
                for flag in analysis_result["red_flags"]:
                    st.markdown(f"🚩 {flag}")

# App footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.8rem;">
    Developed by roboticslover | Powered by OpenAI + LangChain | For educational purposes only
</div>
""", unsafe_allow_html=True)