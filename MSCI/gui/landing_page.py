import streamlit as st
from pathlib import Path
import base64
import requests

# Import custom modules
try:
    from MSCI.gui.utils import load_image_from_url, add_custom_css
    from MSCI.gui.landing_page import landing_page
    from MSCI.gui.peptide_analysis import peptide_twins_analysis, plot_spectra
    from MSCI.gui.peptide_checker import peptide_twins_checker
except ImportError as e:
    st.error(f"Import Error: {e}")

# Function to handle missing logo image
def get_logo_image():
    logo_url = "https://github.com/proteomicsunitcrg/MSCI/raw/main/docs/MSCI_logor.png"
    try:
        logo_image = load_image_from_url(logo_url)
        return logo_image
    except Exception as e:
        st.warning(f"Could not load logo image: {e}")
        return None

# Main function for Streamlit app
def main():
    st.set_page_config(layout="wide")
    
    # Apply custom CSS if available
    try:
        add_custom_css()
    except Exception as e:
        st.warning(f"CSS not applied: {e}")

    # Load and display logo in sidebar
    with st.sidebar:
        logo_image = get_logo_image()
        if logo_image:
            st.markdown(f"""
            <p align="center">
                <img src="data:image/png;base64,{logo_image}" alt="logo" width="300" height="300">
            </p>
            """, unsafe_allow_html=True)
        st.header("MSCI")
        option = st.radio("Choose an option", ("MSCI", "Peptide Twins Analysis", "Peptide Twins Checker"))

    # Handle different options
    if option == "MSCI":
        st.write("### Debug: MSCI page selected")  # Debugging message
        try:
            landing_page()
        except Exception as e:
            st.error(f"Error loading MSCI page: {e}")

    elif option == "Peptide Twins Analysis":
        try:
            peptide_twins_analysis()
            plot_spectra()
        except Exception as e:
            st.error(f"Error in Peptide Twins Analysis: {e}")

    elif option == "Peptide Twins Checker":
        try:
            peptide_twins_checker()
        except Exception as e:
            st.error(f"Error in Peptide Twins Checker: {e}")

if __name__ == "__main__":
    main()
