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
import asyncio
import enum
import locale
import logging
import tkinter
import webbrowser

from pathlib import Path
from tkinter import ttk, filedialog, scrolledtext
from typing import Any, Callable, List, Optional, Union

import PIL.Image
import PIL.ImageFile
import PIL.ImageTk
import argcomplete
import xdg_base_dirs

from pixelfeeder.flickr_data_reader import (
    DEFAULT_CAPTION_ORDER, FlickrData, FlickrDataReader, FlickrVisibility, metadata_to_caption
)
from pixelfeeder.image_loader import BaseImageLoader, ImageLoader, CachingImageLoader, ImageLoaderError
from pixelfeeder.pixelfed_uploader import PixelfedVisibility, PixelfedClient, PixelfedClientError
from pixelfeeder.tools import NumericKwargs, load_config, save_config

MasterType = Union[tkinter.Tk, tkinter.Widget]

APP_NAME = 'Pixelfeeder'
EXIF_ORIENTATION_MAP = {1: 0, 3: 180, 6: 270, 8: 90}
PADDING = 5
FRAME_RELIEF = tkinter.GROOVE
PADDING_KWARGS = NumericKwargs(padx=PADDING, pady=PADDING)
IPADDING_KWARGS = NumericKwargs(ipadx=PADDING, ipady=PADDING)
BUTTON_IPADDING_KWARGS = NumericKwargs(ipadx=PADDING, ipady=PADDING/2)
SIDE_FRAME_WIDTH = '384p'

CACHED_FILES_LIMIT = 10
PRELOAD_WINDOW = 5

LOGGER = logging.getLogger(__name__)


def set_custom_themes() -> None:
    style = ttk.Style()
    style.configure(
        'ClearButton.TButton',
        highlight='grey',
        font=('Monospace', 8, 'bold'),
        padding='2p', width=0, height=0)
    style.map(
        'ClearButton.TButton',
        background=[('active', '!pressed', 'black'), ('active', 'pressed', 'lightgrey'), ('!active', 'black')],
        relief=[('active', 'ridge'), ('!active', 'ridge')],
        foreground=[('active', '!pressed', 'grey'), ('active', 'pressed', 'black'), ('!active', 'grey')],
        bordercolor=[('active', 'white'), ('!active', 'grey')],)


def set_text_content(field: tkinter.Text, text: Optional[str] = None) -> None:
    if text is None:
        text = ''
    field.delete('1.0', tkinter.END)
    field.insert(tkinter.END, text)


class KeypressWrapper:
    keyboard_pause = 100

    def __init__(self, app: tkinter.Tk, callback: Callable[[], None], pause_ms: Optional[int] = None) -> None:
        if pause_ms is None:
            pause_ms = self.keyboard_pause

        self.master = app
        self.callback = callback
        self.pause = pause_ms

        self.kb_block = False

    def __call__(self, _: tkinter.Event):
        if not self.kb_block:
            self.callback()
        self.kb_block = True
        self.master.after(self.pause, self._unset_kb_block)

    def _unset_kb_block(self) -> None:
        self.kb_block = False


class ImageScale(ttk.Scale):
    label_update_period = 10
    label_hide_period = 1000
    deffered_callback_period = 200

    def __init__(self, master: tkinter.Widget, callback: Callable[[], None], variable: tkinter.IntVar) -> None:
        super().__init__(master, command=self._command, variable=variable)
        self._var = variable
        self._load_image_job_id = ''
        self._update_label_job_id = ''
        self._hide_label_job_id = ''
        self._callback = callback
        self._handle_label = ttk.Label(
            self.master,
            justify=tkinter.CENTER,
            background='white',
            relief=tkinter.SOLID,
            border=1,
            padding='2p')

    @property
    def value(self) -> int:
        return self._var.get()

    def _command(self, _: str) -> None:
        if self._load_image_job_id:
            self.master.after_cancel(self._load_image_job_id)
        self._load_image_job_id = self.master.after(self.deffered_callback_period, self._callback)

        if self._update_label_job_id:
            self.master.after_cancel(self._update_label_job_id)
        self._update_label_job_id = self.master.after(self.label_update_period, self._update_label)

        if self._hide_label_job_id:
            self.master.after_cancel(self._hide_label_job_id)
        self._hide_label_job_id = self.master.after(self.label_hide_period, self._handle_label.place_forget)

    def _update_label(self) -> None:
        handler_x, handler_y = self.coords()
        self._handle_label.configure(text=self.value + 1)
        self._handle_label.place(
            in_=self,
            x=handler_x,
            y=handler_y - self.winfo_height() / 2,
            bordermode=tkinter.OUTSIDE,
            anchor=tkinter.S)


class Image(ttk.LabelFrame):
    exif_tags = {v: k for k, v in PIL.Image.ExifTags.TAGS.items()}
    exif_orientation_key = exif_tags['Orientation']
    photo_tag = 'PHOTO'
    frame_relief = tkinter.GROOVE
    placeholder = '(EMPTY)'

    def __init__(
            self,
            master: MasterType,
            input_frame: 'InputFrame',
            settings: 'Settings',
            log_screen: 'LogScreen',
            image_loader: BaseImageLoader):
        super().__init__(master, text=self.placeholder, relief=FRAME_RELIEF, labelanchor=tkinter.S)

        self._input_frame = input_frame
        self._settings = settings
        self._log_screen = log_screen

        self._image_loader = image_loader
        self._photo_data: FlickrData
        self._photo_paths: List[str] = []
        self._image_orig: Optional[PIL.Image] = None
        self._image: PIL.Image
        self._photo_image: PIL.ImageTk.PhotoImage
        self._current_image_path: Optional[str] = None

        self._index_var = tkinter.IntVar(value=0)
        self._canvas = tkinter.Canvas(self, bg='gray')
        self._scale = ImageScale(
            self,
            callback=self._load_image,
            variable=self._index_var,)

        self._canvas.bind('<Configure>', self._refresh)

        self._canvas.pack(fill=tkinter.BOTH, expand=True, **PADDING_KWARGS)
        self._scale.pack(fill=tkinter.X, expand=False, **PADDING_KWARGS)
        self._input_frame.enable()

    @property
    def index(self) -> int:
        return self._index_var.get()

    @index.setter
    def index(self, value: int) -> None:
        images_num = len(self._photo_paths)
        if images_num:
            value = value % images_num
        else:
            value = 0
        self._index_var.set(value)
        self._load_image()

    @property
    def image_path(self) -> Optional[str]:
        if not self._photo_paths:
            return None
        return self._photo_paths[self.index]

    def change_path(self) -> None:
        self._image_loader.clear()

        images_dir = self._input_frame.images_dir
        metadata_dir = self._input_frame.metadata_dir

        assert images_dir
        assert metadata_dir

        flickr_data_reader = FlickrDataReader(images_dir, metadata_dir)

        LOGGER.debug(f'Searching data in {images_dir} images dir, {metadata_dir} metadata dir')
        self._photo_data = flickr_data_reader.get_photo_dict()
        for issue in self._photo_data.issues:
            self._log_screen.warning(str(issue))
        sorted_data = dict(sorted(self._photo_data.items(), key=lambda i: i[1]['id']))
        self._photo_paths = list(sorted_data.keys())

        self.index = 0
        self._scale.configure(to=len(self._photo_paths) - 1)

        self._load_image()

    def seek_image(self, image_path: Optional[str]) -> None:
        if image_path is None:
            return
        try:
            self.index = self._photo_paths.index(image_path)
        except ValueError:
            LOGGER.warning(f'File {image_path} not found')
            return
        self._load_image()

    def next(self) -> None:
        self.index += 1

    def prev(self) -> None:
        self.index -= 1

    def refresh(self) -> None:
        self._canvas.event_generate(
            '<Configure>',
            width=self._canvas.winfo_width(),
            height=self._canvas.winfo_height())

    def reload(self) -> None:
        self._load_image()

    def _refresh(self, event: tkinter.Event) -> None:
        LOGGER.debug('Resizing image by event %s', event)
        if not self._image_orig:
            self._clear_canvas()
            return

        self._image = self._image_orig.copy()

        self._image.thumbnail((event.width, event.height), PIL.Image.Resampling.LANCZOS)
        self._photo_image = PIL.ImageTk.PhotoImage(self._image)
        self._clear_canvas()
        self._canvas.create_image(
            self._canvas.winfo_width()/2,
            self._canvas.winfo_height()/2,
            image=self._photo_image,
            anchor=tkinter.CENTER,
            tags=self.photo_tag)

    def _clear_canvas(self) -> None:
        self._canvas.delete(self.photo_tag)

    def _try_to_preload_images(self) -> None:
        ind1, ind2 = self.index - PRELOAD_WINDOW, self.index + PRELOAD_WINDOW

        if ind2 - ind1 >= len(self._photo_paths):
            paths = self._photo_paths
        elif ind1 >= 0:
            paths = self._photo_paths[ind1: ind2]
        else:
            paths = self._photo_paths[:ind2] + self._photo_paths[ind1:]

        self._image_loader.preload(paths)

    def _load_image(self) -> None:
        image_path = self.image_path
        if self._current_image_path == image_path:
            return

        if image_path:
            self._input_frame.enable()
            self._scale.configure(state=tkinter.NORMAL)
            metadata = self._photo_data[image_path]
            try:
                caption = metadata_to_caption(
                    metadata=metadata,
                    order=self._settings.caption_order,
                    datetime_format=self._settings.caption_datetime_format)
            except KeyError as error:
                self._log_screen.error(f'Unknown caption field {error}')
                caption = ''

            self._input_frame.set_caption_text(caption)

            self._input_frame.visibility = str(metadata['privacy'])

            try:
                self._image_orig = self._image_loader.open(image_path)
            except ImageLoaderError as error:
                self._log_screen.error(f'Error on loading {image_path}:')
                self._log_screen.warning(str(error))
                self._image_orig = self._image_loader.open_truncated(image_path)

            exif = self._image_orig.getexif()
            orientation_tag = exif.get(self.exif_orientation_key, 0)
            if orientation_tag in (2, 4):
                self._image_orig = self._image_orig.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                orientation_tag -= 1

            if orientation_tag in (5, 7):
                self._image_orig = self._image_orig.transpose(PIL.Image.FLIP_)
                orientation_tag += 1

            if orientation_tag in EXIF_ORIENTATION_MAP:
                self._image_orig = self._image_orig.rotate(EXIF_ORIENTATION_MAP[orientation_tag], expand=True)

            new_text = f'{Path(image_path).name} [{self.index + 1}/{len(self._photo_paths)}]'
            self.configure(text=new_text)
        else:
            LOGGER.debug('Empty images list')
            self._input_frame.set_caption_text('')
            self._input_frame.visibility = ''
            self._image_orig = None
            self.configure(text=self.placeholder)
            self._scale.configure(state=tkinter.DISABLED)
            self._input_frame.disable()
        self.refresh()
        self._current_image_path = image_path
        self._try_to_preload_images()


class WrappedLabel(ttk.Label):
    """ Label widget which changes wraphlength to width of itself

    Needs to be fill='x' and expand=True in Pack to takes effect.
    """
    def __init__(
            self,
            master: tkinter.Widget,
            *args,
            attended_container: Optional[tkinter.Widget] = None,
            **kwargs):
        super().__init__(master, *args, **kwargs)

        if attended_container is None:
            attended_container = master

        attended_container.bind(
            '<Configure>',
            lambda _: self.configure(wraplength=self.winfo_width()),
            add=True)


class InputFrame(ttk.Frame):
    def __init__(self, master: MasterType) -> None:
        super().__init__(master)

        self._images_dir_var = tkinter.StringVar()
        self._metadata_dir_var = tkinter.StringVar()

        caption_frame = ttk.LabelFrame(self, text='Caption')
        self._caption = tkinter.Text(caption_frame, height=8)
        upload_frame = ttk.Frame(self, relief='flat',)
        visibility_frame = ttk.LabelFrame(upload_frame, relief=FRAME_RELIEF, text='Visibility')
        self._visibility_list = ttk.Combobox(
            visibility_frame,
            state='readonly',
            values=[i.value for i in PixelfedVisibility])
        self._button_upload = ttk.Button(upload_frame, text='Upload! (^U)')
        self._navigation_frame = ttk.Frame(self, relief='flat')
        self._button_prev = ttk.Button(self._navigation_frame, text='<< Prev (^P)')
        self._button_next = ttk.Button(self._navigation_frame, text='Next (^N) >>')
        images_dir_frame = ttk.LabelFrame(self, text='Images directory', relief=FRAME_RELIEF)
        metadata_dir_frame = ttk.LabelFrame(self, text='Metadata directory', relief=FRAME_RELIEF)
        self._button_open_metadata_dir = ttk.Button(metadata_dir_frame, text='Open')
        self._button_open_images_dir = ttk.Button(images_dir_frame, text='Open')
        images_dir_label = WrappedLabel(
            images_dir_frame, attended_container=self, justify='left', textvariable=self._images_dir_var)
        metadata_dir_label = WrappedLabel(
            metadata_dir_frame, attended_container=self, justify='left', textvariable=self._metadata_dir_var)

        images_dir_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        self._button_open_images_dir.pack(side=tkinter.LEFT, **PADDING_KWARGS, **BUTTON_IPADDING_KWARGS)
        images_dir_label.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, **PADDING_KWARGS)

        metadata_dir_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        self._button_open_metadata_dir.pack(side=tkinter.LEFT, **PADDING_KWARGS, **BUTTON_IPADDING_KWARGS)
        metadata_dir_label.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, **PADDING_KWARGS)

        caption_frame.pack(side='top', fill=tkinter.X, expand=True, **PADDING_KWARGS)
        self._caption.pack(fill=tkinter.X, expand=True, **PADDING_KWARGS)
        upload_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        visibility_frame.pack(side=tkinter.LEFT, **PADDING_KWARGS)
        self._visibility_list.pack(**PADDING_KWARGS)
        self._navigation_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        self._button_upload.pack(side=tkinter.RIGHT, **PADDING_KWARGS, **BUTTON_IPADDING_KWARGS)
        self._button_prev.pack(side=tkinter.LEFT, **PADDING_KWARGS, **BUTTON_IPADDING_KWARGS)
        self._button_next.pack(side=tkinter.RIGHT, **PADDING_KWARGS, **BUTTON_IPADDING_KWARGS)

    @property
    def dirs_are_stated(self) -> bool:
        return bool(self.images_dir and self.metadata_dir)

    @property
    def images_dir(self) -> Optional[str]:
        val = self._images_dir_var.get()
        if not val:
            return None
        self._metadata_dir_var.set(self._metadata_dir_var.get() or val)
        return val

    @images_dir.setter
    def images_dir(self, value: Optional[str]) -> None:
        if value is None:
            value = ''
        self._images_dir_var.set(value)

    @property
    def metadata_dir(self) -> Optional[str]:
        val = self._metadata_dir_var.get()
        if not val:
            return None
        self._images_dir_var.set(self._images_dir_var.get() or val)
        return val

    @metadata_dir.setter
    def metadata_dir(self, value: Optional[str]) -> None:
        if value is None:
            value = ''
        self._metadata_dir_var.set(value)

    @property
    def caption(self) -> str:
        return self._caption.get('0.1', tkinter.END).strip()

    @property
    def visibility(self) -> str:
        return self._visibility_list.get()

    @visibility.setter
    def visibility(self, value: str) -> None:
        if not value:
            self._visibility_list.set('')
            return
        flickr_vis = FlickrVisibility(value)
        visibility = PixelfedVisibility.from_flickr_visibility(flickr_vis)
        self._visibility_list.set(visibility.value)

    def button_set_command(self, name: str, callback: Callable[[], None]) -> None:
        but = getattr(self, f'_button_{name}')
        but.configure(command=callback)

    def set_caption_text(self, text: str) -> None:
        set_text_content(self._caption, text)

    def _set_state(self, enabled: bool) -> None:
        LOGGER.debug(f'Setting inputs to enabled={enabled}')
        text_state: Any
        if enabled:
            state = 'enabled'
            text_state = tkinter.NORMAL
            list_state = 'readonly'
            bg_color = 'white'
        else:
            state = tkinter.DISABLED
            text_state = state
            list_state = state
            bg_color = 'darkgray'
        self._caption.configure(state=text_state, background=bg_color)
        self._visibility_list.configure(state=list_state)
        self._button_upload.configure(state=state)
        self._button_prev.configure(state=state)
        self._button_next.configure(state=state)

    def enable(self) -> None:
        self._set_state(enabled=True)

    def disable(self) -> None:
        self._set_state(enabled=False)


class Settings(ttk.Frame):
    default_caption_order = DEFAULT_CAPTION_ORDER
    default_caption_datetime_format = '%c'

    def __init__(
            self,
            master: tkinter.Widget,
            config_path: Path,
            on_change_callback: Callable[[], None]) -> None:
        super().__init__(master=master, relief=FRAME_RELIEF)

        self._on_change = on_change_callback

        self.config_path = config_path

        inner_frame = ttk.Frame(self, relief=tkinter.FLAT, width=50)

        self._instance_var = tkinter.StringVar()
        self._caption_order_var = tkinter.StringVar()
        self._caption_datetime_format_var = tkinter.StringVar()
        self._ignore_ssl_var = tkinter.BooleanVar()

        token_frame = ttk.LabelFrame(inner_frame, text='Pixelfed token')
        self._token_field = tkinter.Text(token_frame, height=15)

        instance_frame = ttk.Frame(inner_frame)
        instance_label = ttk.Label(instance_frame, text='Pixelfed instance URL: ')
        self._instance_field = tkinter.Entry(instance_frame, textvariable=self._instance_var)
        ignore_ssl_checkbox = ttk.Checkbutton(instance_frame, text='Ignore SSL', variable=self._ignore_ssl_var)

        caption_frame = ttk.Frame(inner_frame)
        caption_order_label = ttk.Label(caption_frame, text='Caption order: ')
        self._caption_order_field = tkinter.Entry(caption_frame, textvariable=self._caption_order_var)
        caption_datetime_format_label = ttk.Label(caption_frame, text='Datetime format: ')
        self._caption_datetime_format_field = tkinter.Entry(
            caption_frame,
            textvariable=self._caption_datetime_format_var,
            width=15)

        self._style = ttk.Style(self)
        theme_wrapper = ttk.Frame(inner_frame)
        theme_frame = ttk.LabelFrame(theme_wrapper, text='Theme')
        self._theme_list = ttk.Combobox(
            theme_frame,
            state='readonly',
            values=self._style.theme_names())

        buttons_frame = ttk.Frame(inner_frame)
        save_button = ttk.Button(buttons_frame, text='Save', command=self.save_action)
        cancel_button = ttk.Button(buttons_frame, text='Cancel', command=self.cancel_action)

        self._init_values()

        # Pack!
        inner_frame.pack(**PADDING_KWARGS)

        instance_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        instance_label.pack(side=tkinter.LEFT, expand=False, **PADDING_KWARGS)
        self._instance_field.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, **PADDING_KWARGS)
        ignore_ssl_checkbox.pack(side=tkinter.LEFT, expand=False, **PADDING_KWARGS)

        caption_frame.pack(fill=tkinter.X, **PADDING_KWARGS)
        caption_order_label.pack(side=tkinter.LEFT, expand=False, **PADDING_KWARGS)
        self._caption_order_field.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, **PADDING_KWARGS)
        caption_datetime_format_label.pack(side=tkinter.LEFT, **PADDING_KWARGS)
        self._caption_datetime_format_field.pack(side=tkinter.LEFT, fill=tkinter.X, **PADDING_KWARGS)

        token_frame.pack(**PADDING_KWARGS)
        self._token_field.pack(fill='both', **PADDING_KWARGS)

        theme_wrapper.pack(fill=tkinter.X, **PADDING_KWARGS)
        theme_frame.pack(side=tkinter.LEFT, expand=False, **PADDING_KWARGS)
        self._theme_list.pack(**PADDING_KWARGS)

        ttk.Separator(inner_frame).pack(fill=tkinter.X, **PADDING_KWARGS*5)

        buttons_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X, **PADDING_KWARGS)
        cancel_button.pack(side=tkinter.LEFT, **PADDING_KWARGS)
        save_button.pack(side=tkinter.RIGHT, **PADDING_KWARGS)

    @property
    def token(self) -> str:
        return self._token_field.get('0.1', tkinter.END).strip()

    @property
    def instance(self) -> str:
        return self._instance_var.get()

    @property
    def caption_order(self) -> str:
        return self._caption_order_var.get()

    @property
    def caption_datetime_format(self) -> str:
        return self._caption_datetime_format_var.get()

    @property
    def is_sufficient(self) -> bool:
        LOGGER.debug(f'Sufficience: instance is {self.instance} and {self.token}')
        return bool(self.instance and self.token)

    @property
    def theme(self) -> str:
        return self._theme_list.get()

    @property
    def ignore_ssl(self) -> bool:
        return self._ignore_ssl_var.get()

    def save_action(self) -> None:
        data = {
            'instance': self.instance,
            'token': self.token,
            'caption_order': self.caption_order,
            'caption_datetime_format': self.caption_datetime_format,
            'ignore_ssl_verify': self.ignore_ssl,
            'theme': self.theme
        }
        self._style.theme_use(self.theme)
        set_custom_themes()
        self._on_change()
        save_config(self.config_path, data, create_missing=True)

    def cancel_action(self) -> None:
        self._init_values()

    def _init_values(self) -> None:
        config = load_config(self.config_path, create_missing=True)
        self._instance_var.set(config.get('instance', ''))
        self._caption_order_var.set(config.get('caption_order', self.default_caption_order))
        self._caption_datetime_format_var.set(
            config.get('caption_datetime_format', self.default_caption_datetime_format))
        set_text_content(self._token_field, config.get('token'))
        self._ignore_ssl_var.set(config.get('ignore_ssl_verify', False))
        current_theme = config.get('theme') or self._style.theme_use()
        self._theme_list.set(current_theme)
        self._style.theme_use(current_theme)


class LogScreen(scrolledtext.ScrolledText):
    class MessageType(enum.Enum):
        SUCCESS = 'success'
        NORMAL = 'normal'
        WARNING = 'warning'
        ERROR = 'error'

    def __init__(self, master: tkinter.Widget):
        super().__init__(
            master,
            state=tkinter.DISABLED,
            background='black',
            foreground='white')
        self._link_counter = 0
        self.tag_config(self.MessageType.SUCCESS.value, foreground='pale green')
        self.tag_config(self.MessageType.NORMAL.value, foreground='grey')
        self.tag_config(self.MessageType.WARNING.value, foreground='yellow')
        self.tag_config(self.MessageType.ERROR.value, foreground='indian red')

        clear_log_button = ttk.Button(
            self, style='ClearButton.TButton', text='rm', command=self.clear)

        clear_log_button.pack(side=tkinter.TOP, anchor=tkinter.NE, **PADDING_KWARGS)

    def _print(self, text: str, tag: str) -> None:
        self.configure(state=tkinter.NORMAL)
        self.insert(tkinter.END, text.rstrip() + '\n', tag)
        self.configure(state=tkinter.DISABLED)
        self.see(tkinter.END)

    def clear(self) -> None:
        self.configure(state=tkinter.NORMAL)
        self.delete('1.0', tkinter.END)
        self.configure(state=tkinter.DISABLED)

    def print(self, text: str, message_type: MessageType) -> None:
        self._print(text, message_type.value)

    def success(self, text: str) -> None:
        self.print(text, self.MessageType.SUCCESS)

    def note(self, text: str) -> None:
        self.print(text, self.MessageType.NORMAL)

    def warning(self, text: str) -> None:
        self.print(text, self.MessageType.WARNING)

    def error(self, text: str) -> None:
        self.print(text, self.MessageType.ERROR)

    def url(self, url: str, text='') -> None:
        tag = f'{url}-{self._link_counter}'
        self.tag_config(tag, foreground='DodgerBlue', underline=True)
        self.tag_bind(tag, '<Button-1>', lambda event: self._open_link(url))
        self.tag_bind(tag, '<Enter>', lambda event: self.configure(cursor='hand1'))
        self.tag_bind(tag, '<Leave>', lambda event: self.configure(cursor=''))
        self._link_counter += 1
        self._print(text or url, tag)

    def _open_link(self, url: str) -> None:
        webbrowser.open(url)


class Application(tkinter.Tk):
    state_file_path = xdg_base_dirs.xdg_data_home() / APP_NAME.lower() / 'last_state.yaml'
    loop_period = 1/100
    update_gui_task_name = 'Update GUI'
    tab_main_index = 0
    tab_settings_index = 1

    def __init__(self, config_path: Path, debug=False, safe_mode=False) -> None:
        super().__init__(sync=debug)

        self._loop = asyncio.get_event_loop()
        self._loop.create_task(self._update(), name=self.update_gui_task_name)

        self.title(APP_NAME)

        self._notebook = ttk.Notebook(self)
        main_frame = ttk.Frame(self._notebook)
        settings_tab = ttk.Frame(self._notebook)
        self._settings_is_active = False

        self._notebook.add(main_frame, text='Main')
        self._notebook.add(settings_tab, text='Settings')

        side_frame = ttk.Frame(main_frame, width=SIDE_FRAME_WIDTH)
        side_frame.pack_propagate(False)
        self._input_frame = InputFrame(side_frame)
        self._settings_frame = Settings(settings_tab, config_path, self.init_pixelfed_client)
        log_screen_frame = ttk.LabelFrame(side_frame, text='Messages', relief=FRAME_RELIEF)
        self._log_screen = LogScreen(log_screen_frame)

        image_loader: BaseImageLoader
        if safe_mode:
            image_loader = ImageLoader()
        else:
            image_loader = CachingImageLoader(debug=debug, cached_files_limit=CACHED_FILES_LIMIT)
        self._image_loader_stop_callback = image_loader.stop

        self._image = Image(
            main_frame,
            self._input_frame,
            self._settings_frame,
            self._log_screen,
            image_loader)

        self._load_state()
        self.init_pixelfed_client()

        self.protocol('WM_DELETE_WINDOW', self._on_exit)

        self._notebook.bind('<<NotebookTabChanged>>', self._on_tab_change)
        self.bind('<Control-n>', KeypressWrapper(self, self._image.next))
        self.bind('<Control-p>', KeypressWrapper(self, self._image.prev))
        self.bind('<Control-u>', KeypressWrapper(self, self._create_upload_task))
        self.bind('<Control-q>', self.exit)

        self._input_frame.button_set_command('prev', self._image.prev)
        self._input_frame.button_set_command('next', self._image.next)
        self._input_frame.button_set_command('open_images_dir', self._open_images_dir)
        self._input_frame.button_set_command('open_metadata_dir', self._open_metadata_dir)
        self._input_frame.button_set_command('upload', self._create_upload_task)

        self._notebook.pack(fill=tkinter.BOTH, expand=True, **PADDING_KWARGS)
        self._image.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, **PADDING_KWARGS)
        side_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=False, **PADDING_KWARGS)
        self._input_frame.pack(fill=tkinter.X, **PADDING_KWARGS * 0)
        log_screen_frame.pack(fill=tkinter.BOTH, expand=True, **PADDING_KWARGS)
        self._log_screen.pack(fill=tkinter.BOTH, expand=True, **PADDING_KWARGS)
        self._settings_frame.pack(**PADDING_KWARGS*5)

        set_custom_themes()

        if debug:
            self._log_screen.success('SUCCESS')
            self._log_screen.note('NOTE')
            self._log_screen.warning('WARNING')
            self._log_screen.error('ERROR')
            self._log_screen.url('https://example.com', text='CLICKME')

        if not self._settings_frame.is_sufficient:
            self._notebook.select(tab_id=self.tab_settings_index)

    def run(self) -> None:
        self.willdispatch()
        self._loop.run_forever()

    def exit(self, _: tkinter.Event) -> None:
        self._on_exit()

    def init_pixelfed_client(self) -> None:
        self._pixelfed_client = PixelfedClient(
            base_url=self._settings_frame.instance,
            token=self._settings_frame.token,
            strict_ssl=not self._settings_frame.ignore_ssl)

    async def _update(self) -> None:
        while True:
            self.update()
            await asyncio.sleep(self.loop_period)

    def _on_tab_change(self, _: tkinter.Event) -> None:
        tab = self._notebook.select()
        tab_index = self._notebook.index(tab)

        if tab_index == self.tab_settings_index:
            self._settings_is_active = True
        else:
            if self._settings_is_active:
                LOGGER.debug('Cancel unsaved changes of setting')
                self._settings_frame.cancel_action()
            self._settings_is_active = False

        if tab_index == self.tab_main_index:
            LOGGER.debug('Reloading image after switching to main tab')
            self._image.reload()

    def _open_images_dir(self) -> None:
        directory = filedialog.askdirectory(
            parent=self, title='Images directory')
        if not directory:
            return
        self._input_frame.images_dir = directory
        if not self._input_frame.metadata_dir:
            self._input_frame.metadata_dir = directory
        self._image.change_path()

    def _open_metadata_dir(self) -> None:
        directory = filedialog.askdirectory(
            parent=self, title='Metadata directory')
        if not directory:
            return
        self._input_frame.metadata_dir = directory
        if not self._input_frame.images_dir:
            self._input_frame.images_dir = directory
        self._image.change_path()

    def _create_upload_task(self) -> None:
        self._loop.create_task(self._upload(), name='Upload')

    async def _upload(self) -> None:
        assert self._image.image_path

        img_path = self._image.image_path
        img_name = Path(img_path).name
        caption = self._input_frame.caption
        visibility = PixelfedVisibility(self._input_frame.visibility)

        task = asyncio.current_task()
        assert task
        task.set_name(f'Upload {img_name}')

        self._log_screen.note(f'Uploading {img_name}...')
        self._image.next()

        try:
            url = await self._pixelfed_client.create_post(img_path, caption=caption, visibility=visibility)
        except PixelfedClientError as error:
            self._log_screen.error(f'Failed to upload {img_name}:')
            self._log_screen.error(str(error))
        else:
            self._log_screen.success(f'Image {img_name} posted')
            self._log_screen.url(url)

    def _on_exit(self) -> None:
        self._image_loader_stop_callback()
        LOGGER.info(f'Saving state file {self.state_file_path}')
        data = {
            'images_dir': self._input_frame.images_dir,
            'metadata_dir': self._input_frame.metadata_dir,
            'image_path': self._image.image_path,
        }
        for task in asyncio.all_tasks():
            name = task.get_name()
            if name == self.update_gui_task_name:
                LOGGER.info(f'Cancelling task {task.get_name()}')
            else:
                LOGGER.warning(f'Cancelling task {task.get_name()}')
            task.cancel()
        self._loop.stop()
        save_config(self.state_file_path, data, create_missing=True)
        self.destroy()

    def _load_state(self) -> None:
        data = load_config(self.state_file_path, create_missing=True)
        self._input_frame.images_dir = data.get('images_dir')
        self._input_frame.metadata_dir = data.get('metadata_dir')
        if self._input_frame.dirs_are_stated:
            self._image.change_path()
            self._image.seek_image(data.get('image_path'))


def get_argparser() -> argparse.ArgumentParser:
    default_config_path = xdg_base_dirs.xdg_config_home() / APP_NAME.lower() / 'config.yaml'

    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description='Import Flickr data into a Pixelfed account',
        epilog=None)
    parser.add_argument(
        '-c', '--config-file',
        type=Path,
        default=Path(default_config_path),
        help='Alterative path to config')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Debug mode')
    parser.add_argument(
        '-s', '--safe-mode',
        action='store_true',
        help='Disables some perfomance featrues to avoid IO troubles')

    argcomplete.autocomplete(parser)
    return parser


def main() -> None:
    locale.setlocale(locale.LC_TIME, locale.getlocale())
    args = get_argparser().parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    app = Application(args.config_file, debug=args.verbose, safe_mode=args.safe_mode)
    app.run()
