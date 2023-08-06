from .downloader_middleware import DefineDownloaderMiddleware
from .spider_middleware import DefineSpiderMiddleware
from .settings import append_doc as _append_doc

__all__ = [DefineDownloaderMiddleware, DefineSpiderMiddleware]

__doc__ = _append_doc(__all__)
del _append_doc
