import streamlit as st
import random

# --- Core Logic ---
def load_words(filename="words_5letter.txt"):
    """Load 5-letter words from file."""
    try:
        with open(filename, 'r') as f:
            words = [line.strip().upper() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        return ["CRANE", "SLATE", "TRACE", "CRATE", "PLANT", "STORM", "CRISP", "LOGIC", "CYBER", "PILOT"]

def get_feedback(target, guess):
    """Algorithm to handle letter matching and duplicates per Wordle rules."""
    word_len = len(guess)
    result = ["-"] * word_len
    t_list, g_list = list(target[:word_len]), list(guess)

    for i in range(word_len):
        if g_list[i] == t_list[i]:
            result[i] = "G"
            t_list[i] = None
            g_list[i] = None

    for i in range(word_len):
        if g_list[i] and g_list[i] in t_list:
            result[i] = "Y"
            t_list[t_list.index(g_list[i])] = None

    return result

# --- Terminal Color Scheme ---
COLORS = {
    "G": "#00ff00",      # Terminal Green (exact match)
    "Y": "#ffff00",      # Terminal Yellow (wrong position)
    "-": "#333333",      # Dark gray (not in word)
    "unused": "#555555"  # Dim gray (untried)
}

TERMINAL_BG = "#0a0a0a"
TERMINAL_GREEN = "#00ff00"
TERMINAL_AMBER = "#ffff00"
TERMINAL_DIM = "#8b8686"

# --- Game Initialization ---
if 'target_word' not in st.session_state:
    st.session_state.target_word = random.choice(load_words()).upper()
    st.session_state.history = []
    st.session_state.kb_state = {l: "unused" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    st.session_state.game_over = False

# --- Page Config ---
st.set_page_config(page_title="WordGrep", layout="centered")

# --- Terminal Styles (injected CSS) ---
st.markdown(f"""
<style>
    .stApp {{
        background-color: {TERMINAL_BG};
    }}
    .stTextInput input {{
        background-color: #1a1a1a !important;
        color: {TERMINAL_GREEN} !important;
        font-family: 'Courier New', monospace !important;
        border: 1px solid #333 !important;
    }}
    .stButton button {{
        background-color: #1a1a1a !important;
        color: {TERMINAL_GREEN} !important;
        font-family: 'Courier New', monospace !important;
        border: 1px solid {TERMINAL_GREEN} !important;
    }}
    .stButton button:hover {{
        background-color: #2a2a2a !important;
        border-color: {TERMINAL_GREEN} !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- Header ---
# ASCII art with spaces converted to &nbsp; and newlines to <br>
ascii_lines = [
"      _    _               _  ____                  ",
"     | |  | |             | |/ ___|_ __ ___ _ __    ",
"    | |  | | ___  _ __ __| | |  _| '__/ _ \\ '_ \\  ",
"    | |/\\| |/ _ \\| '__/ _` | |_| | | |  __/ |_) | ",
"    \\  /\\  / (_) | | | (_| |\\____|_|  \\___| .__/",
"     \\/  \\/ \\___/|_|  \\__,_|             |_|    ",
]
ascii_html = "<br>".join(line.replace(" ", "&nbsp;") for line in ascii_lines)

header_html = f'''
<div style="font-family: 'Courier New', monospace; color: {TERMINAL_GREEN}; padding: 10px 0; border-bottom: 1px solid #333; margin-bottom: 20px; text-align: center;">
    <div style="font-size: 12px; line-height: 1.3; display: inline-block;">{ascii_html}</div>
</div>
'''
st.markdown(header_html, unsafe_allow_html=True)

# --- Legend ---
legend_html = f'''
<div style="font-family: 'Courier New', monospace; color: {TERMINAL_DIM}; text-align: center; margin-bottom: 20px; font-size: 14px;">
    <span style="color: {COLORS['G']};">[MATCH]</span> exact &nbsp;&nbsp;
    <span style="color: {COLORS['Y']};">[FOUND]</span> wrong position &nbsp;&nbsp;
    <span style="color: #666;">[_____]</span> not in word
</div>
'''
st.markdown(legend_html, unsafe_allow_html=True)

# --- Render the Grid ---
attempts_remaining = 6 - len(st.session_state.history)
grid_html = f'<div style="font-family: \'Courier New\', monospace; color: {TERMINAL_DIM}; text-align: center; margin-bottom: 10px; font-size: 14px;">attempts remaining: {attempts_remaining}/6</div>'
grid_html += '<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; margin-bottom: 20px;">'

for idx, (word, feedback) in enumerate(st.session_state.history):
    grid_html += f'<div style="display: flex; gap: 4px; align-items: center;">'
    grid_html += f'<span style="font-family: \'Courier New\', monospace; color: {TERMINAL_DIM}; font-size: 14px; width: 30px;">[{idx+1}]</span>'
    for char, status in zip(word, feedback):
        text_color = COLORS[status] if status != "-" else "#888"
        border_color = COLORS[status] if status != "-" else "#444"
        grid_html += f'''
            <div style="width:40px; height:40px; background:{TERMINAL_BG};
                        color:{text_color}; display:flex; align-items:center;
                        justify-content:center; font-weight:bold;
                        font-family: 'Courier New', monospace; font-size:20px;
                        border: 1px solid {border_color};">
                {char}
            </div>'''
    grid_html += '</div>'

# Empty rows for remaining attempts
for idx in range(len(st.session_state.history), 6):
    grid_html += f'<div style="display: flex; gap: 4px; align-items: center;">'
    grid_html += f'<span style="font-family: \'Courier New\', monospace; color: #333; font-size: 12px; width: 30px;">[{idx+1}]</span>'
    for _ in range(5):
        grid_html += f'''
            <div style="width:40px; height:40px; background:{TERMINAL_BG};
                        color:#333; display:flex; align-items:center;
                        justify-content:center; font-weight:bold;
                        font-family: 'Courier New', monospace; font-size:20px;
                        border: 1px solid #222;">
                _
            </div>'''
    grid_html += '</div>'

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

# --- Build Keyboard HTML ---
keyboard_rows = ["ABCDEFGHI", "JKLMNOPQR", "STUVWXYZ"]

kb_html = f'<div style="font-family: \'Courier New\', monospace; color: {TERMINAL_DIM}; text-align: center; margin-bottom: 5px; font-size: 14px;">-- keymap --</div>'
kb_html += '<div style="display: flex; flex-direction: column; align-items: center; gap: 3px;">'
for row in keyboard_rows:
    kb_html += '<div style="display: flex; gap: 3px;">'
    for letter in row:
        status = st.session_state.kb_state[letter]
        if status == "G":
            text_color = COLORS["G"]
            border_color = COLORS["G"]
        elif status == "Y":
            text_color = COLORS["Y"]
            border_color = COLORS["Y"]
        elif status == "-":
            text_color = "#444"
            border_color = "#333"
        else:
            text_color = "#888"
            border_color = "#444"

        kb_html += f'''
            <div style="width:28px; height:32px; background:{TERMINAL_BG};
                        color:{text_color}; display:flex; align-items:center;
                        justify-content:center; font-weight:bold;
                        font-family: 'Courier New', monospace; font-size:14px;
                        border: 1px solid {border_color};">
                {letter}
            </div>'''
    kb_html += '</div>'
kb_html += '</div>'

# --- Side-by-side: Input and Keyboard ---
col1, col2 = st.columns([1, 1])

with col1:
    if not st.session_state.game_over:
        prompt_html = f'<div style="font-family: \'Courier New\', monospace; color: {TERMINAL_GREEN}; margin-bottom: 5px;">$ enter guess:</div>'
        st.markdown(prompt_html, unsafe_allow_html=True)

        with st.form("guess_form", clear_on_submit=True):
            guess = st.text_input("Enter guess", max_chars=5, label_visibility="collapsed").upper()
            submit = st.form_submit_button("Execute")

            if submit:
                if len(guess) != 5:
                    st.markdown(f'<div style="font-family: \'Courier New\', monospace; color: #ff6b6b;">error: input must be exactly 5 characters</div>', unsafe_allow_html=True)
                elif not guess.isalpha():
                    st.markdown(f'<div style="font-family: \'Courier New\', monospace; color: #ff6b6b;">error: invalid characters detected</div>', unsafe_allow_html=True)
                else:
                    feedback = get_feedback(st.session_state.target_word, guess)
                    st.session_state.history.append((guess, feedback))

                    for char, stat in zip(guess, feedback):
                        curr = st.session_state.kb_state[char]
                        if stat == "G" or (stat == "Y" and curr != "G") or (stat == "-" and curr == "unused"):
                            st.session_state.kb_state[char] = stat

                    if guess == st.session_state.target_word:
                        st.session_state.game_over = True
                    elif len(st.session_state.history) >= 6:
                        st.session_state.game_over = True

                    st.rerun()

with col2:
    st.markdown(kb_html, unsafe_allow_html=True)

# --- Game Over Messages ---
if st.session_state.game_over:
    if st.session_state.history and st.session_state.history[-1][0] == st.session_state.target_word:
        msg_html = f'''
        <div style="font-family: 'Courier New', monospace; color: {TERMINAL_GREEN}; text-align: center; padding: 15px; border: 1px solid {TERMINAL_GREEN}; margin: 10px 0;">
            <div style="font-size: 14px;">$ grep "{st.session_state.target_word}" --result</div>
            <div style="font-size: 18px; margin-top: 10px;">MATCH FOUND in {len(st.session_state.history)}/6 attempts</div>
            <div style="font-size: 12px; color: {TERMINAL_DIM}; margin-top: 5px;">process exited with code 0</div>
        </div>
        '''
    else:
        msg_html = f'''
        <div style="font-family: 'Courier New', monospace; color: #ff6b6b; text-align: center; padding: 15px; border: 1px solid #ff6b6b; margin: 10px 0;">
            <div style="font-size: 14px;">$ grep "?????" --result</div>
            <div style="font-size: 18px; margin-top: 10px;">NO MATCH - word was: {st.session_state.target_word}</div>
            <div style="font-size: 12px; color: {TERMINAL_DIM}; margin-top: 5px;">process exited with code 1</div>
        </div>
        '''
    st.markdown(msg_html, unsafe_allow_html=True)

    if st.button("$ ./wordgrep --new"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
