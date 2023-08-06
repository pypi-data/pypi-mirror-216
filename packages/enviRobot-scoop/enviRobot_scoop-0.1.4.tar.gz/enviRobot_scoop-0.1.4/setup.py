import setuptools
# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name = "enviRobot_scoop",
    version = "0.1.4",
    author = "JcXGTcW",
    author_email="jcxgtcw@cameo.tw",
    description="enviRobot service that can be held by Scoop.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bohachu/ask_enviRobot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    'fastapi==0.63.0',
    'uvicorn==0.13.4',
    'openai==0.27.4',
    'geocoder==1.38.1',
    'line-bot-sdk==2.4.2',
    'pandas==1.5.3',
    'geopy==2.3.0',
    'selenium==4.7.2',
    'pyimgur==0.6.0',
    'pyyaml==6.0',
    'python-dotenv==0.15.0',
    "plotly==5.15.0",
    "kaleido==0.2.1"]
    )