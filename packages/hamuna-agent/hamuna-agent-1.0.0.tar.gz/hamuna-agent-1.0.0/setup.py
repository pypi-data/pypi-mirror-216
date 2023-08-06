from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    README = fh.read()
   
setup(
  name = "hamuna-agent",
  version = "1.0.0",
  url = "https://hamuna.club",
  author = "HotDrify",
  license = "Apache License 2.0",
  keywords = [
    "chatBot",
    "freeAI",
    "freeGPT",
    "freeChatGPT",
    "gptfree",
    "freeAPI",
    "python",
    "api",
  ],
  python_requires = ">=3.7",
  packages=find_packages(),
  install_requires=[
    "aiohttp",
    "fake-useragent",
  ]
)
