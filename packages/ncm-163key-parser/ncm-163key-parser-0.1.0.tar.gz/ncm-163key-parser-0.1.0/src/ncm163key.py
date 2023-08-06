# -*- coding: utf-8 -*-
# from __future__ import annotations
import base64 as _base64
import json as _json
import re as _re
from functools import wraps as _wraps
from reprlib import repr as _shortrepr
from string import Template
from typing import Any as _Any
from typing import Callable as _Callable
from typing import Final as _Final
from typing import Iterable as _Iterable
from typing import Iterator as _Iterator
from typing import Mapping as _Mapping
from typing import MutableMapping as _MutableMapping
from typing import MutableSequence as _MutableSequence
from typing import NamedTuple as _NamedTuple
from typing import SupportsIndex as _SupportsIndex
from typing import TypeVar as _TypeVar
from typing import Union as _Union
from typing import overload as _overload

import attrs as _attrs
import pyaes as _pyaes
from typing_extensions import Self as _Self
from typing_extensions import TypeAlias as _TypeAlias

__VERSION__ = '0.1.0'


class _VersionInfo(_NamedTuple):
    major: int
    minor: int
    micro: int


__VERSION_INFO__ = _VersionInfo(0, 1, 0)

_T: _TypeAlias = _TypeVar('_T')

_DEFAULT_ID_KEY: _Final[bytes] = b'\x23\x31\x34\x6c\x6a\x6b\x5f\x21\x5c\x5d\x26\x30\x55\x3c\x27\x28'


def version() -> str:
    return __VERSION__


def version_info() -> _VersionInfo:
    return __VERSION_INFO__


class Error(Exception):
    pass


class Warn(Warning):
    pass


class CryptOperationError(Error):
    pass


class MetadataParseError(Error):
    pass


def _gen_aes_128_ecb_cipher(key: bytes) -> _pyaes.AESModeOfOperationECB:
    if len(key) != 16:
        raise ValueError(f'invalid key size: should be 16, not {len(key)}')

    return _pyaes.AESModeOfOperationECB(key)


def _aes_mode_ecb_decrypt(key: bytes, ciphered: bytes) -> bytes:
    text_blksize = 16

    cipher = _gen_aes_128_ecb_cipher(key)

    # 解密
    ciphertext = bytes(ciphered)
    plaintext = bytearray()
    total_len = len(ciphertext)
    pos = 0
    while pos < total_len:
        plaintext.extend(cipher.decrypt(ciphertext[pos:pos + text_blksize]))
        pos += text_blksize

    # 去除明文后部的填充
    if len(plaintext) % text_blksize != 0:
        raise CryptOperationError('corrupted cipher text: invalid length')
    pad_len = plaintext[-1]
    if pad_len > text_blksize:
        raise CryptOperationError('corrupted cipher text: invalid padding byte')

    return bytes(plaintext[:-pad_len])


def _aes_mode_ecb_encrypt(key: bytes, plain: bytes) -> bytes:
    text_blksize = 16

    cipher = _gen_aes_128_ecb_cipher(key)

    # 填充明文，使其长度达到块大小的整数倍
    plaintext = bytes(plain)
    pad_len = text_blksize - (len(plaintext) % text_blksize)
    plaintext += bytes([pad_len] * pad_len)

    # 加密
    ciphertext = bytearray()
    total_len = len(plaintext)
    pos = 0
    while pos < total_len:
        ciphertext.extend(cipher.encrypt(plaintext[pos:pos + text_blksize]))
        pos += text_blksize

    return bytes(ciphertext)


def _load_metadata_json_object_hook(d: dict) -> dict:
    if 'artist' in d:
        artist: list[list[_Union[str, int]]] = d['artist']
        if isinstance(artist, list):
            d['artist'] = _ArtistsMapping({k: v for k, v in artist})
    return d


def _dump_metadata_json_unserializable(obj) -> _Union[dict, list, str, int, bool]:
    if isinstance(obj, _ArtistsMapping):
        return list(obj.items())
    elif isinstance(obj, _StrOnlySequence):
        return list(obj)
    raise TypeError(f'Object of type {type(obj).__name__!s} is not JSON serializable')


class _ArtistsMapping(_MutableMapping[str, int]):
    @_overload
    def __init__(self, mapping: _Mapping[str, int] = ..., /, **kwargs: int) -> None:
        ...

    @_overload
    def __init__(self, iterable: _Iterable[tuple[str, int]] = ..., /, **kwargs: int):
        ...

    @_overload
    def __init__(self, **kwargs: int) -> None:
        ...

    def __init__(self, initial=None, /, **kwargs) -> None:
        self.__data: dict[str, int] = {}
        if initial is not None:
            self.update(initial)
        if kwargs:
            self.update(kwargs)

    @classmethod
    def __verify_value_as_key(cls, key) -> str:
        if not isinstance(key, str):
            raise TypeError(
                f'non-str object are not available for the mapping keys: {key!r} ({type(key).__name__!r})'
            )
        return str(key)

    @classmethod
    def __verify_value_as_value(cls, key, value) -> int:
        if not isinstance(value, int):
            raise TypeError(
                f'non-int object are not available for the mapping values: {value!r} '
                f'({type(value).__name__!r}, key={key!r})'
            )
        return int(value)

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, key, /) -> int:
        if key in self.__data:
            return self.__data[key]
        if hasattr(self.__class__, '__missing__'):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: int, /) -> None:
        key = self.__verify_value_as_key(key)
        value = self.__verify_value_as_value(key, value)
        self.__data[key] = value

    def __delitem__(self, key, /) -> None:
        del self.__data[key]

    def __iter__(self) -> _Iterator:
        return iter(self.__data)

    def __contains__(self, key, /) -> bool:
        return key in self.__data

    def __repr__(self) -> str:
        return repr(self.__data)


class _StrOnlySequence(_MutableSequence[str]):
    @_overload
    def __init__(self) -> None:
        ...

    @_overload
    def __init__(self, iterable: _Iterable[str], /) -> None:
        ...

    def __init__(self, initial=None, /) -> None:
        self.__data: list[str] = []
        if initial is not None:
            if isinstance(initial, str):
                raise TypeError("initial iterable cannot be 'str'")
            elif isinstance(initial, type(self.__data)):
                self[:] = initial
            elif isinstance(initial, type(self)):
                if hasattr(initial, '__data'):
                    self[:] = initial.__data
                else:  # 使用特殊措施访问 initial 的私有变量 __data
                    self[:] = getattr(initial, f'_{type(initial).__name__}__data')
            else:
                self[:] = list(initial)

    @classmethod
    def __verify_value_as_member(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError(f"only 'str' object can be a member of the sequence, not {type(v).__name__!r}")
        return v

    def __len__(self) -> int:
        return len(self.__data)

    def insert(self, index: _SupportsIndex, value: str, /) -> None:
        self.__data.insert(index, self.__verify_value_as_member(value))

    @_overload
    def __getitem__(self, index: _SupportsIndex, /) -> str:
        ...

    @_overload
    def __getitem__(self, slice_: slice, /) -> _Self:
        ...

    def __getitem__(self, index_or_slice: _Union[_SupportsIndex, slice], /) -> _Union[str, _Self]:
        if isinstance(index_or_slice, slice):
            return type(self)(self.__data[index_or_slice])
        return self.__data[index_or_slice]

    @_overload
    def __setitem__(self, index: _SupportsIndex, value: str, /) -> None:
        ...

    @_overload
    def __setitem__(self, slice_: slice, value: _Iterable[str], /) -> None:
        ...

    def __setitem__(self, index_or_slice: _Union[_SupportsIndex, slice], value: _Union[str, _Iterable[str]], /) -> None:
        if isinstance(index_or_slice, slice):
            self.__data[index_or_slice] = (self.__verify_value_as_member(_) for _ in value)
        else:
            self.__data[index_or_slice] = self.__verify_value_as_member(value)

    def __delitem__(self, index_or_slice: _Union[_SupportsIndex, slice], /) -> None:
        del self.__data[index_or_slice]

    def __repr__(self) -> str:
        return repr(self.__data)


_METADATA_COMMON_FIELD_NAMES: _Final[set[str]] = {
    'album',
    'albumId',
    'albumPic',
    'albumPicDocId',
    'alias',
    'artist',
    'bitrate',
    'duration',
    'format',
    'musicId',
    'musicName',
    'mvId',
    'transNames'
}
_METADATA_ANDROID_FIELD_NAMES: _Final[set[str]] = _METADATA_COMMON_FIELD_NAMES | {
    'flag',
    'gain'
}
_METADATA_PCv1_NCM_FIELD_NAMES: _Final[set[str]] = _METADATA_COMMON_FIELD_NAMES | {
    'flag',
    'mp3DocId'
}
_METADATA_PCv1_FREE_FIELD_NAMES: _Final[set[str]] = _METADATA_COMMON_FIELD_NAMES | {
    'mp3DocId'
}
_METADATA_PCv2_FIELD_NAMES: _Final[set[str]] = _METADATA_COMMON_FIELD_NAMES | {
    'fee',
    'mp3DocId',
    'privilege'
}
_METADATA_PCv2_PRIVILEGES_FIELD_NAMES: _Final[set[str]] = {
    'flag'
}

_ILLEGAL_FN_CHAR_EXCEPT_SLASH_PATTERN: _Final[_re.Pattern] = _re.compile(r"""[<>:"|\\?*\x00-\x1f]""",
                                                                         flags=_re.IGNORECASE
                                                                         )


def _make_filename_safe_string(s: str) -> str:
    return _ILLEGAL_FN_CHAR_EXCEPT_SLASH_PATTERN.sub('_', s).replace('/', '／')


def _prettify_raised_TypeError(validator: _Callable) -> _Callable[[_Any, _attrs.Attribute, _Any], _Any]:
    """用于美化 ``attrs.validators`` 内置的验证器引发的 TypeError 错误信息。"""

    @_wraps(validator)
    def wrapped(self: _Any, attr: _attrs.Attribute, value: _Any):
        try:
            return validator(self, attr, value)
        except TypeError as exc:
            raise TypeError(exc.args[0])

    return wrapped


@_attrs.define(kw_only=True)
class NCMMusicMetadata:
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类以及子类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类为本模块类其他所有元数据类的子类，这些子类是特别设计的，
    以应对来自不同平台和版本网易云音乐客户端的文件中元数据的差异。

    本类的所有属性也是所有文件的元数据所共有的。

    Attributes:
        format (str):
          歌曲的格式。一般为 ``flac`` 或 ``mp3``。不可包含任何 Windows 保留字符。
        musicId (int):
          歌曲 ID。仅在网易云音乐平台有意义。
        musicName (str):
          歌曲名称（标题）。
        artist (Mapping[str, int]):
          参与创作歌曲的歌手和对应 ID 的映射表，键为歌手名称（``str``），对应的值为歌手 ID（``int``）。
          歌手 ID 仅在网易云音乐平台有意义。

          实例方法 ``artist_prettify()`` 可用于美化歌手列表的显示，它使用参数
          ``sep`` 作为分隔符，将所有歌手名称拼接成一个字符串并返回。
        album (str):
          歌曲所属的专辑名称。
        albumId (str):
          歌曲所属的专辑 ID。仅在网易云音乐平台有意义。
        albumPicDocId (int):
          歌曲所属的专辑封面 ID。仅在网易云音乐平台有意义。
        albumPic (str):
          专辑封面的下载链接。
        mvId (int):
          歌曲的 MV（如果有的话）被分配的 ID。仅在网易云音乐平台有意义。
          此属性默认值为 0，以应对歌曲没有 MV 的情况。
        bitrate (int):
          歌曲的平均比特率，单位为比特。

          只读属性 ``kilo_bitrate`` 的值与此属性同步变化，它是此属性除以 1000 后的得数，单位为千比特。
        duration (int):
          歌曲的长度，单位为毫秒。

          只读属性 ``duration_seconds`` 的值与此属性同步变化，它是此属性除以 1000 后的得数，单位为秒。
        alias (list[str]):
          歌曲在网易云音乐平台的别名。
        transNames (list[str]):
          歌曲的标题在网易云音乐平台的翻译。
    """
    musicName: str = _attrs.field(default='',
                                  validator=_prettify_raised_TypeError(_attrs.validators.instance_of(str))
                                  )
    musicId: int = _attrs.field(default=0,
                                validator=_prettify_raised_TypeError(
                                    _attrs.validators.and_(_attrs.validators.instance_of(int),
                                                           _attrs.validators.ge(0)
                                                           )
                                )
                                )
    artist: _Union[_Mapping[str, int], _ArtistsMapping] = _attrs.field(
        factory=_ArtistsMapping,
        converter=lambda _: _ArtistsMapping(_) if isinstance(_, (_Mapping, _Iterable)) else _,
        validator=_prettify_raised_TypeError(_attrs.validators.instance_of(_ArtistsMapping))
    )
    album: str = _attrs.field(default='', validator=_prettify_raised_TypeError(_attrs.validators.instance_of(str)))
    albumId: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))
    albumPic: str = _attrs.field(default='', validator=_prettify_raised_TypeError(_attrs.validators.instance_of(str)))
    albumPicDocId: int = _attrs.field(default=0,
                                      validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int))
                                      )
    bitrate: int = _attrs.field(default=0,
                                validator=_prettify_raised_TypeError(
                                    _attrs.validators.and_(
                                        _attrs.validators.instance_of(int),
                                        _attrs.validators.ge(0)
                                    )
                                )
                                )
    duration: int = _attrs.field(default=0,
                                 validator=_prettify_raised_TypeError(
                                     _attrs.validators.and_(
                                         _attrs.validators.instance_of(int),
                                         _attrs.validators.ge(0)
                                     )
                                 )
                                 )
    mvId: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))
    alias: _StrOnlySequence = _attrs.field(
        factory=_StrOnlySequence,
        converter=lambda _: _StrOnlySequence(_) if isinstance(_, _Iterable) else _,
        validator=_prettify_raised_TypeError(_attrs.validators.instance_of(_StrOnlySequence))
    )
    transNames: _StrOnlySequence = _attrs.field(
        factory=_StrOnlySequence,
        converter=lambda _: _StrOnlySequence(_) if isinstance(_, _Iterable) else _,
        validator=_prettify_raised_TypeError(_attrs.validators.instance_of(_StrOnlySequence))
    )
    format: str = _attrs.field(
        default='',
        validator=_prettify_raised_TypeError(
            _attrs.validators.and_(
                _attrs.validators.instance_of(str),
                _attrs.validators.matches_re(r"""^((?![<>:"|\\?*\x00-\x1f/.]|\s).)*$""", flags=_re.IGNORECASE)
            )
        )
    )
    _orig_metadata_field_names_ordered: tuple[str] = _attrs.field(
        factory=tuple,
        validator=_prettify_raised_TypeError(
            _attrs.validators.and_(
                _attrs.validators.instance_of(tuple),
                _attrs.validators.deep_iterable(
                    member_validator=_attrs.validators.instance_of(str)
                )
            )
        ),
        repr=False
    )

    def artist_prettify(self, *, sep: str = None) -> str:
        """美化属性 ``artist``，使用指定的分隔符 ``sep``，将所有歌手名称拼接成一个字符串并返回。

        默认使用顿号“、”作为分隔符。
        """
        if sep is None:
            sep = '、'
        elif not isinstance(sep, str):
            raise TypeError(f"seperator must be 'str', not {type(sep).__name__!r}")

        return sep.join(self.artist)

    def generate_filename(self, *, artist_sep: str = None, fmt: str = None) -> str:
        """根据元数据生成歌曲文件名。

        根据你使用的格式化字符串（见下文），将会使用的信息：

        - 歌曲名称 - 属性 ``musicName``
        - 歌手列表 - 方法 ``self.artist_prettify()``，通过参数 ``artist_sep`` 自定义分隔符
        - 专辑名称 - 属性 ``album``
        - 歌曲格式 - 属性 ``format``，用作文件扩展名；如果为空字符串，则将使用“unknown”

        参数 ``fmt`` 为一个格式化字符串，决定文件名的格式。默认为：``'${title} - ${artists}'``。
        如果需要自定义文件名格式，以下是可用的变量：

        - ``${title}`` - 歌曲标题
        - ``${artists}`` - 歌手列表
        - ``${album}`` - 专辑名称

        将会使用 ``string.Template(fmt).safe_substitude(...)`` 生成文件名；歌曲格式会作为文件扩展名自动附加在末尾。

        生成的文件名中，所有 Windows 保留字符将会被替换为下划线“_”（斜杠“/”除外，它会被替换为全宽斜线符号“／”）。
        """
        if fmt is None:
            fmt = '${title} - ${artists}'
        elif not isinstance(fmt, str):
            raise TypeError(f"filename template string must be 'str', not {type(fmt).__name__!r}")

        tmpl = Template(fmt)
        ret = tmpl.safe_substitute(title=self.musicName,
                                   artists=self.artist_prettify(sep=artist_sep),
                                   album=self.album
                                   )

        return f"{_make_filename_safe_string(ret)}.{self.format.lower()}"

    @property
    def kilo_bitrate(self) -> float:
        """属性 ``bitrate`` 除以 1000 后的得数。与属性 ``bitrate`` 同步变化。"""
        return self.bitrate / 1000

    @property
    def duration_seconds(self) -> float:
        """属性 ``duration`` 除以 1000 后的得数，单位为秒。与属性 ``duration`` 同步变化。"""
        return self.duration / 1000

    def _dump_self_as_dict(self) -> dict[str, _Any]:
        metadata_dict = _attrs.asdict(self, filter=lambda attr, _: not attr.name.startswith('_'))
        return metadata_dict

    @classmethod
    def _convert_metadata_dict_to_json(cls, metadata_dict: dict[str, _Any]) -> str:
        return _json.dumps(metadata_dict,
                           ensure_ascii=False,
                           separators=(',', ':'),
                           allow_nan=False,
                           default=_dump_metadata_json_unserializable
                           ).replace('/', '\\/')

    def dump(self, *, alter_id_key: _Union[bytes, bytearray] = None) -> str:
        """将当前元数据对象还原为标识符。

        请注意，即使在不修改 ``metadata`` 的情况下，也会出现还原的标识符和原标识符不一致的情况，
        即 ``dump(load(identifier, alter_id_key=id_key), alter_id_key=id_key) == identifier``
        不一定为真值。

        返回的标识符总是 ``str`` 对象，如果需要写入二进制文件，你需要自行编码为字节对象。

        Args:
            alter_id_key (bytes): 自定义元数据加密密钥。仅在生成自制的标识符时需要使用。
        """
        if alter_id_key is None:
            id_key = bytes(_DEFAULT_ID_KEY)
        else:
            try:
                memoryview(alter_id_key)
            except TypeError:
                raise TypeError(
                    f"a bytes-like object or None is required for argument 'alter_id_key', "
                    f"not {type(alter_id_key).__name__!r}"
                )
            else:
                id_key = bytes(alter_id_key)

        # 重排键值对顺序
        dumped_metadata_dict = self._dump_self_as_dict()
        final_metadata_dict = {}
        for k in self._orig_metadata_field_names_ordered:
            final_metadata_dict[k] = dumped_metadata_dict[k]
        for k in (set(dumped_metadata_dict) - set(self._orig_metadata_field_names_ordered)):
            final_metadata_dict[k] = dumped_metadata_dict[k]

        metadata_json_stage1 = self._convert_metadata_dict_to_json(final_metadata_dict)
        metadata_json_stage2 = f'music:{metadata_json_stage1!s}'.encode('UTF-8')
        identifier_stage1 = _aes_mode_ecb_encrypt(id_key, metadata_json_stage2)
        identifier_stage2 = _base64.b64encode(identifier_stage1)
        identifier = b"163 key(Don't modify):" + identifier_stage2

        return str(identifier, encoding='ASCII')


@_attrs.define(kw_only=True)
class NCMMusicMetadataForAndroid(NCMMusicMetadata):
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类仅适用于来自网易云音乐安卓客户端的文件的元数据。以下只列出其独有属性；
    要查看共有属性，请查阅 ``NCMMusicMetadata`` 的文档。

    Attributes:
        flag (int): 功能未知。
        gain (float): 歌曲的响度。
    """
    flag: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))
    gain: float = _attrs.field(factory=float,
                               validator=_prettify_raised_TypeError(_attrs.validators.instance_of(float)),
                               converter=lambda _: float(_) if isinstance(_, int) else _
                               )


@_attrs.define
class NCMMusicMetadataForPC(NCMMusicMetadata):
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类仅适用于来自网易云音乐 PC 客户端的文件的元数据。以下只列出其独有属性；
    要查看共有属性，请查阅 ``NCMMusicMetadata`` 的文档。

    Attributes:
        mp3DocId (str): 作用未知。
    """
    mp3DocId: str = _attrs.field(default='', validator=_prettify_raised_TypeError(_attrs.validators.instance_of(str)))

    def _dump_self_as_dict(self) -> dict[str, _Any]:
        metadata_dict = super()._dump_self_as_dict()
        metadata_dict['albumPicDocId'] = str(metadata_dict['albumPicDocId'])
        return metadata_dict

    def _convert_metadata_dict_to_json(cls, metadata_dict: dict[str, _Any]) -> str:
        # PC端和安卓端不同，不需要为斜杠使用反斜杠转义
        return _json.dumps(metadata_dict,
                           ensure_ascii=False,
                           separators=(',', ':'),
                           allow_nan=False,
                           default=_dump_metadata_json_unserializable
                           )


@_attrs.define(kw_only=True)
class NCMMusicMetadataForPCv1Free(NCMMusicMetadataForPC):
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类仅适用于来自网易云音乐 PC 客户端的**无加密文件**的元数据。
    """


@_attrs.define(kw_only=True)
class NCMMusicMetadataForPCv1NCM(NCMMusicMetadataForPC):
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类仅适用于来自网易云音乐 PC 客户端的**加密文件**的元数据。以下只列出其独有属性；
    要查看共有属性，请查阅 ``NCMMusicMetadataForPC`` 和 ``NCMMusicMetadata`` 的文档。

    Attributes:
        flag (int): 作用未知。
    """
    flag: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))


@_attrs.define(kw_only=True)
class _MetadataPrivileges:
    """本类的实例用来表示 ``privilege`` 字段，它出现在网易云音乐 PC 客户端 3.0.0 以上出现的新型元数据中。

    Attributes:
        flag: 作用未知。
    """
    flag: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))


@_attrs.define(kw_only=True)
class NCMMusicMetadataForPCv2(NCMMusicMetadataForPC):
    """用于存储从网易云音乐的歌曲标识符解析出的元数据。

    本类不提供解析标识符的功能，你需要使用模块层级的 ``loads()`` 函数。
    要想还原元数据为标识符，你需要使用模块层级的 ``dumps()`` 函数。

    本类适用于网易云音乐 PC 客户端 3.0.0 以上可能出现的元数据，其采用了和以往版本不同的结构。
    以下只列出其独有属性；要查看共有属性，请查阅 ``NCMMusicMetadataForPC`` 和 ``NCMMusicMetadata`` 的文档。

    **警告：对此类元数据的支持尚处于实验阶段。**

    Attributes:
        musicId (str):
          歌曲 ID，，必须是字符串形式。仅在网易云音乐平台有意义。
        artist (str):
          参与创作歌曲的所有歌手。
        fee (int):
          歌曲是否付费。只读属性 ``purchase_required`` 根据此属性返回更直观的结果。
        privilege (_MetadataPrivileges):
          作用未知；可直接访问子属性。
    """
    musicId: str = _attrs.field(default='', validator=_prettify_raised_TypeError(_attrs.validators.instance_of(str)))
    artist: str = _attrs.field(default='')
    fee: int = _attrs.field(default=0, validator=_prettify_raised_TypeError(_attrs.validators.instance_of(int)))
    privilege: _MetadataPrivileges = _attrs.field(
        factory=_MetadataPrivileges,
        converter=lambda _: _MetadataPrivileges(**_) if isinstance(_, _Mapping) else _,
        validator=_prettify_raised_TypeError(_attrs.validators.instance_of(_MetadataPrivileges))
    )

    @property
    def purchase_required(self) -> bool:
        return self.fee > 0

    def artist_prettify(self, *, sep: str = None) -> str:
        return self.artist

    def _dump_self_as_dict(self) -> dict[str, _Any]:
        metadata_dict = super()._dump_self_as_dict()
        metadata_dict['albumId'] = str(metadata_dict['albumId'])
        metadata_dict['mvId'] = str(metadata_dict['mvId'])
        return metadata_dict


Metadata: _TypeAlias = _TypeVar('Metadata', bound=NCMMusicMetadata)


def loads(identifier: _Union[str, bytes, bytearray], /,
          *, alter_id_key: _Union[bytes, bytearray] = None
          ) -> _Union[
    NCMMusicMetadata,
    NCMMusicMetadataForPCv1Free,
    NCMMusicMetadataForPCv1NCM,
    NCMMusicMetadataForPCv2,
    NCMMusicMetadataForAndroid
]:
    """载入并解析网易云音乐歌曲标识符 ``identifier``，返回一个基于 ``NCMMusicMetadata`` 的元数据对象。

    Args:
        identifier (str, bytes): 标识符，可接受 ``str``、``bytes`` 和 ``bytearray`` 对象。
        alter_id_key (bytes): 自定义元数据加密密钥。仅在加载自制的标识符时需要使用。
    """
    if isinstance(identifier, str):
        identifier = bytes(identifier, encoding='ASCII')
    try:
        memoryview(identifier)
    except TypeError:
        raise TypeError(
            f"a bytes-like object is required for argument 'identifier', not {type(identifier).__name__!r}"
        )
    else:
        identifier = bytes(identifier)

    if alter_id_key is None:
        id_key = bytes(_DEFAULT_ID_KEY)
    else:
        try:
            memoryview(alter_id_key)
        except TypeError:
            raise TypeError(
                f"a bytes-like object or None is required for argument 'alter_id_key', "
                f"not {type(alter_id_key).__name__!r}"
            )
        else:
            id_key = bytes(alter_id_key)

    if not identifier.startswith(b"163 key(Don't modify):"):
        raise MetadataParseError(f'{_shortrepr(identifier)}: Not a valid Identifier')
    identifier_stage1 = identifier.removeprefix(b"163 key(Don't modify):")
    identifier_stage2 = _base64.b64decode(identifier_stage1, validate=True)
    metadata_json_stage1 = _aes_mode_ecb_decrypt(id_key, identifier_stage2)
    if metadata_json_stage1.startswith(b'music:'):
        metadata_json_stage2 = metadata_json_stage1.removeprefix(b'music:')
    else:
        metadata_json_stage2 = metadata_json_stage1
    metadata_dict: dict[str, _Any] = _json.loads(metadata_json_stage2, object_hook=_load_metadata_json_object_hook)
    alter_albumPicDocId = int(metadata_dict['albumPicDocId'])
    alter_albumId = int(metadata_dict['albumId'])
    alter_mvId = int(metadata_dict['mvId'])

    metadata_field_names = tuple(metadata_dict)
    metadata_field_names_set = set(metadata_field_names)
    if metadata_field_names_set == _METADATA_ANDROID_FIELD_NAMES:
        cls = NCMMusicMetadataForAndroid
    else:
        metadata_dict['albumPicDocId'] = alter_albumPicDocId
        if metadata_field_names_set == _METADATA_PCv1_FREE_FIELD_NAMES:
            cls = NCMMusicMetadataForPCv1Free
        elif metadata_field_names_set == _METADATA_PCv1_NCM_FIELD_NAMES:
            cls = NCMMusicMetadataForPCv1NCM
        else:
            metadata_dict['albumId'] = alter_albumId
            metadata_dict['mvId'] = alter_mvId
            if metadata_field_names_set == _METADATA_PCv2_FIELD_NAMES:
                cls = NCMMusicMetadataForPCv2
            else:
                cls = NCMMusicMetadata
                if metadata_field_names != _METADATA_COMMON_FIELD_NAMES:
                    raise MetadataParseError(
                        f'{_shortrepr(metadata_json_stage2)}: '
                        f'missing Metadata field: '
                        f'{", ".join(repr(_) for _ in metadata_field_names)}'
                    )
                metadata_dict = {k: metadata_dict[k] for k in _METADATA_COMMON_FIELD_NAMES}
                metadata_field_names = tuple(metadata_dict)

    return cls(**metadata_dict, orig_metadata_field_names_ordered=metadata_field_names)


def dumps(
        metadata: Metadata, /,
        *, alter_id_key: _Union[bytes, bytearray] = None
) -> str:
    """将元数据对象 ``metadata`` 还原为标识符。

    本函数并不运行实际的还原操作，而是通过 ``metadata.dump()`` 完成并返回其结果。
    请注意，即使在不修改 ``metadata`` 的情况下，也会出现还原的标识符和原标识符不一致的情况，
    即 ``dump(load(identifier, alter_id_key=id_key), alter_id_key=id_key) == identifier``
    不一定为真值。

    返回的标识符总是 ``str`` 对象，如果需要写入二进制文件，你需要自行编码为字节对象。

    Args:
        metadata: 元数据对象，必须是 ``NCMMusicMetadata`` 或其子类（即 ``loads()`` 返回的结果）。
        alter_id_key (bytes): 自定义元数据加密密钥。仅在生成自制的标识符时需要使用。
    """
    if not isinstance(metadata, NCMMusicMetadata):
        raise TypeError(
            f"'dumps' can only accept a NCMMusicMetadata-based object, not {type(metadata).__name__!r}"
        )
    return metadata.dump(alter_id_key=alter_id_key)
