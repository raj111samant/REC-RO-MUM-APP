import streamlit as st
import streamlit.components.v1 as components
from utils import Utils

@st.cache_data(show_spinner=False)
def DCRValidationCache(modSerNum):
    return Utils.ValidateDCR(modSerNum)

def ProcessUserInput(userInput):
    userInput = userInput.replace(" ", ",").replace(" ", "").replace("\r\n", ",").replace("\n", ",")
    seen = set()
    userInputList = [x for x in [y for y in userInput.split(",")] if not (x == "" or x in seen or seen.add((x,)))]
    resultList = [DCRValidationCache(modSerNum) for modSerNum in userInputList]
    resultMarkdownText = '''
| Serial Number | DCR Validation |
|----|----|
'''
    for result in resultList:
        if "DCR FOUND" in result[1]: color = "green"
        elif "DCR NOT-FOUND" in result[1]: color = "red"
        else: color = "orange"
        resultMarkdownText += f"| :{color}[{result[0]}] | :{color}[{result[1]}] |\n"
    return resultMarkdownText

def ApplyPageLayoutSettings():
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                footer {visibility: hidden;}
                .block-container {
                    padding-top: 2 rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                .element-container:has(iframe[height="0"]) {
                    display: none;
                }
                .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
                .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
                .viewerBadge_text__1JaDK {
                    display: none;
                }
        </style>""", unsafe_allow_html=True)

def WideSpaceDefault():
    st.set_page_config(layout="wide", page_title="DCRValidation App", page_icon="✅")

WideSpaceDefault()

def InitSessionState():
    if "FormSubmitter:DCRInputForm-Input" not in st.session_state.keys():
        st.session_state["FormSubmitter:DCRInputForm-Input"] = ""

def RenderForm():
    st.title("DCRValidation App")
    st.sidebar.success("Select a page above.")
    st.subheader("🚨 Note")
    st.markdown(
"""
This app verifies DCR for input Module Serial Number via solardcrportal.nise.res.in 🌐
User input should contain module serial number(s) separated by comma or newline or space.
Example:
* ```
  SerialNumber1,SerialNumber2,SerialNumber3
* ```
  SerialNumber1
  SerialNumber2
* ```
  SerialNumber1 SerialNumber2 SerialNumber3
""")

    st.subheader("✍ Input")
    with st.form('DCRInputForm'):
        inputColumn, buttonColumn = st.columns([6,1]) 
        with inputColumn:
            st.session_state["FormSubmitter:DCRInputForm-Input"] = st.text_area(
                "Comma seperated Module Serial Numbers", value=None,
                placeholder="Comma/Newline/Space seperated Module Serial Numbers", label_visibility='collapsed')
        with buttonColumn:
            _ = st.form_submit_button('Validate', use_container_width=True)

def RenderFormAction():
    userInput = st.session_state["FormSubmitter:DCRInputForm-Input"]
    st.subheader("🏆 Result")
    resultTableElem = st.empty()
    if (st.session_state["FormSubmitter:DCRInputForm-Validate"]) and (userInput not in ["", None]):
        resultTableElem.empty()
        with st.spinner("Processing user input..."):
            with Utils.Timer() as timer:
                resultMarkdownText = ProcessUserInput(userInput)
                resultTableElem.write(resultMarkdownText + "\n" + f"⏱ Time taken {timer.ElapsedTime():.6f} secs")

InitSessionState()
RenderForm()
ApplyPageLayoutSettings()
RenderFormAction()

# NSMP24091468370, NSMP24091468383, NSMP24091468381, 26240523C3284085, SE540240924065, WS08249037680588

#ToDo