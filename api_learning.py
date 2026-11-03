import requests

url = "https://httpbin.org/post"

incident = {
    "service": "Jenkins",
    "stage": "Build",
    "error": "mvn: command not found",
    "task": "Explain this error"
}

try:
    response = requests.post(
        url,
        json=incident,
        timeout=10
    )

    print("Status code:", response.status_code)

    result = response.json()

    print("Request method:", result["method"])
    print("Data received by server:", result["json"])

except requests.exceptions.RequestException as error:
    print("Request failed:", error)