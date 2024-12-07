import streamlit as st
from utils import Utils

prevUserInput = ""

def ProcessUserInput(userInput):
    global prevUserInput
    prevUserInput = userInput
    userInput = userInput.replace(" ", ",").replace(" ", "").replace("\r\n", ",").replace("\n", ",")
    seen = set()
    userInputList = [x for x in [y for y in userInput.split(",")] if not (x == "" or x in seen or seen.add((x,)))]
    resultList = [Utils.ValidateDCR(modSerNum) for modSerNum in userInputList]
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

def WideSpaceDefault():
    st.set_page_config(layout="wide", page_title="DCRValidation App", page_icon="✅")
    st.markdown(
        """
        <style>
        ._container_gzau3_1, ._viewerBadge_nim44_23, .st-emotion-cache-h4xjwg, ._profileContainer_gzau3_53 {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True)

WideSpaceDefault()

st.title("DCRValidation App")
st.sidebar.success("Select a page above.")
st.markdown("""---""")

st.header("🚨 Note")
st.markdown(
"""
This app verifies DCR for input Module Serial Number via solardcrportal.nise.res.in 🌐

User input should contain module serial number(s) separated by comma or newline.
Example:
* ```
  SerialNumber1,SerialNumber2,SerialNumber3
* ```
  SerialNumber1
  SerialNumber2
"""
)

st.markdown("""---""")
st.header("✍ Input")
with st.form('chat_input_form'):
    col1, col2 = st.columns([5,1]) 
    with col1:
        userInput = st.text_area(
            "Comma seperated Module Serial Numbers",
            value=None,
            placeholder="Comma/Newline seperated Module Serial Numbers",
            label_visibility='collapsed'
        )
    with col2:
        submitButtonPressed = st.form_submit_button('Validate')

st.markdown("""---""")
st.header("🏆 Result")

if (submitButtonPressed or (prevUserInput != userInput)) and (userInput not in ["", None]):
    with st.spinner("Processing user input..."):
        with Utils.Timer() as timer:
            resultMarkdownText = ProcessUserInput(userInput)
            st.write(resultMarkdownText + "\n" + f"⏱ Time taken {timer.ElapsedTime():.6f} secs")

ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
<p style='font-size: 0.875em;'>Made with <a style='display: inline; text-align: left;' href="https://streamlit.io/" target="_blank">Streamlit</a><br 'style= top:3px;'>
with <img src="https://em-content.zobj.net/source/skype/289/red-heart_2764-fe0f.png" alt="heart" height= "10"/><a style='display: inline; text-align: left;' href="https://github.com/sape94" target="_blank"> by sape94</a></p>
</div>

</div>
"""
st.write(ft, unsafe_allow_html=True)


# NSMP24091468370, NSMP24091468383, NSMP24091468381, 26240523C3284085, SE540240924065, WS08249037680588