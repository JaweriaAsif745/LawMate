# app/components/highlights.py
import streamlit as st
from typing import List, Dict
import html

SEVERITY_COLORS = {
    "high": "#ff4d4f",    # red
    "medium": "#fa8c16",  # orange
    "low": "#fadb14"      # yellow
}

def _render_badges(matches):
    # matches: list of {"severity":..., "keyword":...}
    if not matches:
        return ""
    badges = []
    seen = set()
    for m in matches:
        sev = m.get("severity", "low")
        kw = m.get("keyword", "")
        key = f"{sev}|{kw}"
        if key in seen:
            continue
        seen.add(key)
        color = SEVERITY_COLORS.get(sev, "#ddd")
        badges.append(f"<span style='display:inline-block;padding:4px 8px;margin:2px;border-radius:6px;"
                      f"background:{color};color:#111;font-weight:600;font-size:12px'>{html.escape(sev.upper())}</span>")
    return " ".join(badges)

def highlight_clauses(clause_results: List[Dict]):
    """
    clause_results: list of {"index", "clause", "matches", "is_risky"}
    Render each clause, highlight risk if present using badges and colored text.
    """
    for item in clause_results:
        clause = item.get("clause", "")
        idx = item.get("index", None)
        matches = item.get("matches", []) or []
        is_risky = item.get("is_risky", False)

        badges_html = _render_badges(matches)
        header = f"Clause {idx}" if idx is not None else "Clause"
        # render card-like block
        st.markdown("---")
        cols = st.columns([0.06, 0.94])
        with cols[0]:
            # small severity dot if risky
            if is_risky:
                st.markdown(f"<div style='width:14px;height:14px;border-radius:7px;background:{SEVERITY_COLORS.get(matches[0]['severity'],'#ff4d4f')};'></div>", unsafe_allow_html=True)
            else:
                st.markdown("", unsafe_allow_html=True)
        with cols[1]:
            # header + badges
            st.markdown(f"**{header}:** {html.escape(clause)}", unsafe_allow_html=True)
            if badges_html:
                st.markdown(badges_html, unsafe_allow_html=True)
            # show matched keywords detail (optional)
            if matches:
                detail_lines = []
                for m in matches:
                    detail_lines.append(f"- **{m['severity'].upper()}** — _{html.escape(m['keyword'])}_")
                st.markdown("<br>".join(detail_lines), unsafe_allow_html=True)
