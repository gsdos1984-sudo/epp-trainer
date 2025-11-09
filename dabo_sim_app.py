
# dabo_sim_app.py
import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="EPP Trainer • DABO Simulator", page_icon="🧠", layout="wide")

# ---------- Tiny theme for kid-simple UI ----------
st.markdown("""
<style>
  .big {font-size: 28px; font-weight: 900;}
  .hint {font-size: 16px; color:#2c3e50;}
  .panel {background:#0D3239; padding:16px; border-radius:14px; border:1px solid #1f5b66;}
  .title {color:#E9C341; font-weight:900; letter-spacing:1px;}
  .box {background:#0f3a42; padding:10px 14px; border-radius:10px; color:#ecf0f1; font-weight:800;}
  .kbtn {font-size:22px; font-weight:900;}
</style>
""", unsafe_allow_html=True)

# ---------- Navigation (simple) ----------
pages = {
    "HOME": "Home",
    "MOLD SETTING": "Mold Setting",
    "GLOSSARY": "Glossary"
}
sel = st.sidebar.radio("Go to", list(pages.values()))

# ---------- HOME ----------
if sel == "Home":
    st.markdown("<div class='title'><h1>Welcome • EPP Trainer</h1></div>", unsafe_allow_html=True)
    st.write("""
    **Goal:** Train people in any plant that uses **Expanded Polypropylene (EPP)** machines.

    **Language:** English. **Style:** very simple, like for a child.

    Click a big button. Change one number. See what happens.

    """)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➡️ Mold Setting", use_container_width=True):
            st.session_state["_nav"] = "Mold Setting"
    with c2:
        if st.button("ℹ️ Glossary", use_container_width=True):
            st.session_state["_nav"] = "Glossary"
    with c3:
        st.download_button("Download Sample Recipe", data=json.dumps({
            "pv_mm": 0.0,
            "settings": {"cracking_mm": 8.0, "close_slow_mm": 20.0, "open_slow_mm": 15.0, "open_stop1_mm": 60.0, "a2a_close_mm": 2.0, "a2a_open_mm": 8.0},
            "notes": {"A":"Use 6–10 mm for small parts", "B":"Close slow to protect edges"},
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }, indent=2), file_name="sample_recipe.json", mime="application/json")

    st.markdown("""
    ---
    ### Three golden rules (super simple)
    1) **One change at a time.**

    2) **Small steps.** Move by little numbers.

    3) **See – Think – Save.** Look at the result, learn, save the recipe.
    """)

# ---------- MOLD SETTING (imports the same logic as the standalone file) ----------
if sel == "Mold Setting" or st.session_state.get("_nav") == "Mold Setting":
    st.session_state["_nav"] = "Mold Setting"
    st.markdown("<div class='title'><h2>Mold Setting</h2></div>", unsafe_allow_html=True)

    # Lazy embed: reuse code inline (keeps project single-file for Streamlit Cloud)
    DEFAULTS = {
        "cracking_mm": 8.0,
        "close_slow_mm": 20.0,
        "open_slow_mm": 15.0,
        "open_stop1_mm": 60.0,
        "a2a_close_mm": 2.0,
        "a2a_open_mm": 8.0,
        "pv_mm": 0.0,
        "notes": {"A":"","B":"","C":"","D":"","F":"","G":""},
        "hydraulic_log": []
    }
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

    def log(msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        st.session_state.hydraulic_log.insert(0, f"[{ts}] {msg}")

    # Simple kid tips
    with st.expander("Kid tip 👶: What is PV?"):
        st.write("**PV** means **Process Value**. It is what the machine feels now. PV is live.")

    # PV big box
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"<div class='box'>PV: <span style='font-size:28px;font-weight:900'>{st.session_state['pv_mm']:.1f} mm</span></div>", unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2.2, 1.2])
    with left:
        st.subheader("Process Name & Setting (mm)")
        rows = [
            ("A.", "CRACKING", "cracking_mm"),
            ("B.", "MOLD CLOSE SLOW", "close_slow_mm"),
            ("C.", "MOLD OPEN SLOW", "open_slow_mm"),
            ("D.", "MOLD OPEN STOP 1", "open_stop1_mm"),
            ("F.", "A2A CLOSE", "a2a_close_mm"),
            ("G.", "A2A OPEN", "a2a_open_mm"),
        ]
        for code, name, key in rows:
            cA, cB = st.columns([.6, .4])
            with cA:
                st.write(f"**{code} {name}**")
            with cB:
                val = st.number_input(
    f"{name} (mm)",
    value=float(st.session_state[key]),
    step=0.5, min_value=0.0, max_value=300.0,
    key=key,                     # el widget maneja st.session_state[key]
    label_visibility="collapsed"
)

            st.text_area(f"Note {code}", key=f"note_{code}", value=st.session_state['notes'].get(code, ""), height=60, label_visibility="collapsed", placeholder="Write a short tip…")

        cS, cL = st.columns(2)
        with cS:
            if st.button("Save Notes"):
                for code in ["A","B","C","D","F","G"]:
                    st.session_state['notes'][code] = st.session_state.get(f"note_{code}", "")
                st.success("Notes saved")
        with cL:
            recipe = {
                "pv_mm": st.session_state["pv_mm"],
                "settings": {k: st.session_state[k] for k in ["cracking_mm","close_slow_mm","open_slow_mm","open_stop1_mm","a2a_close_mm","a2a_open_mm"]},
                "notes": st.session_state["notes"],
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
            st.download_button("Download Recipe (JSON)", data=json.dumps(recipe, indent=2), file_name="mold_setting_recipe.json", mime="application/json")

    with right:
        st.subheader("Hydraulic")
        if st.button("MOLD CLOSE", use_container_width=True):
            st.session_state["pv_mm"] = max(0.0, st.session_state["pv_mm"] - 5)
            log("Mold Close")
        if st.button("MOLD OPEN", use_container_width=True):
            st.session_state["pv_mm"] = min(300.0, st.session_state["pv_mm"] + 5)
            log("Mold Open")
        st.button("HIGH", use_container_width=True)
        st.button("PRESSURE RELEASE", use_container_width=True)
        st.button("CLAMP CYL' FOR'", use_container_width=True)
        st.button("CLAMP CYL' REV'", use_container_width=True)
        st.button("CLAMP SLIDE REV'", use_container_width=True)

        st.caption("Action Log")
        st.code("\n".join(st.session_state["hydraulic_log"][:25]))

    st.divider()
    st.info("Try: change **CRACKING** a little. Press **MOLD OPEN**. Watch PV move. Save recipe.")

# ---------- GLOSSARY ----------
if sel == "Glossary" or st.session_state.get("_nav") == "Glossary":
    st.session_state["_nav"] = "Glossary"
    st.markdown("<div class='title'><h2>Glossary (Very Simple)</h2></div>", unsafe_allow_html=True)
    items = {
        "PV (Process Value)": "What the machine has now (live reading).",
        "SV (Set Value)": "Your target number. What you want.",
        "Cracking": "A small open of the mold to help steam/air and easy eject.",
        "A2A": "Air-to-Air gap (open/close distance).",
        "Mold Open Stop 1": "First stop position when opening.",
    }
    for k, v in items.items():
        st.markdown(f"**{k}** — {v}")
