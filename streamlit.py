import streamlit as st
from pathlib import Path
import base64
import requests
from MSCI.gui.utils import load_image_from_url, add_custom_css
from MSCI.gui.landing_page import landing_page
from MSCI.gui.peptide_analysis import peptide_twins_analysis, plot_spectra
from MSCI.gui.peptide_checker import peptide_twins_checker

def main():
    st.set_page_config(layout="wide")
    add_custom_css()

    # URL of the image on GitHub
    logo_url = "https://github.com/proteomicsunitcrg/MSCI/raw/main/docs/MSCI_logor.png"
    logo_image = load_image_from_url(logo_url)

    # Initialize session state for navigation
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    def go_to_landing():
        st.session_state.page = "landing"
        st.rerun()  # Refresh Streamlit to reflect changes

    with st.sidebar:
        if logo_image:
            logo_html = f"""
            <p align="center">
                <a href="#" onclick="window.location.reload();">
                    <img src="data:image/png;base64,{logo_image}" alt="logo" width="300" height="300">
                </a>
            </p>
            """
            st.markdown(logo_html, unsafe_allow_html=True)

        st.header("MSCI")
        option = st.radio("Choose an option", ("", "Peptide Twins Analysis", "Peptide Twins Checker"), index=0)

    # Navigate based on user choice
    if option == "" or st.session_state.page == "landing":
        landing_page()
    elif option == "Peptide Twins Analysis":
        peptide_twins_analysis()
        plot_spectra()
    elif option == "Peptide Twins Checker":
        peptide_twins_checker()

if __name__ == "__main__":
    main()
