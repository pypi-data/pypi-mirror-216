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
import json

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

from pixelfeeder.tools import (
    PathUnion, get_file_paths, metadata_file_predicate,
    photo_file_predicate, prepare_string
)

from pixelfeeder.tools import FlickrVisibility
assert FlickrVisibility.__name__ in globals()

DEFAULT_CAPTION_ORDER = 'name, description, date_taken, tags'

MetadataType = Dict[str, Union[str, int, bool]]
PhotoDictType = Dict[str, MetadataType]


class FlickrDataReaderError(RuntimeError):
    ...


class FlickrMetadataError(FlickrDataReaderError):
    ...


class PhotoLocatorType(enum.Enum):
    PHOTO_ID = enum.auto()
    IMAGE_FILE = enum.auto()


@dataclass
class Issue:
    locator: str
    locator_type: PhotoLocatorType
    info: str

    @property
    def locator_str(self) -> str:
        if self.locator_type is PhotoLocatorType.PHOTO_ID:
            return f'photo_id "{self.locator}"'
        if self.locator_type is PhotoLocatorType.IMAGE_FILE:
            return f'Image file "{self.locator}"'
        raise FlickrDataReaderError(f'Unhandled locator type {self.locator_type}')

    def __str__(self) -> str:
        return f'{self.locator_str}: {self.info}'


class FlickrData(PhotoDictType):
    def __init__(self, *args, **kwargs) -> None:
        self.issues: List[Issue] = []
        super().__init__(*args, **kwargs)


def get_tags(metadata: Dict) -> List[str]:
    """ Get list of tags from Flicker image metadata
    """
    return [i['tag'] for i in metadata['tags']]


def metadata_to_caption(metadata: Dict, order=DEFAULT_CAPTION_ORDER, datetime_format='%c') -> str:
    items = [i.strip() for i in order.split(',')]

    fields = {}
    fields['name'] = prepare_string(metadata['name'])
    fields['description'] = prepare_string(metadata['description'])
    taken_dt = datetime.fromisoformat(prepare_string(metadata['date_taken']))
    fields['date_taken'] = taken_dt.strftime(datetime_format)
    fields['tags'] = ' '.join([f'#{t}' for t in get_tags(metadata)])

    caption = '\n\n'.join([fields[i] for i in items if fields[i]])

    return caption.strip()


class FlickrDataReader:
    def __init__(self, images_dir: PathUnion, metadata_dir: PathUnion):
        self.images_dir = Path(images_dir)
        self.metadata_dir = Path(metadata_dir)

    def get_photo_by_id(self, photo_id: str, file_paths: Iterable[PathUnion], ignore_multiple=False) -> Optional[str]:
        result = []
        for path in file_paths:
            path_str = str(path)
            if photo_id in path_str:
                result.append(path_str)
        if not ignore_multiple:
            if len(result) > 1:
                raise FlickrMetadataError(f'Multiple files found for id {photo_id}')
        if result:
            return result[0]
        return None

    def get_metadata_file_paths(self) -> List[Path]:
        return list(filter(metadata_file_predicate, get_file_paths(self.metadata_dir)))

    def get_photo_file_paths(self) -> List[Path]:
        return list(filter(photo_file_predicate, get_file_paths(self.images_dir)))

    def get_photo_dict(self, ignore_multiple=False) -> FlickrData:
        result = FlickrData()

        metadata_file_paths = self.get_metadata_file_paths()
        photo_files = list(map(str, self.get_photo_file_paths()))

        for file_path in metadata_file_paths:
            with open(file_path, 'r', encoding='UTF-8') as file:
                metadata = json.load(file)

            photo_id = metadata['id']

            try:
                photo_file = self.get_photo_by_id(photo_id, photo_files, ignore_multiple)
            except FlickrMetadataError:
                result.issues.append(Issue(photo_id, PhotoLocatorType.PHOTO_ID, 'matches multiple images'))

            if photo_file is None:
                result.issues.append(Issue(photo_id, PhotoLocatorType.PHOTO_ID, 'no image file'))
                continue
            if photo_file in result:
                issue = Issue(photo_file, PhotoLocatorType.IMAGE_FILE, 'matches with multiple metadata files')
                result.issues.append(issue)
                continue

            result[photo_file] = metadata

        for path in photo_files:
            if path not in result:
                issue = Issue(path, PhotoLocatorType.IMAGE_FILE, 'missing metadata')
                result.issues.append(issue)

        return result
