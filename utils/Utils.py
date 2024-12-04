from time import perf_counter as time_perf_counter
import urllib.request

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