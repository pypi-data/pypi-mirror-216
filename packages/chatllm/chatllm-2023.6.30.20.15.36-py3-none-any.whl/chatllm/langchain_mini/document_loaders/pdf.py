#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : pdf
# @Time         : 2023/6/30 18:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from langchain.document_loaders.parsers.pdf import BaseBlobParser, Blob, Document
from langchain.document_loaders.pdf import PyMuPDFLoader as _PyMuPDFLoader


class PyMuPDFLoader(_PyMuPDFLoader):
    """Loader that uses PyMuPDF to load PDF files."""

    def load(self, **kwargs: Optional[Any]) -> List[Document]:
        """Load file."""

        parser = PyMuPDFParser(text_kwargs=kwargs)
        blob = Blob.from_path(self.file_path)
        return parser.parse(blob)


class PyMuPDFParser(BaseBlobParser):
    """Parse PDFs with PyMuPDF."""

    def __init__(self, text_kwargs: Optional[Mapping[str, Any]] = None) -> None:
        """Initialize the parser.

        Args:
            text_kwargs: Keyword arguments to pass to ``fitz.Page.get_text()``.
        """
        self.text_kwargs = text_kwargs or {}

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob."""
        import fitz
        with blob.as_bytes_io() as file_path:
            doc = fitz.open(file_path)  # open document

            for page in doc:
                page_content = page.get_text(**self.text_kwargs).strip()  #

                yield Document(
                    page_content=page_content,
                    metadata=dict(
                        {
                            "source": blob.source,
                            "file_path": blob.source,
                            "page": page.number,
                            "page_length": len(page_content),  #
                            "total_pages": len(doc),
                        },
                        **{
                            k: doc.metadata[k]
                            for k in doc.metadata
                            if type(doc.metadata[k]) in [str, int]
                        },
                    ),
                )
