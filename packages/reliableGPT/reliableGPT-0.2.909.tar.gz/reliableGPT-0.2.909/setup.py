from setuptools import setup, find_packages

setup(
    name='reliableGPT',
    version='0.2.909',
    description='Error handling and auto-retry library for GPT',
    author='Ishaan Jaffer',
    packages=find_packages(),
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
