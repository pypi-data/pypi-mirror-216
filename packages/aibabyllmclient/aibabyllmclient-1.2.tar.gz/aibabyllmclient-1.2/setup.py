from setuptools import setup, find_packages

setup(
    name="aibabyllmclient",
    version="1.2",
    author="zzy",
    author_email="zhaichenhao1889@163.com",
    description="llmserver_call",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)