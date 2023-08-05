from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_mcqq_server',
version='1.0.4',
description='mcqq服主版',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_mcqq_server"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot","nonebot_plugin_guild_patch","mcrcon"],
url='https://github.com/KarisAya/nonebot_plugin_mcqq_server',
)