import streamlit as st
from agent.agent import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BharatAI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD CSS
# ============================================================

with open("style.css", "r", encoding="utf-8") as f:
    st.html(f"<style>{f.read()}</style>")


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("messages", [])
st.session_state.setdefault("recent_searches", [])
st.session_state.setdefault("pending", False)  # True while waiting for a reply


# ============================================================
# HELPERS
# ============================================================

def submit(prompt: str):
    """Add the user's message and mark it as waiting for a reply."""
    prompt = (prompt or "").strip()
    if not prompt or st.session_state.pending:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})

    recent = st.session_state.recent_searches
    if prompt in recent:
        recent.remove(prompt)
    recent.insert(0, prompt)
    st.session_state.recent_searches = recent[:8]

    st.session_state.pending = True


def answer_pending():
    """Ask the agent about the latest user message."""
    prompt = st.session_state.messages[-1]["content"]
    try:
        response = run_agent(prompt) or "Sorry, I couldn't generate a response."
    except Exception as e:
        response = f"Something went wrong. Try again in a moment.\n\nDetails: {e}"

    st.session_state.messages.append({"role": "assistant", "content": str(response)})
    st.session_state.pending = False


def new_chat():
    st.session_state.messages = []
    st.session_state.pending = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.html("""
    <div class="brand">
        <div class="brand-logo">IN</div>
        <div>BharatAI</div>
    </div>
    """)

    if st.button("✏️  New chat", use_container_width=True, key="new_chat"):
        new_chat()
        st.rerun()

    st.html("<div class='side-label'>Recent</div>")

    if st.session_state.recent_searches:
        for i, search in enumerate(st.session_state.recent_searches):
            if st.button(search, use_container_width=True, key=f"recent_{i}"):
                submit(search)
                st.rerun()
    else:
        st.html("<div class='side-empty'>No chats yet.</div>")

    st.html("""
    <div class="side-footer">
        Weather and news for India.<br>Made with ♥ for India
    </div>
    """)


# ============================================================
# EMPTY STATE: greeting + suggestions
# ============================================================

if not st.session_state.messages:

    st.html("""
    <div class="greeting">
        <div class="greeting-title">What can I help with?</div>
        <div class="greeting-sub">
            Ask about the weather, the latest news, or both.
        </div>
    </div>
    """)

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        if st.button("☀️  Weather in Delhi", use_container_width=True, key="s_weather"):
            submit("What is the current weather in Delhi?")
            st.rerun()

    with c2:
        if st.button("📰  Latest news in India", use_container_width=True, key="s_news"):
            submit("What are the latest news in India?")
            st.rerun()

    with c3:
        if st.button("✨  Lucknow weather and news", use_container_width=True, key="s_both"):
            submit(
                "Tell me the current weather in Lucknow "
                "and the latest news about Lucknow."
            )
            st.rerun()


# ============================================================
# CONVERSATION
# ============================================================

for message in st.session_state.messages:
    is_user = message["role"] == "user"
    with st.chat_message(
        "user" if is_user else "assistant",
        avatar="👤" if is_user else "🇮🇳",
    ):
        st.markdown(message["content"])

if st.session_state.pending:
    with st.chat_message("assistant", avatar="🇮🇳"):
        with st.spinner("Thinking…"):
            answer_pending()
    st.rerun()


# ============================================================
# MESSAGE BAR (Streamlit pins this to the bottom)
# ============================================================

prompt = st.chat_input("Message BharatAI")

if prompt:
    submit(prompt)
    st.rerun()