from setuptools import setup
 
setup(
    name='AppForge',
    version='0.1.0',
    description='A benchmark for app generation',
    author='Your Name',
    author_email='your.email@example.com',
    packages=['AppForge'],
    package_data={
        '': ['tasks/tasks.json','compiler/*'],
    },
    install_requires=[
            "docker",
            "openpyxl",
            "pathlib",
            "typing",
            "numpy",
            ],
    extras_require={
        'example': [  # run qwen3coder example
            "openai==0.28",
            "anthropic",
            "tenacity",
            "dashscope",
            
        ],
        'local': [  # local emulator

        ],
    }
)