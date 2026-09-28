import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import streamlit as st

import config
from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text

st.set_page_config(page_title="LegalEase", layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(config.WEB_LOGO_PATH):
        st.image(config.WEB_LOGO_PATH, use_container_width=True)
st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

for key, default in {"generated_text": "", "doc_type": "", "terms": "", "show_edit": False}.items():
    st.session_state.setdefault(key, default)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    if not document_type.strip() or not parties.strip():
        st.warning("Please enter at least the Document Type and Parties Involved.")
    else:
        try:
            with st.spinner("Generating your document..."):
                resp = requests.post(
                    f"{config.API_URL}/generate",
                    json={"document_type": document_type, "parties": parties, "terms": terms, "dates": dates},
                    timeout=180,
                )
            if resp.status_code == 200:
                st.session_state.generated_text = sanitize_text(resp.json()["document"])
                st.session_state.doc_type = document_type
                st.session_state.terms = terms
                st.session_state.show_edit = False
                st.session_state.pop("edit_area", None)
                st.success("Document Generated Successfully!")
            else:
                st.error(f"Backend error: {resp.json().get('detail', resp.text)}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the backend. Start it with: uvicorn legalEaseAPI.main:app --reload")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if not st.session_state.generated_text:
    st.info("Click 'Generate Document' to start")
else:
    def toggle_edit():
        st.session_state.show_edit = not st.session_state.show_edit

    st.button("\u270f\ufe0f Click to Edit Document", on_click=toggle_edit)
    if st.session_state.show_edit:
        edited = st.text_area("Edit Document Below:", value=st.session_state.generated_text,
                              height=300, key="edit_area")
        st.session_state.generated_text = edited

    text = st.session_state.generated_text
    doc_type, terms_saved = st.session_state.doc_type, st.session_state.terms
    styled = format_html_preview(text)
    st.markdown(
        "<div style='background:#0e1525;color:#e6e6e6;padding:16px;border-radius:10px;"
        f"max-height:420px;overflow-y:auto;'>{styled}</div>",
        unsafe_allow_html=True,
    )

    base = "".join(c if c.isalnum() else "_" for c in doc_type.lower()).strip("_") or "document"
    st.download_button("\U0001F4C4 Download as .TXT", data=text, file_name=f"{base}.txt", mime="text/plain")
    st.download_button(
        "\U0001F4DD Download as .DOCX", data=format_docx(text, doc_type, terms_saved), file_name=f"{base}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.download_button(
        "\U0001F4D5 Download as .PDF", data=format_pdf(text, doc_type, terms_saved), file_name=f"{base}.pdf",
        mime="application/pdf")
