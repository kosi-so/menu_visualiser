from pathlib import Path
from tempfile import NamedTemporaryFile
import streamlit as st
from src.app.pipeline import full_menu_pipeline


# ────────────────────────────────  Page config
st.set_page_config(page_title="Menu-Visualiser", layout="wide")
st.title("📋 → 🍽️  Menu-Visualiser")


# ────────────────────────────────  File uploader
uploaded = st.file_uploader(
    "Upload a menu image or PDF",
    type=["png", "jpg", "jpeg", "pdf"],
    help="Max ~20 MB. PNG/JPEG works best; PDFs will process the first page."
)

if uploaded:
    # Persist the upload to a temp file because the pipeline expects a file path
    suffix = Path(uploaded.name).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        tmp_path = Path(tmp.name)

    # Run the full pipeline (OCR ➜ grouping ➜ image generation)
    with st.spinner("Extracting menu & generating previews…"):
        result = full_menu_pipeline(tmp_path)

    menu_items = result["menu"]      # list[dict] (name, price, desc…)
    generated = result["images"]     # list[str] (URLs or local paths)

    # ────────────────────────────────  Layout
    col_raw, col_gen = st.columns([1, 2])

    # Left: original upload
    with col_raw:
        st.subheader("Original menu")
        if suffix == ".pdf":
            st.write("PDF uploaded – open to view:")
            st.page_link(tmp_path.as_uri(), label="Open PDF in new tab")
        else:
            st.image(uploaded, use_container_width=True)

    # Right: generated dishes
    with col_gen:
        st.subheader("AI-generated dish photos")
        if not generated:
            st.info("No images returned.")
        else:
            # Display in a neat 3-column grid
            n_cols = 3
            rows = (len(generated) + n_cols - 1) // n_cols
            for r in range(rows):
                cols = st.columns(n_cols)
                for c in range(n_cols):
                    idx = r * n_cols + c
                    if idx >= len(generated):
                        break
                    item = menu_items[idx] if idx < len(menu_items) else {}
                    with cols[c]:
                        st.image(generated[idx], use_container_width=True)
                        st.markdown(f"**{item.get('name','Unnamed')}**")
                        if desc := item.get("description") or item.get("desc"):
                            st.caption(desc)

    # Optional: expandable JSON blob
    with st.expander("🗂️  Structured menu JSON"):
        st.json(menu_items)

    # Clean-up temp file on server restart; on Streamlit Cloud it’s auto-purged
