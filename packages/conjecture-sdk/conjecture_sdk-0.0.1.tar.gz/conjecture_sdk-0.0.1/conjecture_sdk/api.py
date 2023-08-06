import requests

class ConjAPI:
    def __init__(self, api_key=None):
        self.base_url = "https://api.conjecture.dev"
        self.api_key = None
        self.headers = None

    def request(self, method, endpoint, data=None):
        # setup api_key and base_url before making the request
        import conjecture_sdk
        self.api_key = conjecture_sdk.api_key or self.api_key
        self.base_url = conjecture_sdk.base_url or self.base_url
        self.headers = {'api-key': self.api_key} if self.api_key else None

        url = f"{self.base_url}/v1/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        return response.json()