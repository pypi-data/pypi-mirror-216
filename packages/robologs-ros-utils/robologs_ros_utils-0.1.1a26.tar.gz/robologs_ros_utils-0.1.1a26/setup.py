# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robologs_ros_utils',
 'robologs_ros_utils.connectors',
 'robologs_ros_utils.destinations.aws.athena',
 'robologs_ros_utils.destinations.aws.dynamodb',
 'robologs_ros_utils.destinations.aws.lambdas',
 'robologs_ros_utils.destinations.aws.s3',
 'robologs_ros_utils.destinations.azure',
 'robologs_ros_utils.destinations.google_cloud',
 'robologs_ros_utils.functions',
 'robologs_ros_utils.sources',
 'robologs_ros_utils.sources.ros1',
 'robologs_ros_utils.utils.file_utils',
 'robologs_ros_utils.utils.img_utils',
 'robologs_ros_utils.utils.video_utils']

package_data = \
{'': ['*']}

install_requires = \
['bagpy>=0.5,<0.6',
 'black[d]>=22.12.0,<23.0.0',
 'boto3>=1.26.26,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'isort>=5.11.2,<6.0.0',
 'nose>=1.3.7,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'opencv-python>=4.5.0.0,<5.0.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytest-datafiles>=2.0.1,<3.0.0',
 'pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'rosbags>=0.9.13,<0.10.0',
 'tqdm>=4.64.1,<5.0.0',
 'types-tqdm>=4.64.7.9,<5.0.0.0']

entry_points = \
{'console_scripts': ['robologs-ros-utils = robologs_ros_utils.cli:main']}

setup_kwargs = {
    'name': 'robologs-ros-utils',
    'version': '0.1.1a26',
    'description': 'robologs-ros-utils is an open source library of containerized data transformations for the robotics and drone communities',
    'long_description': '',
    'author': 'roboto.ai',
    'author_email': 'info@roboto.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
