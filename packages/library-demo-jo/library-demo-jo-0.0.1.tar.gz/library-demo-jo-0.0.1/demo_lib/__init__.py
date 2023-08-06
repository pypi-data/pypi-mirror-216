import yaml
from importlib import resources

def say_hello_demo():
    data = yaml.load(resources.read_text("demo_lib", "hello.yaml"), yaml.FullLoader)
    print(data)
