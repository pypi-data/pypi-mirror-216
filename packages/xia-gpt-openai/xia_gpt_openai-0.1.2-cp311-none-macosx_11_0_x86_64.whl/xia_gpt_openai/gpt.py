import os
import openai
from xia_gpt import Gpt


class OpenaiGpt(Gpt):
    gpt_engine = openai
    gpt_engine_name = "openai"
    gpt_engine.api_key = os.environ.get("OPEN_API_KEY")
    gpt_engine_model = "gpt-3.5-turbo"
    # gpt_engine_model = "gpt-4"

    def chat_complete(self, system: str, message: str, context: list = None, **kwargs):
        """Give the context and

        Args:
            system: System Roles
            message: User message to be sent
            context: previous dialog to be passed as parameters as a list of conversion.
                each conversion contains user and assistant part, like: {"user": "Hello", "assistant": "World"}
            **kwargs: other parameters

        Returns:
            result and the job results
        """
        built_request = [{"role": "system", "content": system}]
        context = [] if not context else context
        for dialog in context:
            built_request.append({"role": "user", "content": dialog["user"]})
            built_request.append({"role": "user", "content": dialog["assistant"]})
        built_request.append({"role": "user", "content": message})
        job_result = openai.ChatCompletion.create(model=self.gpt_engine_model, messages=built_request, **kwargs)
        choices = job_result.pop("choices")
        return choices[0].message["content"], job_result


if __name__ == '__main__':
    gpt_agent = OpenaiGpt()
    result, job_status = gpt_agent.chat_complete(
        "You are a helpful assistant.",
        "Where was it played?",
        [{"user": "Who won the world series in 2020?",
         "assistant": "The Los Angeles Dodgers won the World Series in 2020."}]
    )
    print(result)
    print(job_status)
