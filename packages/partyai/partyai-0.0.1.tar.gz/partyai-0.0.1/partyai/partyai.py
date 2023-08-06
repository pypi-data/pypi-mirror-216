import requests


class PartyAI:
    def __init__(self):
        self.apiUrl = "https://api.partyai.co/v1"
        self.cache = {}
        self.pluginsInCache = []

    def definitions(self, names):
        # Filter out plugins that are already in the cache
        pluginsToFetch = list(filter(lambda name: name not in self.pluginsInCache, names))

        if len(pluginsToFetch) > 0:
            response = requests.post(f"{self.apiUrl}/functions/spec", json = {"names": pluginsToFetch})

            if response.status_code != 200:
                print("Error:", response.text)
                return None

            for plugin in response.json():
                self.cache[plugin["name"]] = plugin

            self.pluginsInCache.extend(pluginsToFetch)

        result = []
        for key, value in self.cache.items():
            if key.split("-")[0] in names:
                value["name"] = key.split("/")[1]
                result.append(value)
        return result

    def call(self, name, args):
        full_function_name = next((key for key in self.cache.keys() if key.endswith(name)), None)
        if not full_function_name:
            raise ValueError(f"Function {name} not found!")

        response = requests.post(f"{self.apiUrl}/functions/execute", json = {
            "jsonrpc": "2.0",
            "method": full_function_name,
            "params": args,
        })

        if response.status_code != 200:
            print("Error:", response.text)
            return None

        return response.json()
