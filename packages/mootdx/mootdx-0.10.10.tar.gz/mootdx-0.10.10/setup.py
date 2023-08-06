# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mootdx',
 'mootdx.cache',
 'mootdx.contrib',
 'mootdx.financial',
 'mootdx.tools',
 'mootdx.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0',
 'pandas>=1.5.2,<2.0.0',
 'tdxpy>=0.2.1,<0.3.0',
 'tenacity>=8.1.0,<9.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

extras_require = \
{'all': ['py-mini-racer>=0.6.0,<0.7.0',
         'prettytable>=3.5.0,<4.0.0',
         'click>=8.1.3,<9.0.0'],
 'cli': ['prettytable>=3.5.0,<4.0.0', 'click>=8.1.3,<9.0.0'],
 'fetch': ['py-mini-racer>=0.6.0,<0.7.0']}

entry_points = \
{'console_scripts': ['mootdx = mootdx.__main__:entry']}

setup_kwargs = {
    'name': 'mootdx',
    'version': '0.10.10',
    'description': '通达信数据读取接口.',
    'long_description': "通达信数据读取接口\n==================\n\n[![image](https://badge.fury.io/py/mootdx.svg)](http://badge.fury.io/py/mootdx)\n[![image](https://img.shields.io/travis/bopo/mootdx.svg)](https://travis-ci.org/mootdx/mootdx)\n[![Documentation Status](https://readthedocs.org/projects/mootdx/badge/?version=latest)](https://mootdx.readthedocs.io/zh/latest/?badge=latest)\n[![Updates](https://pyup.io/repos/github/mootdx/mootdx/shield.svg)](https://pyup.io/repos/github/mootdx/mootdx/)\n\n如果喜欢本项目可以在右上角给颗⭐！你的支持是我最大的动力😎！\n\n郑重声明: 本项目只作学习交流, 不得用于任何商业目的.\n\n-   开源协议: MIT license\n-   在线文档: <https://www.mootdx.com>\n-   国内镜像: <https://gitee.com/ibopo/mootdx>\n-   项目仓库: <https://github.com/mootdx/mootdx>\n-   问题交流: <https://github.com/mootdx/mootdx/issues>\n\n版本更新(倒序)\n--------------\n\n版本更新日志: <https://mootdx.readthedocs.io/zh_CN/latest/history/>\n\n运行环境\n--------\n\n-   操作系统: Windows / MacOS / Linux 都可以运行.\n-   Python: 3.8 以及以上版本.\n\n安装方法\n--------\n\n> 新手建议使用 `pip install -U 'mootdx[all]'` 安装\n\n### PIP 安装方法\n```shell\n\n# 包含核心依赖安装\npip install 'mootdx'\n\n# 包含命令行依赖安装, 如果使用命令行工具可以使用这种方式安装\npip install 'mootdx[cli]'\n\n# 包含所有扩展依赖安装, 如果不清楚各种依赖关系就用这个命令\npip install 'mootdx[all]'\n```\n\n### 升级安装\n\n```shell\npip install -U tdxpy mootdx\n```\n\n> 如果不清楚各种依赖关系就用这个命令 `pip install -U 'mootdx[all]'`\n\n使用说明\n--------\n\n> 以下只列举一些例子, 详细说明请查看在线文档: <https://www.mootdx.com>\n\n通达信离线数据读取\n\n```python\nfrom mootdx.reader import Reader\n\n# market 参数 std 为标准市场(就是股票), ext 为扩展市场(期货，黄金等)\n# tdxdir 是通达信的数据目录, 根据自己的情况修改\n\nreader = Reader.factory(market='std', tdxdir='C:/new_tdx')\n\n# 读取日线数据\nreader.daily(symbol='600036')\n\n# 读取分钟数据\nreader.minute(symbol='600036')\n\n# 读取时间线数据\nreader.fzline(symbol='600036')\n```\n\n通达信线上行情读取\n\n```python\nfrom mootdx.quotes import Quotes\n\n# 标准市场\nclient = Quotes.factory(market='std', multithread=True, heartbeat=True)\n\n# k 线数据\nclient.bars(symbol='600036', frequency=9, offset=10)\n\n# 指数\nclient.index(symbol='000001', frequency=9)\n\n# 分钟\nclient.minute(symbol='000001')\n```\n\n通达信财务数据读取\n\n```python\nfrom mootdx.affair import Affair\n\n# 远程文件列表\nfiles = Affair.files()\n\n# 下载单个\nAffair.fetch(downdir='tmp', filename='gpcw19960630.zip')\n\n# 下载全部\nAffair.parse(downdir='tmp')\n```\n\n加微信交流\n----------\n\n![](docs/img/IMG_2851.JPG)\n\n常见问题\n--------\n\nM1 mac 系统PyMiniRacer不能使用，访问:\n<https://github.com/sqreen/PyMiniRacer/issues/143>\n",
    'author': 'bopo',
    'author_email': 'ibopo@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.mootdx.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
