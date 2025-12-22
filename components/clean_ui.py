import streamlit as st

def clean_streamlit_ui():
    st.markdown(
        """
        <style>
        /* ===== 1. Diệt toolbar trên cùng (Deploy, ⋮) ===== */
        [data-testid="stAppToolbar"] {
            display: none !important;
            height: 0 !important;
        }

        /* ===== 2. Diệt toàn bộ header wrapper ===== */
        header {
            display: none !important;
            height: 0 !important;
        }

        /* ===== 3. Diệt sidebar hoàn toàn ===== */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* ===== 4. Diệt mấy element trang trí linh tinh ===== */
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stToolbarActions"] {
            display: none !important;
        }

        /* ===== 5. Kéo nội dung lên sát top ===== */
        .block-container {
            padding-top: 0.5rem !important;
        }

        /* ===== 6. Xóa margin top body ===== */
        body {
            margin-top: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
