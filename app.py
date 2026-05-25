import streamlit as st
import os
import binascii
from triple_des import TripleDES

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Triple DES",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

:root {
    --bg:        #0a0e14;
    --panel:     #0f1520;
    --border:    #1e3a5f;
    --accent:    #00d4ff;
    --accent2:   #00ff9d;
    --danger:    #ff4560;
    --text:      #c9d8e8;
    --muted:     #4a6680;
    --mono:      'Share Tech Mono', monospace;
    --sans:      'Rajdhani', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Title ── */
.title-block {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.title-block h1 {
    font-family: var(--mono);
    font-size: 2.8rem;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-shadow: 0 0 30px rgba(0,212,255,0.4);
    margin: 0;
}
.title-block p {
    font-family: var(--sans);
    color: var(--muted);
    font-size: 1.05rem;
    margin-top: 0.4rem;
    letter-spacing: 0.06em;
}

/* ── Panels ── */
.panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
}
.panel-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--accent);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Output box ── */
.output-box {
    background: #060a10;
    border: 1px solid var(--accent);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    font-family: var(--mono);
    font-size: 0.88rem;
    color: var(--accent2);
    word-break: break-all;
    line-height: 1.6;
    min-height: 60px;
    box-shadow: inset 0 0 20px rgba(0,212,255,0.04), 0 0 12px rgba(0,212,255,0.1);
}

/* ── Step trace ── */
.step-trace {
    background: #060a10;
    border-left: 3px solid var(--accent);
    padding: 0.9rem 1.1rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.9;
    border-radius: 0 4px 4px 0;
    margin-top: 0.8rem;
}
.step-trace .step { color: var(--text); }
.step-trace .val  { color: var(--accent2); }

/* ── Badge ── */
.badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.68rem;
    padding: 0.18rem 0.6rem;
    border-radius: 3px;
    letter-spacing: 0.1em;
    margin-right: 0.4rem;
}
.badge-blue  { background: rgba(0,212,255,0.12); color: var(--accent);  border: 1px solid rgba(0,212,255,0.3); }
.badge-green { background: rgba(0,255,157,0.10); color: var(--accent2); border: 1px solid rgba(0,255,157,0.3); }
.badge-red   { background: rgba(255,69,96,0.12); color: var(--danger);  border: 1px solid rgba(255,69,96,0.3); }

/* ── Streamlit widget overrides ── */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: #060a10 !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
label, .stSelectbox label, .stRadio label {
    font-family: var(--sans) !important;
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #060a10 !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.stButton button {
    background: linear-gradient(135deg, #003d5c, #005580) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    letter-spacing: 0.12em !important;
    font-size: 0.9rem !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.8rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 14px rgba(0,212,255,0.15) !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #005580, #0077aa) !important;
    box-shadow: 0 0 22px rgba(0,212,255,0.35) !important;
}

/* ── Radio ── */
.stRadio > div { gap: 1rem !important; flex-direction: row !important; }
.stRadio > div > label {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 0.3rem 1rem !important;
    cursor: pointer !important;
    color: var(--text) !important;
    font-size: 0.85rem !important;
    text-transform: none !important;
    letter-spacing: 0.05em !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Info / warning boxes ── */
[data-testid="stAlert"] {
    background: rgba(0,212,255,0.06) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 4px !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h1>// TRIPLE-DES</h1>
    <p>Encrypt &amp; Decrypt · Pure Python Implementation · EDE Mode</p>
</div>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="panel-label">⬡ Configuration</div>', unsafe_allow_html=True)

    key_mode = st.selectbox("Key Mode", ["3-key (24 bytes / 168-bit)", "2-key (16 bytes / 112-bit)"])
    block_mode = st.selectbox("Block Cipher Mode", ["CBC", "ECB"])

    # Key input — on_click callbacks run BEFORE widgets render, so session state
    # is already updated when the text_input reads st.session_state["key_in"]
    key_len = 24 if "3-key" in key_mode else 16

    def _gen_key_cb():
        st.session_state["key_in"] = os.urandom(key_len).hex()

    def _gen_iv_cb():
        st.session_state["iv_in"] = os.urandom(8).hex()

    if "key_in" not in st.session_state:
        st.session_state["key_in"] = ""
    if "iv_in" not in st.session_state:
        st.session_state["iv_in"] = ""

    key_placeholder = "48 hex chars (24 bytes)" if "3-key" in key_mode else "32 hex chars (16 bytes)"
    st.markdown("**Hex Key**")
    key_input = st.text_input("", placeholder=key_placeholder,
                               label_visibility="collapsed", key="key_in")
    st.button("⟳  Generate Random Key", on_click=_gen_key_cb)

    if block_mode == "CBC":
        st.markdown("**IV (Initialization Vector)**")
        iv_input = st.text_input("", placeholder="16 hex chars (8 bytes) — blank = 00…00",
                                  label_visibility="collapsed", key="iv_in")
        st.button("⟳  Generate Random IV", on_click=_gen_iv_cb)
    else:
        iv_input = ""

    st.markdown("---")
    operation = st.radio("Operation", ["Encrypt", "Decrypt"], horizontal=True)

with col_right:
    st.markdown('<div class="panel-label">⬡ Input / Output</div>', unsafe_allow_html=True)

    if operation == "Encrypt":
        input_label = "Plaintext"
        input_placeholder = "Enter text to encrypt…"
        hint = "UTF-8 text → PKCS#7 padded → 3DES-EDE → hex output"
    else:
        input_label = "Ciphertext (hex)"
        input_placeholder = "Paste hex ciphertext…"
        hint = "Hex ciphertext → 3DES-EDE → PKCS#7 unpadded → UTF-8"

    user_input = st.text_area(input_label, placeholder=input_placeholder,
                               height=130, label_visibility="visible")
    st.caption(hint)

    run = st.button("▶  RUN", use_container_width=True)

# ── Processing ─────────────────────────────────────────────────────────────────
if run:
    errors = []

    # Validate key
    raw_key_hex = key_input.strip().replace(" ", "")
    expected_key_bytes = 24 if "3-key" in key_mode else 16
    if not raw_key_hex:
        errors.append("Key is required.")
    elif not all(c in "0123456789abcdefABCDEF" for c in raw_key_hex):
        errors.append("Key must be a valid hex string.")
    elif len(raw_key_hex) != expected_key_bytes * 2:
        errors.append(f"Key must be {expected_key_bytes*2} hex chars for {key_mode}.")

    # Validate IV
    raw_iv_hex = iv_input.strip().replace(" ", "")
    if block_mode == "CBC":
        if raw_iv_hex and (len(raw_iv_hex) != 16 or not all(c in "0123456789abcdefABCDEF" for c in raw_iv_hex)):
            errors.append("IV must be exactly 16 hex chars (8 bytes).")

    if not user_input.strip():
        errors.append("Input text is required.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        try:
            key_bytes = bytes.fromhex(raw_key_hex)
            iv_bytes  = bytes.fromhex(raw_iv_hex) if raw_iv_hex else bytes(8)
            cipher    = TripleDES(key_bytes, mode=block_mode, iv=iv_bytes)

            if operation == "Encrypt":
                plaintext    = user_input.encode("utf-8")
                ciphertext   = cipher.encrypt(plaintext)
                output_hex   = ciphertext.hex()

                # ── Result ──
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.markdown(f'<span class="badge badge-blue">{key_mode.split()[0].upper()} KEY</span>', unsafe_allow_html=True)
                c2.markdown(f'<span class="badge badge-green">{block_mode} MODE</span>', unsafe_allow_html=True)
                c3.markdown(f'<span class="badge badge-red">EDE ENCRYPT</span>', unsafe_allow_html=True)

                st.markdown('<div class="panel-label" style="margin-top:1rem">Ciphertext (hex)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{output_hex}</div>', unsafe_allow_html=True)

                # ── EDE Step trace ──
                k1 = key_bytes[:8].hex()
                k2 = key_bytes[8:16].hex()
                k3 = (key_bytes[:8] if len(key_bytes)==16 else key_bytes[16:]).hex()
                first_block = plaintext[:8].ljust(8, b'\x00')
                from triple_des import des_encrypt_block, des_decrypt_block, _pad
                padded = _pad(plaintext)
                b0 = padded[:8]
                if block_mode == "CBC":
                    b0 = bytes(a ^ b for a, b in zip(b0, iv_bytes))
                s1 = des_encrypt_block(b0, key_bytes[:8])
                s2 = des_decrypt_block(s1, key_bytes[8:16])

                st.markdown(f"""
                <div class="step-trace">
                    <div><span class="step">① Encrypt (K1)</span>  K1 = <span class="val">{k1}</span></div>
                    <div><span class="step">② Decrypt (K2)</span>  K2 = <span class="val">{k2}</span></div>
                    <div><span class="step">③ Encrypt (K3)</span>  K3 = <span class="val">{k3}</span></div>
                    {"<div><span class='step'>  Mode</span>  CBC chaining applied per block</div>" if block_mode=="CBC" else ""}
                    <div><span class="step">  Input blocks</span>  <span class="val">{len(padded)//8}</span> × 8 bytes (PKCS#7 padded)</div>
                    <div><span class="step">  Output</span>  <span class="val">{len(ciphertext)}</span> bytes → <span class="val">{len(output_hex)}</span> hex chars</div>
                </div>
                """, unsafe_allow_html=True)

                st.info("Copy the hex output above to decrypt later.")

            else:  # Decrypt
                ct_hex = user_input.strip().replace(" ", "")
                if not all(c in "0123456789abcdefABCDEF" for c in ct_hex):
                    st.error("Ciphertext must be a valid hex string.")
                elif len(ct_hex) % 16 != 0:
                    st.error("Ciphertext hex length must be a multiple of 16 (8 bytes per block).")
                else:
                    ciphertext = bytes.fromhex(ct_hex)
                    plaintext  = cipher.decrypt(ciphertext)
                    output_text = plaintext.decode("utf-8")

                    st.markdown("---")
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f'<span class="badge badge-blue">{key_mode.split()[0].upper()} KEY</span>', unsafe_allow_html=True)
                    c2.markdown(f'<span class="badge badge-green">{block_mode} MODE</span>', unsafe_allow_html=True)
                    c3.markdown(f'<span class="badge badge-red">DED DECRYPT</span>', unsafe_allow_html=True)

                    st.markdown('<div class="panel-label" style="margin-top:1rem">Plaintext</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="output-box">{output_text}</div>', unsafe_allow_html=True)

                    k1 = key_bytes[:8].hex()
                    k2 = key_bytes[8:16].hex()
                    k3 = (key_bytes[:8] if len(key_bytes)==16 else key_bytes[16:]).hex()
                    st.markdown(f"""
                    <div class="step-trace">
                        <div><span class="step">① Decrypt (K3)</span>  K3 = <span class="val">{k3}</span></div>
                        <div><span class="step">② Encrypt (K2)</span>  K2 = <span class="val">{k2}</span></div>
                        <div><span class="step">③ Decrypt (K1)</span>  K1 = <span class="val">{k1}</span></div>
                        {"<div><span class='step'>  Mode</span>  CBC chaining reversed per block</div>" if block_mode=="CBC" else ""}
                        <div><span class="step">  Input blocks</span>  <span class="val">{len(ciphertext)//8}</span> × 8 bytes</div>
                        <div><span class="step">  Output</span>  <span class="val">{len(plaintext)}</span> bytes (padding removed)</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as ex:
            st.error(f"Error: {ex}")

# ── Footer info ────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("ℹ  How this works"):
    st.markdown("""
**EDE (Encrypt–Decrypt–Encrypt)**
- **Step 1** — Encrypt plaintext block with K1 using DES
- **Step 2** — Decrypt result with K2 using DES  *(undoes step 1 if K1=K2)*
- **Step 3** — Encrypt result with K3 using DES

**Key modes**
- **3-key**: K1 ≠ K2 ≠ K3 → 168 bits of key material
- **2-key**: K1 = K3, K2 different → 112-bit effective security

**Backwards compatibility**: when K1 = K2 = K3, steps 1 & 2 cancel out, leaving plain single DES.

**Padding**: PKCS#7 — the final byte value tells you how many padding bytes were added.

**CBC mode**: each plaintext block is XOR'd with the previous ciphertext block before encryption, breaking patterns across blocks.
    """)
