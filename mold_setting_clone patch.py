
# mold_setting_clone.py (patched keys)
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="DABO Simulator • Mold Setting (Clone)", page_icon="🧩", layout="wide")

PRIMARY_BG = "#103C43"
PANEL_BG   = "#0E353B"
ACCENT_YEL = "#F3C83E"
ACCENT_RED = "#E64E43"
TEXT_WHITE = "#EAF7FA"

st.markdown(f"""
<style>
  .main {{ background:{PRIMARY_BG}; }}
  .block-container {{ padding-top: 0.8rem; padding-bottom: 0.8rem; }}
  .topbar {{ display:flex; gap:12px; align-items:center; }}
  .btn-red {{ background:{ACCENT_RED}; color:white; border:none; border-radius:8px; padding:.55rem 1rem; font-weight:900; letter-spacing:.3px; }}
  .titlebar {{ flex:1; background:{PANEL_BG}; border:1px solid #1f5b66; border-radius:8px; text-align:center; padding:.5rem 1rem; }}
  .titlebar h1 {{ color:{ACCENT_YEL}; margin:0; font-size:28px; letter-spacing:1px; font-weight:900 }}
  .pv-row {{ display:flex; align-items:center; justify-content:center; gap:10px; margin-top:.6rem; }}
  .pv-label {{ color:{ACCENT_YEL}; font-weight:900; font-size:20px; }}
  .pv-value {{ min-width:180px; text-align:center; background:#0a2025; color:white; border:2px solid #102e35; border-radius:6px; padding:.6rem 1rem; font-weight:900; font-size:22px; }}
  .pv-suf {{ color:{ACCENT_YEL}; font-weight:900; font-size:16px; }}
  .panel {{ background:{PANEL_BG}; border:1px solid #1f5b66; border-radius:12px; padding:12px; }}
  .panel-title {{ background:{ACCENT_YEL}; color:#122; font-weight:900; border-radius:8px; padding:.35rem .6rem; display:inline-block; letter-spacing:.6px; }}
  .panel-title.right {{ display:block; text-align:center; }}
  .tbl-head {{ display:grid; grid-template-columns: 1.2fr 1.2fr .6fr; gap:10px; margin-top:8px; margin-bottom:6px; }}
  .tbl-head span {{ color:{ACCENT_YEL}; font-weight:900; }}
  .procname {{ color:{TEXT_WHITE}; font-weight:900; letter-spacing:.3px; }}
  .note-btn {{ background:{ACCENT_YEL}; color:#222; font-weight:900; border:none; border-radius:6px; padding:.45rem .6rem; width:100%; cursor:pointer; }}
  .input-wrap > div > input {{ background:#2e646f !important; color:white !important; border:1px solid #1f5b66 !important; font-weight:800; }}
</style>
""", unsafe_allow_html=True)

DEFAULTS = {"pv_mm":0.0,"A":8.0,"B":20.0,"C":15.0,"D":60.0,"F":2.0,"G":8.0}
for k,v in DEFAULTS.items():
    st.session_state.setdefault(k,v)

def bump_pv(delta: float):
    st.session_state["pv_mm"] = max(0.0, min(300.0, st.session_state["pv_mm"] + delta))

t1, t2, t3 = st.columns([.9, 1, 6])
with t1:
    st.markdown('<div class="topbar"><button class="btn-red">MENU</button></div>', unsafe_allow_html=True)
with t2:
    st.markdown('<div class="topbar"><button class="btn-red">OPERATION</button></div>', unsafe_allow_html=True)
with t3:
    st.markdown('<div class="titlebar"><h1>MOLD SETTING</h1></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pv-row"><span class="pv-label">PV</span>'
                f'<span class="pv-value">{st.session_state["pv_mm"]:.2f}</span>'
                f'<span class="pv-suf">mm</span></div>', unsafe_allow_html=True)

st.divider()

left, right = st.columns([2.3, 1.2], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="tbl-head"><span>PROCESS NAME</span><span>SETTING</span><span style="text-align:center;">&nbsp;</span></div>', unsafe_allow_html=True)

    rows = [("A.  CRACKING","A"),("B.  MOLD CLOSE SLOW","B"),("C.  MOLD OPEN SLOW","C"),
            ("D.  MOLD OPEN STOP 1","D"),("F.  A2A CLOSE","F"),("G.  A2A OPEN","G")]

    for label, key in rows:
        c1, c2, c3 = st.columns([1.2, 1.2, .6])
        with c1:
            st.markdown(f'<div class="procname">{label}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
            st.number_input(" ", key=key, value=float(st.session_state[key]), step=0.5, min_value=0.0, max_value=300.0, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<button class="note-btn">NOTE</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title right">HYDRAULIC</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("MOLD CLOSE", key="btn_close", use_container_width=True):
            bump_pv(-5.0)
    with c2:
        if st.button("MOLD OPEN", key="btn_open", use_container_width=True):
            bump_pv(+5.0)
    c3, c4 = st.columns(2, gap="small")
    with c3:
        st.button("HIGH", key="btn_high", use_container_width=True)
    with c4:
        st.button("PRESSURE RELEASE", key="btn_pr", use_container_width=True)
    c5, c6 = st.columns(2, gap="small")
    with c5:
        st.button("CLAMP CYL' FOR'", key="btn_cyl_for", use_container_width=True)
    with c6:
        st.button("CLAMP CYL' REV'", key="btn_cyl_rev", use_container_width=True)
    c7, c8 = st.columns(2, gap="small")
    with c7:
        st.button("CLAMP SLIDE REV'", key="btn_slide_rev_left", use_container_width=True)
    with c8:
        st.button("CLAMP SLIDE REV'", key="btn_slide_rev_right", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Pixel-style clone of the DABO 'Mold Setting' screen. Set main file to: mold_setting_clone.py")
