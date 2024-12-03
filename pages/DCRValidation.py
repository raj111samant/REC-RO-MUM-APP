import streamlit as st
import urllib.request
from time import perf_counter as time_perf_counter

prevUserInput = ""

def ValidateDCR(modSrNum):
    url = f'https://solardcrportal.nise.res.in/VerifyDCR/PnlNumberO?PnlNumber={modSrNum}'
    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        response = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8')
    except Exception as e:
        response = "DCRValidationRequestError"

    if "ItemTransId" in response: response = "DCR FOUND"
    elif "DCRValidationRequestError" in response: response = "ERROR in getting result from solardcrportal.nise.res.in. Try again"
    else: response = "DCR NOT-FOUND"
    return (modSrNum, response)

def ProcessUserInput(userInput):
    global prevUserInput
    prevUserInput = userInput
    seen = set()
    userInputList = [str(x) for x in [y.replace(" ", "") for y in userInput.split(",")] if not (x in seen or seen.add((x,)))]
    resultList = [ValidateDCR(modSerNum) for modSerNum in userInputList]
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

class Timer:
    def __init__(self):
        self.startTime, self.endTime = time_perf_counter(), None

    def __enter__(self):
        self.startTime, self.endTime = time_perf_counter(), None
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.endTime = time_perf_counter()

    def ElapsedTime(self):
        if self.endTime is None: return time_perf_counter() - self.startTime
        else: return self.endTime - self.startTime

st.set_page_config(
    page_title="DCRValidation App",
    page_icon="✅",
)

st.title("DCRValidation App")
st.sidebar.success("Select a page above.")
st.markdown("""---""")

st.header("🚨 Note")
st.markdown(
"""
This app verifies DCR for input Module Serial Number via solardcrportal.nise.res.in 🌐

User input should contain module serial number(s) separated by comma.

Example:
* ```
  SerialNumber1, SerialNumber2, SerialNumber3
* ```
  SerialNumber1,SerialNumber2,SerialNumber3
"""
)

st.markdown("""---""")
st.header("✍ Input")
with st.form('chat_input_form'):
    col1, col2 = st.columns([5,1]) 
    with col1:
        userInput = st.text_input(
            "Comma seperated Module Serial Numbers",
            value=None,
            placeholder="Comma seperated Module Serial Numbers",
            label_visibility='collapsed'
        )
    with col2:
        submitButtonPressed = st.form_submit_button('Validate')


st.markdown("""---""")
st.header("🏆 Result")


if (submitButtonPressed or (prevUserInput != userInput)) and (userInput not in ["", None]):
    with st.empty():
        st.write(f"⏳ Processing user input...")
        #with Timer() as timer:
        resultMarkdownText = ProcessUserInput(userInput)
        with Timer() as timer:
            st.write(resultMarkdownText + "\n" + f"⏱ Time taken {timer.ElapsedTime():.6f} secs")
        

# NSMP24091468370, NSMP24091468383, NSMP24091468381, 26240523C3284085, SE540240924065, WS08249037680588