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

import enum
import mimetypes
import os

from numbers import Real
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

PathUnion = Union[str, os.PathLike]
ENCODING = 'UTF-8'


class NumericKwargs(dict):
    def _calc(self, operator: str, other: float) -> 'NumericKwargs':
        result = {}
        for key, val in self.items():
            if isinstance(val, Real):
                if operator == '*':
                    new_val = val * other
                elif operator == '/':
                    new_val = val / other
                else:
                    raise AssertionError(f'Unknown operator {operator}')
            else:
                new_val = val
            result[key] = new_val
        return NumericKwargs(result)

    def __mul__(self, other: float) -> 'NumericKwargs':
        return self._calc('*', other)

    def __div__(self, other: float) -> 'NumericKwargs':
        return self._calc('*', other)


class FlickrVisibility(enum.Enum):
    PUBLIC = 'public'
    FRIENDS_ONLY = 'friends only'
    FAMILY_ONLY = 'family only'
    FRIENDS_AND_FAMILY = 'friends & family'
    PRIVATE = 'private'


class PixelfedVisibility(enum.Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'
    UNLISTED = 'unlisted'

    @classmethod
    def from_flickr_visibility(cls, visibility: FlickrVisibility) -> 'PixelfedVisibility':
        if visibility in (
                FlickrVisibility.FRIENDS_ONLY,
                FlickrVisibility.FAMILY_ONLY,
                FlickrVisibility.FRIENDS_AND_FAMILY):
            return cls.UNLISTED
        return cls(visibility.value)


def metadata_file_predicate(file_path: Path) -> bool:
    """ Check if a file type matches metadata file
    """
    filename = file_path.name.lower()
    mimetype, _enc = mimetypes.guess_type(file_path)
    return mimetype == 'application/json' and filename.startswith('photo_')


def photo_file_predicate(file_path: Path) -> bool:
    """ Check if a file type matches appropirate photo format
    """
    mimetype, _enc = mimetypes.guess_type(file_path)
    return mimetype in {'image/jpeg', 'image/png'}


def get_file_paths(path: PathUnion) -> List[Path]:
    """ Traverse the path and return list of file paths
    """
    result = []
    for root, _dirs, files in os.walk(top=Path(path)):
        root_path = Path(root)
        for filename in files:
            result.append(root_path / filename)
    return result


def prepare_string(value: Any) -> str:
    assert isinstance(value, str)
    return value.strip()


def load_config(file_path: PathUnion, create_missing=False) -> Dict:
    file_path_casted = Path(file_path)
    if create_missing:
        file_path_casted.parent.mkdir(parents=True, exist_ok=True)
        file_path_casted.touch()
    with open(file_path_casted, 'r', encoding=ENCODING) as conf_file:
        return yaml.safe_load(conf_file) or {}


def save_config(file_path: PathUnion, data: Dict, create_missing=False) -> None:
    file_path_casted = Path(file_path)
    if create_missing:
        file_path_casted.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path_casted, 'w', encoding=ENCODING) as conf_file:
        yaml.dump(data, conf_file)


def validate_path_exists(arg: str) -> Path:
    if (file := Path(arg)).exists():
        return file
    raise FileNotFoundError(f'Path "{file}" does not exist')
