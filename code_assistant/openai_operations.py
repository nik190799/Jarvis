import openai
import os, time
from file_operations import Operation
from tasks import Task

openai.api_key = os.environ.get("OPENAI_API_KEY")

class OpenAI:
    def get_response(json_id, user_input):
        messages = Operation.load_messages(json_id)
        max_attempts = 2
        for attempt in range(max_attempts):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages + [
                        {"role": "user", "content": user_input}
                    ]
                )
                break
            except Exception as e:
                print(f"<Error: API error: {str(e)}>")
                if attempt < max_attempts - 1:
                    print(f"<Update: Retrying... Attempt {attempt + 2}>")
                    time.sleep(2)
                else:
                    print("<Update: Max attempts reached. Unable to get API response.>")
                    return None
        assistant_response = response.choices[0].message.content
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": assistant_response})
        # Operation.save_messages(json_id, messages)
        if json_id == 0 or json_id == 1:
            return Task.generate_code_map(assistant_response)
        else:
            return assistant_response