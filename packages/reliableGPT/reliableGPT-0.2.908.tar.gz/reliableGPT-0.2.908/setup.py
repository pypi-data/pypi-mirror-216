from setuptools import setup

setup(
    name='reliableGPT',
    version='0.2.908',
    description='Error handling and auto-retry library for GPT',
    author='Ishaan Jaffer',
    packages=['reliablegpt'],
    install_requires=[
        'openai',
        'termcolor',
        'klotty',
        'numpy',
        'posthog',
        'tiktoken',
        'api_handler',
        'custom_queue'
    ],
)
