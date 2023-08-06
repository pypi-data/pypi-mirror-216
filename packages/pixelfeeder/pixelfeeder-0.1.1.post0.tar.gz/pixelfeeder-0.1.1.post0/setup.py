# Copyright 2023 Anton Karmanov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is a part of Pixelfeeder utility. Pixelfeeder helps to migrate data
# from Flickr to a Pixelfed instance.

from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='pixelfeeder',
    version='0.1.1.post0',
    author='Anton Karmanov',
    author_email='a.karmanov@inventati.org',
    python_requires='>=3.8',
    url='https://gitlab.com/bergentroll/pixelfeeder',
    description='Import Flickr data into a Pixelfed account',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache',
    packages=find_packages(),
    include_package_data=False,
    install_requires=(
        'Pillow~=9.4',
        'PyYAML~=6.0',
        'argcomplete~=3.0',
        'httpx~=0.23',
        'xdg-base-dirs~=6.0',
    ),
    entry_points={
        'console_scripts': [
            'pixelfeeder = pixelfeeder.cli:main',
            'pixelfeeder-gui = pixelfeeder.gui:main',
        ]
    },
    classifiers=[
         'Environment :: X11 Applications',
         'License :: OSI Approved :: Apache Software License',
         'Operating System :: OS Independent',
         'Programming Language :: Python :: 3',
         'Topic :: Multimedia :: Graphics',
         'Topic :: Utilities',
    ])
