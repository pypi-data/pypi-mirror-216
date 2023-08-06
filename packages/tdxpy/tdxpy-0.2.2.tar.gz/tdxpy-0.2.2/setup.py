# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tdxpy',
 'tdxpy.crawler',
 'tdxpy.parser',
 'tdxpy.parser.ext',
 'tdxpy.parser.std',
 'tdxpy.reader']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=38.0.3,<39.0.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'tdxpy',
    'version': '0.2.2',
    'description': '',
    'long_description': '# TdxPy - Python TDX 数据接口\n\n[![Build Status](https://travis-ci.org/rainx/pytdx.svg?branch=master)](https://travis-ci.org/bopo/tdxpy)\n\n如果喜欢本项目可以在右上角给颗⭐！你的支持是我最大的动力😎！\n\n- 开源协议: MIT license\n- 在线文档: https://tdxpy.readthedocs.io\n- 国内镜像: https://gitee.com/ibopo/tdxpy\n- 项目仓库: https://github.com/mootdx/tdxpy\n\n项目概述\n---------\n本项目是 pytdx 衍生项目, 原作者因不再维护了, 以至于很多问题不能得到修复。\n\n项目特点\n------\n\n* 纯 python 实现，无须引入动态连接库`.dll / .so`文件\n* 支持全平台`Windows / MacOS / Linux`\n* 移除`python2`的支持\n* 去除命令行功能\n* 修复若干 bug\n* 重新整理项目结构\n* 修复基金价格问题\n\n快速安装\n--------\n\n```shell\npip install tdxpy\n```\n\n郑重声明\n-------\n本项目只作学习交流, 不得用于任何商业目的.\n\n此代码用于个人对网络协议的研究和习作，不对外提供服务，任何人使用本代码遇到问题请自行解决，也可以在 github 提 issue 给我，但是我不保证能即时处理。\n\n由于我们连接的是既有的行情软件兼容行情服务器，机构请不要使用此代码，对此造成的任何问题本人概不负责。\n',
    'author': 'bopo',
    'author_email': 'ibopo@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
