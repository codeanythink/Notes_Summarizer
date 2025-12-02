import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Prevents Windows Crash

import streamlit as st
import time
from pathlib import Path

from src import config, file_loader, ocr_pipeline, summarizer_extractive, utils

st.set_page_config(page_title="AI Notes Summarizer", page_icon="📚")    #streamlit page initiation
st.markdown("<style>.stTextArea textarea {font-size: 16px !important;}</style>", unsafe_allow_html=True)
st.title("📚 AI Lecture Notes Summarizer")


# This acts as the app's "Long-term Memory"
if 'source_data' not in st.session_state:
    st.session_state.source_data = None
if 'file_hash' not in st.session_state:
    st.session_state.file_hash = None

with st.sidebar:   #sidebar
    st.header("⚙️ Settings")
    summary_length = st.slider("Summary Length", 3, 20, 5)
    st.info(f"Model: {config.EMBEDDING_MODEL_NAME}")

    if st.session_state.source_data:    #saves session data
        st.success(f"Loaded: {st.session_state.source_data['metadata']['source']}")
    else:
        st.warning("No data loaded.")

tab1, tab2 = st.tabs(["📂 Upload File", "📝 Paste Text"])

with tab1:
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if uploaded_file:  #hash calculates
        current_hash = utils.get_content_hash(uploaded_file.name + str(uploaded_file.size))

        if st.session_state.file_hash != current_hash:
            file_path = utils.save_uploaded_file(uploaded_file)

            try:
                with st.spinner("📖 Reading file..."):
                    if file_path.endswith(".pdf"):
                        data = file_loader.read_pdf(file_path)
                    else:
                        data = file_loader.read_text_file(file_path)

                    st.session_state.source_data = data
                    st.session_state.file_hash = current_hash
                    st.rerun()  # Force refresh to show data immediately

            except file_loader.ScannedPDFError:
                st.warning("Scanned PDF detected! OCR Required.")
                try:
                    with st.spinner("⏳ Running OCR (30-60s)..."):
                        ocr_path = ocr_pipeline.ocr_pdf(file_path)
                        data = file_loader.read_pdf(ocr_path)

                        st.session_state.source_data = data
                        st.session_state.file_hash = current_hash
                        st.rerun()
                except Exception as e:
                    st.error(f"OCR Failed: {e}")
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    with st.form("paste_form"):
        pasted_text = st.text_area("Paste content:", height=200)
        submitted = st.form_submit_button("Process Text")

        if submitted and pasted_text.strip():
            try:
                data = file_loader.load_from_string(pasted_text)

                st.session_state.source_data = data
                st.session_state.file_hash = "paste_" + str(hash(pasted_text))
                st.success("Text Processed! You can now generate a summary.")
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.source_data:
    st.divider()
    data = st.session_state.source_data

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Source:** {data['metadata']['source']}")
    with col2:
        st.write(f"**Length:** {len(data['text'])} chars")

    with st.expander("👁️ View Source Text"):
        st.text_area("Content", data['text'], height=150)

    if st.button("✨ Generate Summary", type="primary"):

        progress = st.progress(0)
        status = st.empty()

        try:
            start_time = time.time()

            status.text("⏳ Initializing AI...")
            progress.progress(10)
            time.sleep(0.5)  # Small visual delay

            status.text("🧠 Analyzing semantics...")
            progress.progress(50)

            result = summarizer_extractive.summarize(
                data['text'],
                top_n=summary_length
            )

            progress.progress(100)
            status.empty()

            st.success(f"Done in {time.time() - start_time:.2f}s")

            st.subheader("📝 Summary")
            st.markdown(f"**{result['summary_text']}**")

            out_name = "summary.txt"
            st.download_button("📥 Download", result['summary_text'], out_name)

        except Exception as e:
            progress.empty()
            st.error(f"Failed: {e}")