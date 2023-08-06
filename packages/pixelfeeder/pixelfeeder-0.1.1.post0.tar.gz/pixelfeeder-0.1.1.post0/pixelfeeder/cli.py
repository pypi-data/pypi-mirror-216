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

import argparse
import logging

from pathlib import Path

import argcomplete

from pixelfeeder.flickr_data_reader import (
    DEFAULT_CAPTION_ORDER, FlickrDataReader, FlickrVisibility, metadata_to_caption)
from pixelfeeder.pixelfed_uploader import PixelfedClient, PixelfedVisibility
from pixelfeeder.tools import load_config, validate_path_exists


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pixelfeeder',
        description='Import Flickr data into a Pixelfed account',
        epilog=None)

    parser.add_argument(
        '-i', '--images-dir',
        help='Directory with image files',
        type=validate_path_exists,
        required=True)
    parser.add_argument(
        '-m', '--metadata-dir',
        type=validate_path_exists,
        help='Directory with metadata files, same as the --images-dir if not passed')
    parser.add_argument(
        '-c', '--config-file',
        type=Path,
        default=Path('config.yaml'),
        help='File with a link and a token')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true')
    parser.add_argument(
        '--ignore-ssl-verify',
        help='Skip SSL verification for the Pixelfed instance',
        action='store_true')
    parser.add_argument(
        '-n', '--dry-run',
        help='Do not upload, print what supposed to do instead',
        action='store_true')

    argcomplete.autocomplete(parser)
    return parser


def main() -> None:
    args = get_argparser().parse_args()

    if args.metadata_dir is None:
        args.metadata_dir = args.images_dir

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger(__name__)

    conf = load_config(args.config_file)
    base_url = conf['instance']
    token = conf['token']

    data_reader = FlickrDataReader(images_dir=args.images_dir, metadata_dir=args.metadata_dir)
    data = data_reader.get_photo_dict()

    for issue in data.issues:
        logger.warning(issue)

    strict_ssl = not (args.ignore_ssl_verify or conf.get('ignore_ssl_verify', False))
    pixelfed = PixelfedClient(base_url, token, strict_ssl=strict_ssl)

    for file_path, metadata in data.items():
        caption = metadata_to_caption(
            metadata,
            order=conf.get('caption_order', DEFAULT_CAPTION_ORDER),
            datetime_format=conf.get('caption_datetime_format', '%c'),)
        flickr_visibility = FlickrVisibility(metadata['privacy'])
        visibility = PixelfedVisibility.from_flickr_visibility(flickr_visibility)
        logger.info(f'Uploading {file_path}')
        if args.dry_run:
            logger.info(f'Caption:\n{caption}')
            logger.info(f'Visibility: {visibility.value}')
        else:
            pixelfed.blocking_create_post(file_path, caption=caption, visibility=visibility)


if __name__ == '__main__':
    main()
