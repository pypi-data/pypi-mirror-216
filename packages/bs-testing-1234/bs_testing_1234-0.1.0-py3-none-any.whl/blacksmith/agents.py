import redis
import json
import requests
from tenacity import retry, stop_after_attempt
from blacksmith.llm import llm_call
from blacksmith.defaults.prompts import DEFAULT_SYSTEM_PROMPT, DEFAULT_REACT_PROMPT

# Connect to tool storage service
r = redis.Redis(host="redis-service", port=6379)


class Agent:
    def __init__(self, **kwargs) -> None:
        type = kwargs.get("type", "zero-shot-react")

        # Make this a switch case
        if type == "zero-shot-react":
            self.prompt = DEFAULT_REACT_PROMPT
            self.system_prompt = DEFAULT_SYSTEM_PROMPT
        else:
            self.prompt = kwargs.get("prompt")
            self.system_prompt = kwargs.get("system_prompt")

        self.tools = kwargs.get(
            "tools", [json.loads(tool.decode()) for tool in r.lrange("tools", 0, -1)]
        )
        self.max_loops = kwargs.get("max_loops", 5)

    def process(self, messages):
        @retry(stop=stop_after_attempt(self.max_loops))
        def _think():
            resp = llm_call(messages=messages, tools=self.tools)

            # while not final answer
            while not resp.get("content"):
                print(resp)
                func = resp["function_call"]
                service_name = func["name"]
                args = json.loads(func["arguments"])
                url = f"http://{service_name}:80"
                tool_res = requests.get(url=url, json=args)
                data = tool_res.json()
                print(f"Executed function {service_name}. Result: {data}")
                messages.append(
                    {
                        "role": "user",
                        "content": f"""
                            Observation: Result of calling {service_name} with {args} is {data}.
                            If the information provided in the observations can answer the initial question, do not execute further function calls and return the answer. Otherwise, proceed.
                        """,
                    }
                )
                resp = llm_call(messages=messages, tools=self.tools)
            return resp["content"]

        return _think()

    def run(self, input: str) -> None:
        formatted_prompt = self.prompt.format(input=input)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": formatted_prompt},
        ]
        return self.process(messages=messages)
