from setuptools import setup

setup(
    name="mentord",
    version="1.2.0",
    description="A sync library for creating self bots in python!",
    packages=["mentord", "mentord/classes", "mentord/events", "mentord/utils"],
    long_description_content_type="text/markdown",
    long_description="""
### Example use:

```python
from mentord import *

User_client: Client = Client()
User_client.connect(token='YOUR TOKEN')
```

### Use decorators:

```python
@on_ready(client=User_client, delay=5.0)
def client_on_ready() -> None:
    print('Self-bot is started!')

@on_message(client=User_client, delay=0.5)
def client_on_message(message: Message) -> None:
    utils.channel_opers.ChannelOperations(channel=message.channel_id, client=User_client).send_message("hello!")
```""",
)
