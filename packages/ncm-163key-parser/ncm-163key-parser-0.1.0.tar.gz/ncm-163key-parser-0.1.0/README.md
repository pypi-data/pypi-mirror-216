# 简介

`ncm-163key-parser` 项目意图以简单明了的方式操纵网易云音乐歌曲标识符（即“163 key”）。

# 使用须知

本项目是以学习和技术研究的初衷创建的，修改、再分发时请遵循[许可协议](LICENSE)。

**本项目虽然可以读取网易云音乐加密文件格式 `.ncm` 中的标识符，但是不可也无法移除中音频数据的加密保护！如果你是为此而来，请自行搜索并尝试其他项目！**

# 支持特性

-   [x] 解析标识符为元数据。
-   [x] （仅限 Python 调用）简明地编辑解析的元数据。
-   [x] （仅限 Python 调用）将元数据还原为标识符。
-   [x] 支持 PC 和 Android 平台的网易云音乐客户端下载的文件包含的标识符。
    -   是的，两个平台、不同版本的客户端下载的文件，包含的元数据不一致。
-   [ ] （等待实现）同时也是命令行工具，可用于直接读取和解析文件中的标识符。
    -   支持的文件类型包括：
        -   普通音频文件（.flac、.mp3）
        -   网易云音乐加密文件格式 `.ncm`。**（本项目不支持移除其音频的加密保护）**
-   [x] 纯 Python 实现，包括依赖包在内，没有任何 C 扩展模块，洁癖人士的不二之选。

# 安装

## 所需依赖

-   [`pyaes`](https://pypi.org/project/pyaes) - AES 加解密
-   [`attrs`](https://pypi.org/project/attrs) - 工厂化构建属性类，被本项目用来构建元数据容器

## 获取方式

### PyPI（推荐）

[查看 PyPI 页面](https://pypi.org/project/ncm-163key-parser/)

或者在命令行使用 `pip` 下载安装：

```sh-session
$ > python -m pip install ncm-163key-parser
```

### 从本仓库获取

[前往当前版本发布页](https://github.com/nukemiko/ncm-163key-parser/releases/latest)，此处提供了 Wheel 包下载。

安装下载的 Wheel 包：

```sh-session
python -m pip install /path/to/ncm_163key_parser-[version]-py3-none-any.whl
```

# 使用方法

## 命令行工具（待实现）

## Python 调用

以下是示例用法。如果想要玩出花样，请在使用时关注你使用的 IDE 对本模块函数、类和方法的提示信息，这样有助于你了解 API。

-   导入模块

```pycon
>>> import ncm163key
>>>
```

### 解析标识符

-   使用 `loads()` 加载一个标识符，该函数可接受 `str` 或字节对象形式的标识符：

    ```pycon
    >>> metadata1 = ncm163key.loads("163 key(Don't modify):...")
    >>> metadata1
    NCMMusicMetadataForAndroid(musicName='METHOD_HYMME_AMENOFLAME/.', musicId=471403213, artist={'stellatram': 12023150}, album='Kaleido Sphere ～天淵の双つ星～', albumId=35338410, albumPic='http://...', ...)
    >>> metadata2 = ncm163key.loads(b"163 key(Don't modify):...")
    >>> metadata2
    NCMMusicMetadataForPCv1NCM(musicName='忘れじの言の葉 (feat. 安次嶺希和子) [2022]', musicId=1972641406, artist={'未来古代楽団': 12131344, '安次嶺希和子': 30104787}, album='忘れじの言の葉／エデンの揺り籃', albumId=149778835, albumPic='https://...', ...)
    >>>
    ```

-   如果使用了自定义的标识符加密密钥，通过参数 `alter_id_key` 传递给函数：

    ```pycon
    >>> ncm163key.loads("163 key(Don't modify):...", alter_id_key=b'...')
    >>> ncm163key.loads(b"163 key(Don't modify):...", alter_id_key=b'...')
    >>>
    ```

### 查看解析出的元数据

以下列出了几种常用信息的获取方法。除非特殊说明，所有以“Id”结尾的属性都是 `int` 对象。

-   歌曲名称和 ID

    -   `musicName` - 歌曲名称（即标题）
    -   `musicId` - 歌曲 ID
        -   注意：如果你的下载文件来源是网易云音乐 PC 端 3.0.0 及以上版本，`musicId` 将会是一个 `str` 而不是 `int` 对象。

    ```pycon
    >>> metadata1.musicName
    'METHOD_HYMME_AMENOFLAME/.'
    >>> metadata1.musicId
    471403213
    >>>
    ```

-   歌手列表和歌手 ID：
    -   `artist` - 是一个定制的类字典对象，键（str）为歌手名称，值（int）为歌手 ID，会尝试自动转换被赋予的值
    -   `artist_prettify()` - 根据 `artist` 生成的美化后的歌手列表，默认使用顿号“、”分割每个歌手名称
    ```pycon
    >>> metadata1.artist
    {'stellatram': 12023150}
    >>> metadata1.artist_prettify()
    'stellatram'
    >>> metadata2.artist_prettify()
    '未来古代楽団、安次嶺希和子'
    >>> metadata2.artist_prettify(sep=' | ')
    '未来古代楽団 | 安次嶺希和子'
    >>>
    ```
-   专辑名称、ID 和专辑封面链接：

    -   `album` - 专辑名称
    -   `albumId` - 专辑 ID
    -   `albumPic` - 专辑封面下载链接

    ```pycon
    >>> metadata1.album
    'Kaleido Sphere ～天淵の双つ星～'
    >>> metadata1.albumId
    35338410
    >>> metadata1.albumPic
    'http://p2.music.126.net/cPwdlJxGCtX0e2L3SMQksg==/18915998044327357.jpg'
    >>>
    ```

-   `flac` - 歌曲的音频格式
    ```pycon
    >>> metadata1.format
    'flac'
    >>>
    ```
-   歌曲时长
    -   `duration` - 歌曲时长，单位为毫秒
    -   `duration_seconds`（只读） - 歌曲时长，由 `duration` 除以 1000 得到，与 `duration` 同步变化，单位为秒
    ```pycon
    >>> metadata.duration  # 单位为毫秒
    294026
    >>> metadata.duration_seconds  # metadata.duration_seconds 除以 1000，单位为秒
    294.026
    >>>
    ```

### 修改元数据

所有属性都是可修改的，但请注意，属性对类型甚至结构都有严格要求。以 `bitrate` 和 `metadata.artist` 为例：

-   `metadata.bitrate`：仅接受非负整数。

```pycon
>>> metadata.bitrate
984052
>>> metadata.bitrate = 1000000  # OK
>>> metadata.bitrate
1000000
>>> metadata.bitrate = '2000000'  # TypeError
Traceback (most recent call last):
...
TypeError: 'bitrate' must be <class 'int'> (got '2000000' that is a <class 'str'>).
>>> metadata.bitrate = -1000000  # ValueError
Traceback (most recent call last):
...
ValueError: 'bitrate' must be >= 0: -1000000
>>>
```

-   `metadata.artist`：仅接受可以转换为字典的对象；键必须是字符串，对应的值必须是整数，否则会引发 `TypeError`。

```pycon
>>> metadata1.artist
{'stellatram': 12023150}
>>> metadata1.artist['群星'] = 122455  # OK
>>> metadata1.artist
{'stellatram': 12023150, '群星': 122455}
>>> metadata1.artist = {
... 'stellatram': 12023150,
... '未来古代楽団': 12131344,
... '安次嶺希和子': 30104787
... }  # 尝试使用真正的字典对象为 artist 属性赋值，OK
>>> metadata.artist
{'stellatram': 12023150, '未来古代楽団': 12131344, '安次嶺希和子': 30104787}
>>> metadata.artist = 'stellatram'  # ValueError
Traceback (most recent call last):
...
ValueError: not enough values to unpack (expected 2, got 1)
>>> metadata.artist = 12023150  # TypeError
Traceback (most recent call last):
...
TypeError: 'artist' must be <class 'ncm163key._ArtistsMapping'> (got 12023150 that is a <class 'int'>).
>>> metadata.artist[12023150] = 12023150  # TypeError
Traceback (most recent call last):
...
TypeError: non-str object are not available for the mapping keys: 12023150 ('int')
>>> metadata1.artist['stellatram'] = '12023150'  # TypeError
Traceback (most recent call last):
...
TypeError: non-int object are not available for the mapping values: '12023150' ('str', key='stellatram')
>>>
```

### 将元数据还原为标识符

```pycon
>>> ncm163key.dumps(metadata)
"163 key(Don't modify):..."
>>>
```

-   如果要使用自定义的标识符加密密钥，通过参数 `alter_id_key` 传递给函数：

```pycon
>>> ncm163key.dumps(metadata, alter_id_key=b'...')
b"163 key(Don't modify):..."
>>>
```

# （可能的）常见问题

> 这个项目能输出 NCM 文件的音频内容吗？

不行，以后也不可能。下一个。

> 我没听说过 `pyaes` 这个包，为什么要用它做 AES 加解密，而不用 `pycryptodome`？

标识符的加解密使用了 AES，没有其他加密方式，因此使用 `pyaes` 这种简单的 AES 算法实现就足够了，`pycryptodome` 这种大而全的加密算法库显得有些臃肿。
