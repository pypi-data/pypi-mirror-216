from setuptools import setup

setup(name='mentord',
      version='1.1.3',
      description='Library for discord self bots.',
      packages=['mentord'],
      long_description="""
### Example use:
```python
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

### Send message in chat:
```python
User_client.send_message(content="Hello!", embeds=[], channel_id="916385464238370826")
```
      """,
      long_description_content_type='text/markdown')