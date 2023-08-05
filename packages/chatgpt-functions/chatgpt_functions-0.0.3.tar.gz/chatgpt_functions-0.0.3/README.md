# Example of usage:
```python
import asyncio
from chatgpt_functions import (
    ChatGPT,
    Message,
    Roles,
    ChatGptFunction,
    Parameters,
    Property,
)
from config import API_KEY

chatgpt = ChatGPT(openai_api_key=API_KEY)


async def main():
    def say_hello(args):
        print(args)

    await chatgpt.get_chatgpt_response_with_functions(
        functions=[
            ChatGptFunction(
                function=say_hello,
                parameters=Parameters(
                    properties=[
                        Property(
                            property_name="name",
                            prop_type="string",
                            description="Name who to say hello to",
                            enum=["Evan", "Micha"],
                        ),
                        Property(
                            property_name="text",
                            prop_type="string",
                            description="Greeting",
                        ),
                    ]
                ),
                function_description="Say hello to user",
            )
        ],
        messages=[Message(role=Roles.USER, content='Скажи приветик миче')]
    )


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
```