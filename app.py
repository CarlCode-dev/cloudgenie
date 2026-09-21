import json
import streamlit as st
import pandas as pd
import random
import datetime
import textwrap
import google.generativeai as genai
import streamlit.components.v1 as components

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="CloudGenie", page_icon="☁️", layout="wide")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #0F1B33 0%, #0A0F1E 45%, #060910 100%);
    background-size: 200% 200%;
    animation: bgShift 15s ease infinite;
}
@keyframes bgShift {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

[data-testid="stSidebar"] {
    background: rgba(13, 21, 38, 0.55);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(56, 225, 255, 0.15);
}

[data-testid="stFormSubmitButton"] button {
    white-space: nowrap;
}

.sidebar-logo {
    font-size: 22px;
    font-weight: 700;
    color: #E6F1FF;
    padding: 8px 4px 24px 4px;
    animation: floaty 3s ease-in-out infinite;
}
.sidebar-logo span { color: #38E1FF; text-shadow: 0 0 14px rgba(56,225,255,0.5); }
@keyframes floaty {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
}

.sidebar-section-label {
    color: #5C6B85;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 20px 0 6px 4px;
}

[data-testid="stSidebar"] .stButton>button {
    width: 100%;
    text-align: left;
    background: transparent; !important;
    color: #FFFFFF; !important;
    border: none;
    border-left: 2px solid transparent;
    border-radius: 6px;
    padding: 8px 12px 8px 38px;
    font-weight: 400;
    font-size: 14px;
    margin-bottom: 2px;
    box-shadow: none;
    position: relative;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stSidebar"] .stButton>button::before {
    content: "";
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%) scale(1);
    width: 16px;
    height: 16px;
    background-color: #FFFFFF;
    mask-size: contain;
    mask-repeat: no-repeat;
    mask-position: center;
    -webkit-mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    -webkit-mask-position: center;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(56,225,255,0.05);
    color: #C7D6E8;
    border-left: 2px solid rgba(56,225,255,0.3);
    transform: translateX(3px);
    box-shadow: none;
}
[data-testid="stSidebar"] .stButton>button:hover::before {
    background-color: #38E1FF;
    transform: translateY(-50%) scale(1.1);
}

[data-testid="stSidebar"] .stButton>button[kind="primary"] {
    background: rgba(56,225,255,0.07);
    color: #38E1FF;
    border-left: 2px solid #38E1FF;
    border-radius: 6px;
    font-weight: 600;
    box-shadow: none;
    animation: navSlideIn 0.3s ease;
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]::before {
    background-color: #38E1FF;
    filter: drop-shadow(0 0 4px rgba(56,225,255,0.6));
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover {
    transform: none;
    background: rgba(56,225,255,0.1);
}
@keyframes navSlideIn {
    from { border-left-width: 0px; background: rgba(56,225,255,0); }
    to { border-left-width: 2px; background: rgba(56,225,255,0.07); }
}

.st-key-nav_About-Me button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNCIvPjxwYXRoIGQ9Ik00IDIwYzAtNCAzLjUtNiA4LTZzOCAyIDggNiIvPjwvc3ZnPg=="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNCIvPjxwYXRoIGQ9Ik00IDIwYzAtNCAzLjUtNiA4LTZzOCAyIDggNiIvPjwvc3ZnPg=="); }

.st-key-nav_Dashboard button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxyZWN0IHg9IjMiIHk9IjMiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMTQiIHk9IjMiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMyIgeT0iMTQiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMTQiIHk9IjE0IiB3aWR0aD0iNyIgaGVpZ2h0PSI3IiByeD0iMSIvPjwvc3ZnPg=="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxyZWN0IHg9IjMiIHk9IjMiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMTQiIHk9IjMiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMyIgeT0iMTQiIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHJ4PSIxIi8+PHJlY3QgeD0iMTQiIHk9IjE0IiB3aWR0aD0iNyIgaGVpZ2h0PSI3IiByeD0iMSIvPjwvc3ZnPg=="); }

.st-key-nav_Monitoring button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5bGluZSBwb2ludHM9IjIyIDEyIDE4IDEyIDE1IDIxIDkgMyA2IDEyIDIgMTIiLz48L3N2Zz4="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5bGluZSBwb2ludHM9IjIyIDEyIDE4IDEyIDE1IDIxIDkgMyA2IDEyIDIgMTIiLz48L3N2Zz4="); }

.st-key-nav_Incidents button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMC4yOSAzLjg2IDEuODIgMThhMiAyIDAgMCAwIDEuNzEgM2gxNi45NGEyIDIgMCAwIDAgMS43MS0zTDEzLjcxIDMuODZhMiAyIDAgMCAwLTMuNDIgMFoiLz48bGluZSB4MT0iMTIiIHkxPSI5IiB4Mj0iMTIiIHkyPSIxMyIvPjxsaW5lIHgxPSIxMiIgeTE9IjE3IiB4Mj0iMTIuMDEiIHkyPSIxNyIvPjwvc3ZnPg=="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMC4yOSAzLjg2IDEuODIgMThhMiAyIDAgMCAwIDEuNzEgM2gxNi45NGEyIDIgMCAwIDAgMS43MS0zTDEzLjcxIDMuODZhMiAyIDAgMCAwLTMuNDIgMFoiLz48bGluZSB4MT0iMTIiIHkxPSI5IiB4Mj0iMTIiIHkyPSIxMyIvPjxsaW5lIHgxPSIxMiIgeTE9IjE3IiB4Mj0iMTIuMDEiIHkyPSIxNyIvPjwvc3ZnPg=="); }

.st-key-nav_Status button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0yMiAxMS4wOFYxMmExMCAxMCAwIDEgMS01LjkzLTkuMTQiLz48cG9seWxpbmUgcG9pbnRzPSIyMiA0IDEyIDE0LjAxIDkgMTEuMDEiLz48L3N2Zz4="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0yMiAxMS4wOFYxMmExMCAxMCAwIDEgMS01LjkzLTkuMTQiLz48cG9seWxpbmUgcG9pbnRzPSIyMiA0IDEyIDE0LjAxIDkgMTEuMDEiLz48L3N2Zz4="); }

.st-key-nav_Architecture button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5Z29uIHBvaW50cz0iMTIgMiAyIDcgMTIgMTIgMjIgNyAxMiAyIi8+PHBvbHlsaW5lIHBvaW50cz0iMiAxNyAxMiAyMiAyMiAxNyIvPjxwb2x5bGluZSBwb2ludHM9IjIgMTIgMTIgMTcgMjIgMTIiLz48L3N2Zz4="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwb2x5Z29uIHBvaW50cz0iMTIgMiAyIDcgMTIgMTIgMjIgNyAxMiAyIi8+PHBvbHlsaW5lIHBvaW50cz0iMiAxNyAxMiAyMiAyMiAxNyIvPjxwb2x5bGluZSBwb2ludHM9IjIgMTIgMTIgMTcgMjIgMTIiLz48L3N2Zz4="); }

.st-key-nav_Live-Deployments button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PGxpbmUgeDE9IjIiIHkxPSIxMiIgeDI9IjIyIiB5Mj0iMTIiLz48cGF0aCBkPSJNMTIgMmExNS4zIDE1LjMgMCAwIDEgNCAxMCAxNS4zIDE1LjMgMCAwIDEtNCAxMCAxNS4zIDE1LjMgMCAwIDEtNC0xMCAxNS4zIDE1LjMgMCAwIDEgNC0xMHoiLz48L3N2Zz4="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PGxpbmUgeDE9IjIiIHkxPSIxMiIgeDI9IjIyIiB5Mj0iMTIiLz48cGF0aCBkPSJNMTIgMmExNS4zIDE1LjMgMCAwIDEgNCAxMCAxNS4zIDE1LjMgMCAwIDEtNCAxMCAxNS4zIDE1LjMgMCAwIDEtNC0xMCAxNS4zIDE1LjMgMCAwIDEgNC0xMHoiLz48L3N2Zz4="); }

.st-key-nav_SecOps-Auditor button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMiAyIDMgNnY2YzAgNSA0IDguNSA5IDEwIDUtMS41IDktNSA5LTEwVjZ6Ii8+PHBhdGggZD0ibTkgMTIgMiAyIDQtNCIvPjwvc3ZnPg=="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMiAyIDMgNnY2YzAgNSA0IDguNSA5IDEwIDUtMS41IDktNSA5LTEwVjZ6Ii8+PHBhdGggZD0ibTkgMTIgMiAyIDQtNCIvPjwvc3ZnPg=="); }

.st-key-nav_FinOps-Optimizer button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjkiLz48cGF0aCBkPSJNMTIgN3YxME0xNSA5LjVjMC0xLjQtMS4zLTIuNS0zLTIuNXMtMyAxLjEtMyAyLjNjMCAzLjIgNiAxLjYgNiA0LjcgMCAxLjQtMS4zIDIuNS0zIDIuNXMtMy0xLjEtMy0yLjUiLz48L3N2Zz4="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjkiLz48cGF0aCBkPSJNMTIgN3YxME0xNSA5LjVjMC0xLjQtMS4zLTIuNS0zLTIuNXMtMyAxLjEtMyAyLjNjMCAzLjIgNiAxLjYgNiA0LjcgMCAxLjQtMS4zIDIuNS0zIDIuNXMtMy0xLjEtMy0yLjUiLz48L3N2Zz4="); }

.st-key-nav_Runbooks button::before { mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik00IDE5LjVBMi41IDIuNSAwIDAgMSA2LjUgMTdIMjAiLz48cGF0aCBkPSJNNi41IDJIMjB2MjBINi41QTIuNSAyLjUgMCAwIDEgNCAxOS41di0xNUEyLjUgMi41IDAgMCAxIDYuNSAyWiIvPjwvc3ZnPg=="); -webkit-mask-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik00IDE5LjVBMi41IDIuNSAwIDAgMSA2LjUgMTdIMjAiLz48cGF0aCBkPSJNNi41IDJIMjB2MjBINi41QTIuNSAyLjUgMCAwIDEgNCAxOS41di0xNUEyLjUgMi41IDAgMCAxIDYuNSAyWiIvPjwvc3ZnPg=="); }

.sidebar-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px;
    margin-top: 24px;
    border-radius: 14px;
    background: rgba(56,225,255,0.05);
    border: 1px solid rgba(56,225,255,0.12);
}
.sidebar-footer .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1B8FD1, #38E1FF);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: #06121F;
}
.sidebar-footer .name { color: #E6F1FF; font-weight: 600; font-size: 14px; }
.sidebar-footer .link { color: #38E1FF; font-size: 12px; text-decoration: none; }

.hero { animation: fadeInUp 0.7s ease both; padding: 40px 0 20px 0; }
.hero h1 {
    font-size: 42px;
    background: linear-gradient(90deg, #E6F1FF, #38E1FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.hero p { color: #9FB3CC; font-size: 16px; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.card-grid { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 24px; }
.card {
    flex: 1; min-width: 220px;
    background: linear-gradient(145deg, rgba(56,225,255,0.06), rgba(17,26,46,0.9));
    border: 1px solid rgba(56, 225, 255, 0.18);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    animation: fadeInUp 0.7s ease both, cardGlow 4s ease-in-out infinite;
}
@keyframes cardGlow {
    0%, 100% { box-shadow: 0 8px 30px rgba(0,0,0,0.35), 0 0 0px rgba(56,225,255,0); }
    50% { box-shadow: 0 8px 30px rgba(0,0,0,0.35), 0 0 20px rgba(56,225,255,0.25); }
}
.card .label { color: #9FB3CC; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
.card .value { color: #E6F1FF; font-size: 32px; font-weight: 700; margin-top: 6px; }
.card .glow { color: #38E1FF; text-shadow: 0 0 14px rgba(56,225,255,0.5); }

.risk-card { background: #0F1830; border-left: 4px solid; border-radius: 10px; padding: 16px 20px; margin-bottom: 12px; animation: fadeInUp 0.5s ease both; }
.risk-high { border-color: #FF5C6C; }
.risk-med { border-color: #FFB020; }
.risk-low { border-color: #38E1FF; }

[data-testid="stAppViewContainer"] .stButton>button {
    background: linear-gradient(90deg, #1B8FD1, #38E1FF);
    color: #06121F;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.55em 1.6em;
}
[data-testid="stAppViewContainer"] .stButton>button:hover {
    box-shadow: 0 0 24px rgba(56, 225, 255, 0.55);
    transform: translateY(-2px);
}

[data-testid="stFileUploaderDropzone"] {
    background: #0D1526;
    border: 2px dashed rgba(56, 225, 255, 0.3);
    border-radius: 14px;
}

.incident-card {
    background: #0F1830;
    border-left: 4px solid;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: fadeInUp 0.5s ease both;
}
.incident-open { border-color: #FF5C6C; }
.incident-resolved { border-color: #38E1FF; opacity: 0.7; }
.badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-open { background: rgba(255,92,108,0.15); color: #FF5C6C; }
.badge-resolved { background: rgba(56,225,255,0.15); color: #38E1FF; }

.st-key-floating_chat_btn {
    position: fixed;
    bottom: 54px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    width: fit-content;
}
.st-key-floating_chat_btn button {
    background: linear-gradient(90deg, #B14EFF, #FF6EC7) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 28px !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px rgba(177,78,255,0.4), 0 0 20px rgba(255,110,199,0.3) !important;
    transition: all 0.25s ease !important;
}
.st-key-floating_chat_btn button:hover {
    box-shadow: 0 0 30px rgba(177,78,255,0.6), 0 0 30px rgba(255,110,199,0.5) !important;
    transform: translateY(-2px);
}

.st-key-chat_panel_container {
    position: fixed;
    bottom: 100px;
    right: 24px;
    width: 380px;
    max-height: 65vh;
    z-index: 9998;
    background: rgba(15, 20, 35, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(177,78,255,0.3);
    border-radius: 18px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    padding: 16px;
    display: flex;
    flex-direction: column;
}

.chat-messages-scroll {
    max-height: 320px;
    overflow-y: auto;
    padding-right: 4px;
    margin-bottom: 10px;
}
.chat-messages-scroll::-webkit-scrollbar { width: 6px; }
.chat-messages-scroll::-webkit-scrollbar-thumb {
    background: rgba(177,78,255,0.4);
    border-radius: 10px;
}

.chat-bubble-user {
    background: linear-gradient(90deg, #1B8FD1, #38E1FF);
    color: #06121F;
    border-radius: 14px 14px 4px 14px;
    padding: 10px 14px;
    margin: 6px 0;
    max-width: 85%;
    width: fit-content;
    margin-left: auto;
    font-size: 14px;
    font-weight: 500;
    animation: fadeInUp 0.4s ease both;
}
.chat-bubble-ai {
    background: linear-gradient(90deg, #B14EFF, #FF6EC7);
    color: white;
    border-radius: 14px 14px 14px 4px;
    padding: 10px 14px;
    margin: 6px 0;
    max-width: 85%;
    width: fit-content;
    align-self: flex-start;
    font-size: 14px;
    animation: fadeInUp 0.4s ease both;
}
.chat-container { display: flex; flex-direction: column; }

.st-key-close_chat_btn button {
    background: linear-gradient(90deg, #1B8FD1, #38E1FF) !important;
    color: #06121F !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

#chat-drag-handle:active {
    cursor: grabbing;
}

</style>
""", unsafe_allow_html=True)

components.html("""
<div id="particle-mount"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {
    const doc = window.parent.document;

    let canvas = doc.getElementById('particle-canvas');
    if (canvas) canvas.remove();
    canvas = doc.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '0';
    canvas.style.pointerEvents = 'none';
    doc.body.appendChild(canvas);

    const THREE = window.parent.THREE || window.THREE;

    function makeGlowTexture() {
        const size = 64;
        const c = doc.createElement('canvas');
        c.width = size; c.height = size;
        const ctx = c.getContext('2d');
        const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
        grad.addColorStop(0, 'rgba(255,255,255,1)');
        grad.addColorStop(0.15, 'rgba(255,255,255,0.7)');
        grad.addColorStop(0.5, 'rgba(255,255,255,0.2)');
        grad.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, size, size);
        return new THREE.CanvasTexture(c);
    }
    const glowTexture = makeGlowTexture();

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.parent.innerWidth / window.parent.innerHeight, 0.1, 1000);
    camera.position.z = 50;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.parent.innerWidth, window.parent.innerHeight);
    renderer.setPixelRatio(window.parent.devicePixelRatio || 1);

    const particleCount = 110;
    const positions = new Float32Array(particleCount * 3);
    const originalPositions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const baseColors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    const twinklePhase = new Float32Array(particleCount);
    const twinkleSpeed = new Float32Array(particleCount);
    const brightness = new Float32Array(particleCount);

    const cyan = new THREE.Color(0x38E1FF);
    const white = new THREE.Color(0xFFFFFF);

    for (let i = 0; i < particleCount; i++) {
        const edgeBias = Math.random() < 0.7;
        let x, y;
        if (edgeBias) {
            const angle = Math.random() * Math.PI * 2;
            const radius = 35 + Math.random() * 25;
            x = Math.cos(angle) * radius;
            y = Math.sin(angle) * radius * 0.6;
        } else {
            x = (Math.random() - 0.5) * 100;
            y = (Math.random() - 0.5) * 60;
        }
        const z = (Math.random() - 0.5) * 60;
        positions[i*3] = x; positions[i*3+1] = y; positions[i*3+2] = z;
        originalPositions[i*3] = x; originalPositions[i*3+1] = y; originalPositions[i*3+2] = z;

        const c = Math.random() > 0.6 ? white : cyan;
        baseColors[i*3] = c.r; baseColors[i*3+1] = c.g; baseColors[i*3+2] = c.b;
        colors[i*3] = c.r; colors[i*3+1] = c.g; colors[i*3+2] = c.b;

        const isStandout = Math.random() < 0.12;
        sizes[i] = isStandout ? (Math.random() * 1 + 2.2) : (Math.random() * 1 + 0.6);
        brightness[i] = isStandout ? 1.0 : (Math.random() * 0.4 + 0.25);

        twinklePhase[i] = Math.random() * Math.PI * 2;
        twinkleSpeed[i] = Math.random() * 0.015 + 0.008;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
        size: 3.5,
        map: glowTexture,
        vertexColors: true,
        transparent: true,
        opacity: 1,
        sizeAttenuation: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });

    const points = new THREE.Points(geometry, material);
    scene.add(points);

    const maxLines = particleCount * 3;
    const linePositions = new Float32Array(maxLines * 2 * 3);
    const lineColors = new Float32Array(maxLines * 2 * 3);
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));
    lineGeometry.setDrawRange(0, 0);
    const lineMaterial = new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.12,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const lineSegments = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lineSegments);

    let mouseX = 0, mouseY = 0;
    let targetMouseWorld = new THREE.Vector3(0, 0, 0);

    doc.addEventListener('mousemove', function(e) {
        mouseX = (e.clientX / window.parent.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.parent.innerHeight) * 2 + 1;
    });

    function onResize() {
        camera.aspect = window.parent.innerWidth / window.parent.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.parent.innerWidth, window.parent.innerHeight);
    }
    window.parent.addEventListener('resize', onResize);

    const currentX = new Float32Array(particleCount);
    const currentY = new Float32Array(particleCount);
    const currentZ = new Float32Array(particleCount);
    for (let i = 0; i < particleCount; i++) {
        currentX[i] = originalPositions[i*3];
        currentY[i] = originalPositions[i*3+1];
        currentZ[i] = originalPositions[i*3+2];
    }

    let time = 0;
    function animate() {
        time += 0.003;

        const vector = new THREE.Vector3(mouseX, mouseY, 0.5);
        vector.unproject(camera);
        const dir = vector.sub(camera.position).normalize();
        const distance = -camera.position.z / dir.z;
        targetMouseWorld = camera.position.clone().add(dir.multiplyScalar(distance));

        const posAttr = geometry.attributes.position;
        const colorAttr = geometry.attributes.color;

        for (let i = 0; i < particleCount; i++) {
            const depthFactor = 0.5 + ((originalPositions[i*3+2] + 30) / 60) * 0.5;

            const ox = originalPositions[i*3] + Math.sin(time * depthFactor + i) * 1.5;
            const oy = originalPositions[i*3+1] + Math.cos(time * 1.2 * depthFactor + i) * 1.5;
            const oz = originalPositions[i*3+2];

            const dx = ox - targetMouseWorld.x;
            const dy = oy - targetMouseWorld.y;
            const dist = Math.sqrt(dx*dx + dy*dy);

            let px = ox, py = oy;
            const repelRadius = 15;
            if (dist < repelRadius) {
                const force = (1 - dist / repelRadius) * 8;
                px = ox + (dx / (dist || 1)) * force;
                py = oy + (dy / (dist || 1)) * force;
            }

            currentX[i] += (px - currentX[i]) * 0.1;
            currentY[i] += (py - currentY[i]) * 0.1;
            currentZ[i] = oz;

            posAttr.array[i*3] = currentX[i];
            posAttr.array[i*3+1] = currentY[i];
            posAttr.array[i*3+2] = currentZ[i];

            const distFromCenter = Math.sqrt(ox*ox + oy*oy) / 45;
            const centerFade = Math.min(1, Math.max(0.15, distFromCenter));
            const twinkle = 0.6 + 0.4 * Math.sin(time * 40 * twinkleSpeed[i] * 20 + twinklePhase[i]);
            const finalBrightness = brightness[i] * centerFade * twinkle;

            colorAttr.array[i*3] = baseColors[i*3] * finalBrightness;
            colorAttr.array[i*3+1] = baseColors[i*3+1] * finalBrightness;
            colorAttr.array[i*3+2] = baseColors[i*3+2] * finalBrightness;
        }
        posAttr.needsUpdate = true;
        colorAttr.needsUpdate = true;

        let lineIdx = 0;
        const connectDist = 13;
        for (let i = 0; i < particleCount && lineIdx < maxLines; i++) {
            for (let j = i + 1; j < particleCount && lineIdx < maxLines; j++) {
                const dx = currentX[i] - currentX[j];
                const dy = currentY[i] - currentY[j];
                const dz = currentZ[i] - currentZ[j];
                const d = Math.sqrt(dx*dx + dy*dy + dz*dz);
                if (d < connectDist) {
                    const base = lineIdx * 6;
                    linePositions[base] = currentX[i]; linePositions[base+1] = currentY[i]; linePositions[base+2] = currentZ[i];
                    linePositions[base+3] = currentX[j]; linePositions[base+4] = currentY[j]; linePositions[base+5] = currentZ[j];
                    const cbase = lineIdx * 6;
                    lineColors[cbase] = 0.22; lineColors[cbase+1] = 0.88; lineColors[cbase+2] = 1.0;
                    lineColors[cbase+3] = 0.22; lineColors[cbase+4] = 0.88; lineColors[cbase+5] = 1.0;
                    lineIdx++;
                }
            }
        }
        lineGeometry.attributes.position.needsUpdate = true;
        lineGeometry.attributes.color.needsUpdate = true;
        lineGeometry.setDrawRange(0, lineIdx * 2);

        camera.position.x += (mouseX * 5 - camera.position.x) * 0.02;
        camera.position.y += (mouseY * 5 - camera.position.y) * 0.02;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
        window.parent.requestAnimationFrame(animate);
    }
    animate();
})();
</script>
""", height=0)

if "page" not in st.session_state:
    st.session_state.page = "About Me"

if "page" not in st.session_state:
    st.session_state.page = "About Me"

nav_groups = [
    (None, [("About Me", "👤")]),
    ("Overview", [
        ("Dashboard", "📊"),
        ("Monitoring", "📈"),
        ("Incidents", "🚨"),
        ("Status", "✅"),
        ("Architecture", "🧩"),
        ("Live Deployments", "🌐"),

    ]),
    ("AI Tools", [
        ("SecOps Auditor", "🛡️"),
        ("FinOps Optimizer", "💰"),
        ("Runbooks", "📖"),
    ]),
]

st.sidebar.markdown("<div class='sidebar-logo'>☁️ <span>CloudGenie</span></div>", unsafe_allow_html=True)

for section_label, items in nav_groups:
    if section_label:
        st.sidebar.markdown(f'<div class="sidebar-section-label">{section_label}</div>', unsafe_allow_html=True)
    for label, icon in items:
        is_active = st.session_state.page == label
        with st.sidebar.container(key=f"nav_{label}"):
            if st.button(f"  {label}", key=f"navbtn_{label}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.page = label

st.sidebar.markdown("""
<div class="sidebar-footer">
    <div class="avatar">CD</div>
    <div>
        <div class="name">Carlito Dignos</div>
        <a class="link" href="https://github.com/CarlCode-dev" target="_blank">github.com/CarlCode-dev</a>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.show_chat:
    with st.container(key="chat_panel_container"):
        header_col1, header_col2 = st.columns([5, 1])
        with header_col1:
            st.markdown('<div id="chat-drag-handle" style="cursor:move; font-weight:700;">💬 Ask CloudGenie</div>', unsafe_allow_html=True)
        with header_col2:
            with st.container(key="close_chat_btn"):
                closed = st.button("✕")

        if len(st.session_state.chat_history) == 0:
            st.info("👋 I'm specialized in cloud engineering, DevOps, security, and cost optimization topics only.")

        chat_html = '<div class="chat-messages-scroll"><div class="chat-container">'
        for msg in st.session_state.chat_history:
            css_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            chat_html += f'<div class="{css_class}">{msg["content"]}</div>'
        chat_html += '</div></div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        with st.form(key="chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([4, 1])
            with col_input:
                user_question = st.text_input("Type your question...", label_visibility="collapsed")
            with col_send:
                submitted = st.form_submit_button("Send")

        if submitted and user_question.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.spinner("Thinking..."):
                chat_prompt = f"""You are CloudGenie, a friendly AI assistant specialized in cloud engineering, DevOps, security operations, and cost optimization. Answer clearly and concisely (2-4 sentences unless more detail is genuinely needed). If the question is unrelated to cloud/DevOps/tech topics, politely redirect the user back to cloud-related topics instead of answering.

User question: {user_question}
"""
                try:
                    response = model.generate_content(chat_prompt)
                    answer = response.text.strip()
                except Exception as e:
                    answer = "⏳ Rate limit reached — please wait about 30-60 seconds and try again."
            st.session_state.chat_history.append({"role": "ai", "content": answer})
            st.rerun()

        if closed:
            st.session_state.show_chat = False
            st.rerun()


# --- Runbooks ---
elif page == "Runbooks":
    st.markdown("<div class='hero'><h1>Runbook Generator</h1><p>AI-generated incident response runbooks.</p></div>", unsafe_allow_html=True)

    common_incidents = [
        "Database connection timeout",
        "High memory usage",
        "Failed deployment rollback",
        "SSL certificate expiration",
        "API rate limit exceeded",
        "Disk space exhaustion",
        "Custom (type your own)"
    ]

    selected = st.selectbox("Select an incident type", common_incidents)

    if selected == "Custom (type your own)":
        incident_type = st.text_input("Describe the incident type")
    else:
        incident_type = selected

    if st.button("📖 Generate Runbook") and incident_type.strip():
        with st.spinner("Generating runbook..."):
            runbook_prompt = f"""You are a senior SRE creating an incident response runbook for a team's internal documentation. Create a structured runbook for this incident type: "{incident_type}"

Return ONLY a valid JSON object with this exact structure (no markdown, no extra text):
{{
  "title": "runbook title",
  "severity": "High/Medium/Low",
  "detection": "how this incident is typically detected",
  "steps": ["step 1", "step 2", "step 3", "..."],
  "prevention": "brief note on preventing recurrence"
}}
"""
            try:
                response = model.generate_content(runbook_prompt)
                raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
                st.session_state.runbook_data = json.loads(raw_text)
            except Exception as e:
                st.session_state.runbook_data = None
                st.warning("⏳ Rate limit reached or couldn't parse response — please wait 30-60 seconds and try again.")

    if st.session_state.get("runbook_data") is not None:
        rb = st.session_state.runbook_data
        severity_color = {"High": "risk-high", "Medium": "risk-med", "Low": "risk-low"}.get(rb.get("severity", "Medium"), "risk-med")

        steps_html = "".join([f"<li style='margin-bottom:8px;'>{step}</li>" for step in rb.get("steps", [])])

        runbook_html = f"""
<div class="risk-card {severity_color}" style="padding:24px;">
<h3 style="margin-top:0; color:#E6F1FF;">{rb.get('title','')}</h3>
<p><b>Severity:</b> {rb.get('severity','')}</p>
<p><b>Detection:</b> {rb.get('detection','')}</p>
<p><b>Response Steps:</b></p>
<ol style="color:#9FB3CC;">{steps_html}</ol>
<p><b>Prevention:</b> <span style="color:#9FB3CC;">{rb.get('prevention','')}</span></p>
</div>
"""
        st.markdown(runbook_html, unsafe_allow_html=True)

with st.container(key="floating_chat_btn"):
    if st.button("💬 Ask CloudGenie"):
        st.session_state.show_chat = not st.session_state.show_chat
        st.rerun()


# --- About Me ---
if page == "About Me":
    st.markdown("""
    <div class="hero">
        <h1>Hi, I'm Carl 👋</h1>
        <p>3rd-year BSIT student building toward a Cloud Engineer/Architecture career. CloudGenie is my hands-on portfolio project — a working cloud operations platform with real AI integration, combining security auditing, cost optimization, live monitoring, incident response, and an AI assistant into one deployed app.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Skills I'm building:** Cloud fundamentals · Python · UI/UX design · Security auditing · Cost optimization · AI API integration · Git/GitHub deployment")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("What this project demonstrates")

    st.markdown("""
    <div class="card-grid">
        <div class="card"><div class="label">📊 Dashboard</div><div style="color:#9FB3CC; margin-top:8px;">At-a-glance overview of overall security score and savings found.</div></div>
        <div class="card"><div class="label">📈 Monitoring</div><div style="color:#9FB3CC; margin-top:8px;">Live simulated system health metrics — CPU, memory, and network throughput.</div></div>
        <div class="card"><div class="label">🚨 Incidents</div><div style="color:#9FB3CC; margin-top:8px;">Auto-logged incident timeline triggered by monitoring thresholds.</div></div>
        <div class="card"><div class="label">✅ Status</div><div style="color:#9FB3CC; margin-top:8px;">Public-facing system status page reflecting live incident state.</div></div>
        <div class="card"><div class="label">🧩 Architecture</div><div style="color:#9FB3CC; margin-top:8px;">Visual system architecture diagram showing how the platform is structured.</div></div>
        <div class="card"><div class="label">🌐 Live Deployments</div><div style="color:#9FB3CC; margin-top:8px;">Showcase of real cloud infrastructure projects deployed on AWS, GCP, or Azure.</div></div>
        <div class="card"><div class="label">🛡️ SecOps Auditor</div><div style="color:#9FB3CC; margin-top:8px;">Real AI analysis of uploaded files for security risks, with AI-generated fixes.</div></div>
        <div class="card"><div class="label">💰 FinOps Optimizer</div><div style="color:#9FB3CC; margin-top:8px;">Real AI-generated cost-saving recommendations, with a 6-month cost trend chart.</div></div>
        <div class="card"><div class="label">📖 Runbooks</div><div style="color:#9FB3CC; margin-top:8px;">AI-generated incident response runbooks for common outage scenarios.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("💬 Also available on every page: **Ask CloudGenie**, a floating AI assistant for cloud and DevOps questions.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("Built end-to-end: coded in Python, integrated with Google's Gemini API for real AI analysis, version-controlled with Git/GitHub, and deployed live on Streamlit Community Cloud — a full working deployment pipeline, not just a design mockup.")

    st.info("All AI-powered features (SecOps, FinOps, Ask CloudGenie, Runbooks) use real, live Gemini API responses. Some supporting data within CloudGenie itself — like the 6-month billing history and live system metrics — is simulated by design. The Live Deployments page, however, links to genuinely real, separately-hosted cloud infrastructure projects.")

# --- Dashboard ---
elif page == "Dashboard":
    st.markdown("<div class='hero'><h1>Dashboard</h1><p>Welcome to CloudGenie — your AI-powered cloud engineering portfolio.</p></div>", unsafe_allow_html=True)

    secops_findings = st.session_state.get("secops_findings")
    if secops_findings is not None:
        score = 100
        for f in secops_findings:
            risk = f.get("risk", "Low")
            score -= {"High": 20, "Medium": 10, "Low": 5}.get(risk, 5)
        score = max(score, 0)
        security_value = f"{score}/100"
    else:
        security_value = "Run a scan first"

    finops_recs = st.session_state.get("finops_recommendations")
    if finops_recs is not None:
        total = 0
        for r in finops_recs:
            digits = "".join(c for c in r.get("estimated_savings", "") if c.isdigit())
            if digits:
                total += int(digits)
        savings_value = f"${total}/month" if total > 0 else "No savings found"
    else:
        savings_value = "Run FinOps analysis first"

    st.markdown(f"""
    <div class="card-grid">
        <div class="card"><div class="label">Security Score</div><div class="value glow">{security_value}</div></div>
        <div class="card"><div class="label">Monthly Savings Found</div><div class="value glow">{savings_value}</div></div>
    </div>
    """, unsafe_allow_html=True)

# --- Monitoring ---
elif page == "Monitoring":
    st.markdown("<div class='hero'><h1>Monitoring</h1><p>Live system health metrics (simulated).</p></div>", unsafe_allow_html=True)

    if "metrics_history" not in st.session_state:
        st.session_state.metrics_history = pd.DataFrame({
            "Time": [], "CPU (%)": [], "Memory (%)": [], "Network (Mbps)": []
        })

    if st.button("🔄 Refresh Metrics"):
        new_row = pd.DataFrame({
            "Time": [datetime.datetime.now().strftime("%H:%M:%S")],
            "CPU (%)": [random.randint(20, 95)],
            "Memory (%)": [random.randint(30, 90)],
            "Network (Mbps)": [random.randint(10, 500)],
        })
        st.session_state.metrics_history = pd.concat(
            [st.session_state.metrics_history, new_row], ignore_index=True
        ).tail(20)

    if len(st.session_state.metrics_history) == 0:
        st.info("Click 'Refresh Metrics' to start monitoring.")
    else:
        latest = st.session_state.metrics_history.iloc[-1]
        st.markdown(f"""
        <div class="card-grid">
            <div class="card"><div class="label">CPU Usage</div><div class="value glow">{latest['CPU (%)']}%</div></div>
            <div class="card"><div class="label">Memory Usage</div><div class="value glow">{latest['Memory (%)']}%</div></div>
            <div class="card"><div class="label">Network Throughput</div><div class="value glow">{latest['Network (Mbps)']} Mbps</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        chart_df = st.session_state.metrics_history.set_index("Time")
        st.line_chart(chart_df)

        if latest["CPU (%)"] > 85:
            st.warning("⚠️ High CPU usage detected — potential scaling event.")
            if "incidents" not in st.session_state:
                st.session_state.incidents = []
            already_logged = any(
                inc["time"] == latest["Time"] for inc in st.session_state.incidents
            )
            if not already_logged:
                st.session_state.incidents.append({
                    "time": latest["Time"],
                    "description": f"High CPU usage detected ({latest['CPU (%)']}%)",
                    "status": "Open"
                })

# --- Incidents ---
elif page == "Incidents":
    st.markdown("<div class='hero'><h1>Incident Timeline</h1><p>Auto-logged incidents from live monitoring.</p></div>", unsafe_allow_html=True)

    if "incidents" not in st.session_state:
        st.session_state.incidents = []

    if len(st.session_state.incidents) == 0:
        st.info("No incidents logged yet. Trigger high CPU usage on the Monitoring page to generate one.")
    else:
        for i, incident in enumerate(reversed(st.session_state.incidents)):
            real_index = len(st.session_state.incidents) - 1 - i
            status_class = "incident-open" if incident["status"] == "Open" else "incident-resolved"
            badge_class = "badge-open" if incident["status"] == "Open" else "badge-resolved"

            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="incident-card {status_class}">
                    <div>
                        <b>{incident['description']}</b><br>
                        <span style="color:#9FB3CC; font-size:13px;">{incident['time']}</span>
                    </div>
                    <span class="badge {badge_class}">{incident['status']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if incident["status"] == "Open":
                    if st.button("Resolve", key=f"resolve_{real_index}"):
                        st.session_state.incidents[real_index]["status"] = "Resolved"
                        st.rerun()

# --- Status ---
elif page == "Status":
    st.markdown("<div class='hero'><h1>System Status</h1><p>Live operational status overview.</p></div>", unsafe_allow_html=True)

    open_incidents = [i for i in st.session_state.get("incidents", []) if i["status"] == "Open"]
    overall_status = "🟠 Degraded Performance" if open_incidents else "🟢 All Systems Operational"

    st.markdown(f"""
    <div class="card-grid">
        <div class="card" style="flex:2;">
            <div class="label">Overall Status</div>
            <div class="value glow">{overall_status}</div>
        </div>
        <div class="card">
            <div class="label">Open Incidents</div>
            <div class="value glow">{len(open_incidents)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Components")

    status_components = [
        ("SecOps Auditor", "Operational"),
        ("FinOps Optimizer", "Operational"),
        ("Monitoring Engine", "Degraded" if open_incidents else "Operational"),
        ("Incident Tracker", "Operational"),
    ]
    for name, status in status_components:
        badge_class = "badge-resolved" if status == "Operational" else "badge-open"
        dot = "🟢" if status == "Operational" else "🟠"
        st.markdown(f"""
        <div class="incident-card incident-resolved">
            <div>{dot} <b>{name}</b></div>
            <span class="badge {badge_class}">{status}</span>
        </div>
        """, unsafe_allow_html=True)

    if open_incidents:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Active Incidents")
        for inc in open_incidents:
            st.markdown(f"""
            <div class="incident-card incident-open">
                <div><b>{inc['description']}</b><br><span style="color:#9FB3CC; font-size:13px;">{inc['time']}</span></div>
                <span class="badge badge-open">Open</span>
            </div>
            """, unsafe_allow_html=True)

# --- Architecture ---
elif page == "Architecture":
    st.markdown("<div class='hero'><h1>Architecture</h1><p>How CloudGenie's fictional system is structured.</p></div>", unsafe_allow_html=True)

    svg_code = """<div class="card" style="padding:30px;">
<svg viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
<path d="M0,0 L0,6 L9,3 z" fill="#38E1FF"/>
</marker>
<filter id="glow">
<feGaussianBlur stdDeviation="3" result="blur"/>
<feMerge>
<feMergeNode in="blur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>
<line x1="450" y1="90" x2="450" y2="150" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="450" y1="210" x2="250" y2="280" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="450" y1="210" x2="650" y2="280" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="250" y1="340" x2="440" y2="410" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="650" y1="340" x2="460" y2="410" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<rect x="360" y="30" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="65" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Users / CDN</text>
<rect x="360" y="150" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="185" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Load Balancer</text>
<rect x="160" y="280" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="250" y="315" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Web Server 1</text>
<rect x="560" y="280" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="650" y="315" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Web Server 2</text>
<rect x="360" y="410" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="445" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Database</text>
</svg>
</div>"""
    st.markdown(svg_code, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Users / CDN**")
        st.caption("Entry point for traffic; caches static content close to users for speed.")
    with col2:
        st.markdown("**Load Balancer**")
        st.caption("Distributes incoming requests evenly across available web servers.")
    with col3:
        st.markdown("**Web Servers**")
        st.caption("Run the application logic; multiple instances allow redundancy and scaling.")
    with col4:
        st.markdown("**Database**")
        st.caption("Stores and retrieves persistent application data.")

# --- Live Deployments ---
elif page == "Live Deployments":
    st.markdown("<div class='hero'><h1>Live Deployments</h1><p>Real cloud infrastructure projects I've built and deployed.</p></div>", unsafe_allow_html=True)

    deployments = [
        {
            "name": "Example: Static Portfolio Site",
            "provider": "AWS",
            "description": "A simple static website hosted using S3 bucket static website hosting.",
            "services": "S3, (optional: CloudFront, Route 53)",
            "link": None
        },
    ]

    for d in deployments:
        link_html = f'<a href="{d["link"]}" target="_blank" style="color:#38E1FF; text-decoration:none; font-weight:600;">Visit live project →</a>' if d["link"] else '<span style="color:#5C6B85; font-size:13px;">Not deployed yet</span>'

        card_html = f"""
<div class="card" style="margin-bottom:16px; max-width:100%;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div class="label">{d['name']}</div>
<span style="background:rgba(56,225,255,0.1); color:#38E1FF; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700;">{d['provider']}</span>
</div>
<div style="color:#9FB3CC; margin-top:10px; font-size:14px;">{d['description']}</div>
<div style="color:#5C6B85; margin-top:6px; font-size:12px;"><b>Services used:</b> {d['services']}</div>
<div style="margin-top:12px;">{link_html}</div>
</div>
"""
        st.markdown(card_html, unsafe_allow_html=True)

    st.info("🚧 This is a placeholder example. More real deployments will be added here as I build and ship them on AWS, GCP, and Azure.")        

# --- SecOps Auditor ---
elif page == "SecOps Auditor":
    st.markdown("<div class='hero'><h1>SecOps Auditor</h1><p>Upload a config or log file to scan for vulnerabilities.</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a file for AI security analysis", type=["txt", "json", "log"])

    if uploaded_file is not None:
        st.write(f"File received: **{uploaded_file.name}**")
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")

        if st.button("🔍 Scan with AI"):
            with st.spinner("Analyzing file for security risks..."):
                prompt = f"""This is a classroom exercise for a student's cloud security course. Below is a made-up, non-functional example configuration (all values are placeholders, not real credentials or systems). Your task is purely educational: identify which configuration PATTERNS would be considered risky in a real system, for teaching purposes. Do not repeat literal values back — describe the pattern category only (e.g. "hardcoded weak password" not the actual string).
Return ONLY a valid JSON array (no markdown, no extra text) where each item has this exact structure:
{{"risk": "High" or "Medium" or "Low", "title": "short title", "description": "1-2 sentence explanation and recommendation"}}

If there are no notable risks, return an empty array: []

File content:
{file_content[:4000]}
"""
                try:
                    response = model.generate_content(prompt)
                    raw_text = response.text.strip()
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                    st.session_state.secops_findings = json.loads(raw_text)
                except Exception as e:
                    st.session_state.secops_findings = None
                    st.error("Couldn't parse AI response. Raw output shown below.")
                    st.code(response.text if 'response' in dir() else str(e))

        if st.session_state.get("secops_findings") is not None:
            findings = st.session_state.secops_findings
            if len(findings) == 0:
                st.success("✅ No significant risks detected in this file.")
            else:
                risk_class_map = {"High": "risk-high", "Medium": "risk-med", "Low": "risk-low"}
                risk_emoji_map = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
                for idx, finding in enumerate(findings):
                    risk = finding.get("risk", "Low")
                    css_class = risk_class_map.get(risk, "risk-low")
                    emoji = risk_emoji_map.get(risk, "🟢")
                    card_html = f"""
<div class="risk-card {css_class}">{emoji} <b>{risk.upper()} RISK</b> — {finding.get('title','')}<br><span style="color:#9FB3CC;">{finding.get('description','')}</span></div>
"""
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button("🛠️ Fix with AI", key=f"fix_{idx}"):
                        with st.spinner("Generating fix..."):
                            fix_prompt = f"""You are a cloud infrastructure engineer. Given this security risk, provide a specific fix as a Terraform resource block or AWS CLI command (whichever is more appropriate). Return ONLY the code, no explanation, no markdown code fences.

Risk: {finding.get('title','')}
Details: {finding.get('description','')}
"""
                            try:
                                fix_response = model.generate_content(fix_prompt)
                                fix_code = fix_response.text.strip().replace("```hcl", "").replace("```bash", "").replace("```", "").strip()
                                st.code(fix_code, language="hcl")
                            except Exception as e:
                                st.warning("⏳ Rate limit reached — please wait about 30-60 seconds and click 'Fix with AI' again.")                   

                    Details: {finding.get('description','')}
    else:
        st.caption("No file uploaded yet.")

# --- FinOps Optimizer ---
elif page == "FinOps Optimizer":
    st.markdown("<div class='hero'><h1>FinOps Optimizer</h1><p>Analyze cloud billing to find savings opportunities.</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("6-Month Cost Trend")
    st.caption("Monthly cloud spend before optimization recommendations were applied.")

    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    monthly_cost = [1450, 1580, 1390, 1240, 1180, 1020]

    trend_df = pd.DataFrame({
        "Month": months,
        "Cloud Spend ($)": monthly_cost
    })
    st.line_chart(trend_df.set_index("Month"))

    total_saved = monthly_cost[0] - monthly_cost[-1]
    pct_saved = round((total_saved / monthly_cost[0]) * 100, 1)
    st.success(f"📉 Spend down **{pct_saved}%** since April — roughly **${total_saved}/month** saved through ongoing optimization.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("AI Cost Optimization Recommendations")

    mock_billing_data = """
Monthly Cloud Billing Summary (September):
- EC2 instance web-prod-02: running 24/7 at m5.xlarge, average CPU utilization 8%
- RDS database db-main: db.r5.2xlarge, average connections 12, storage 500GB (200GB used)
- S3 bucket 'old-backups-2023': 800GB, no access in 90+ days, no lifecycle policy
- Elastic IP allocated but unattached: 3 addresses
- EBS volumes: 5 unattached volumes totaling 200GB
Total monthly spend: $1,020
"""

    if st.button("💡 Get AI Recommendations"):
        with st.spinner("Analyzing billing data for cost savings..."):
            prompt = f"""You are a FinOps cost optimization specialist. Analyze this mock cloud billing data and identify specific cost-saving opportunities.

Return ONLY a valid JSON array (no markdown, no extra text) where each item has this exact structure:
{{"title": "short title", "description": "1-2 sentence explanation of the issue and fix", "estimated_savings": "$XX/month"}}

Billing data:
{mock_billing_data}
"""
            try:
                response = model.generate_content(prompt)
                raw_text = response.text.strip()
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                st.session_state.finops_recommendations = json.loads(raw_text)
            except Exception as e:
                st.session_state.finops_recommendations = None
                st.error("Couldn't parse AI response. Raw output shown below.")
                st.code(response.text if 'response' in dir() else str(e))

    if st.session_state.get("finops_recommendations") is not None:
        recommendations = st.session_state.finops_recommendations
        if len(recommendations) == 0:
            st.info("No additional optimization opportunities found.")
        else:
            cards_html = '<div class="card-grid">'
            for rec in recommendations:
                cards_html += f"""
<div class="card">
<div class="label">{rec.get('title','')}</div>
<div class="value glow" style="font-size:22px;">{rec.get('estimated_savings','')}</div>
<div style="color:#9FB3CC; margin-top:8px; font-size:14px;">{rec.get('description','')}</div>
</div>
"""
            cards_html += '</div>'
            st.markdown(cards_html, unsafe_allow_html=True)

components.html("""
<script>
(function() {
    const doc = window.parent.document;
    console.log("DRAG SCRIPT LOADED");
    let isDragging = false;
    let offsetX = 0, offsetY = 0;

    doc.addEventListener('mousedown', function(e) {
        const handle = e.target.closest('#chat-drag-handle');
        if (!handle) return;

        const panel = doc.querySelector('.st-key-chat_panel_container');
        if (!panel) return;

        isDragging = true;
        const rect = panel.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;

        panel.style.right = 'auto';
        panel.style.bottom = 'auto';
        panel.style.left = rect.left + 'px';
        panel.style.top = rect.top + 'px';

        e.preventDefault();
    });

    doc.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        const panel = doc.querySelector('.st-key-chat_panel_container');
        if (!panel) return;

        let newX = e.clientX - offsetX;
        let newY = e.clientY - offsetY;

        newX = Math.max(0, Math.min(newX, window.parent.innerWidth - panel.offsetWidth));
        newY = Math.max(0, Math.min(newY, window.parent.innerHeight - panel.offsetHeight));

        panel.style.left = newX + 'px';
        panel.style.top = newY + 'px';
    });

    doc.addEventListener('mouseup', function() {
        isDragging = false;
    });
})();
</script>
""", height=0)