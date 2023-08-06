from setuptools import setup

setup(name='mentord',
      version='1.1.2',
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
```
      """,
      long_description_content_type='text/markdown')