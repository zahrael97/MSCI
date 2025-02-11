import streamlit as st
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
        st.session_state.page = "Landing"

    # Check URL query parameters for navigation
    query_params = st.query_params
    if "page" in query_params and query_params["page"] == "Landing":
        st.session_state.page = "Landing"

    with st.sidebar:
        if logo_image:
            # Create a clickable image that redirects to Landing page
            st.markdown(f"""
            <p align="center">
                <a href="?page=Landing">
                    <img src="data:image/png;base64,{logo_image}" alt="logo" width="300" height="300">
                </a>
            </p>
            """, unsafe_allow_html=True)

        st.header("MSCI")
        option = st.radio("Choose an option", ("Peptide Twins Analysis", "Peptide Twins Checker"))

    # Handle navigation
    if st.session_state.page == "Landing":
        landing_page()
    elif option == "Peptide Twins Analysis":
        peptide_twins_analysis()
        plot_spectra()
    elif option == "Peptide Twins Checker":
        peptide_twins_checker()

if __name__ == "__main__":
    main()
