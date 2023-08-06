from setuptools import setup

setup(name='mentord',
      version='1.1.4',
      long_description_content_type='text/markdown',
      description="""
Sync library from discord self bots.
      """,
      long_description="""
### Example use

```python
from mentord import *

User_client: Client = Client() 
User_client.connect(token='YOUR TOKEN')
```

### Use decorators:

```python
@User_client.on_message
def client_wait_message(message: Message):
    print('new message!')

@User_client.on_ready
def client_on_ready():
    print('client on connected!')
```

### Send message in channel:

```python
@User_client.on_message
def client_wait_message(message: Message):
    User_client.send_message(content="Hello!", embeds=[], channel_id=message.channel_id)
```
      """,
      packages=['mentord'],)