from io import open
import os
import json
from enum import Enum
from typing import List

# typing
from typing_extensions import Self
from dataclasses import dataclass, field

# module
from .line import LongIdentificationLine, ShortIdentificationLine, Line

@dataclass
class Document:
    long_id_line: LongIdentificationLine = field(default_factory=LongIdentificationLine)
    short_id_line: ShortIdentificationLine = field(default_factory=ShortIdentificationLine)
    doc_lines: List[Line] = field(default_factory=list)
    linemap = {}
    doctype_codes = {}
    doctype_code = ""
    version_code = ""

    def get_doctype_version(self) -> str:
        """
        Produces the sinli version string, like "09"
        from the package of the instance class, such as sinli.libros.v9
        """
        pkg = self.__class__.__module__
        version_code = pkg.split('.')[-1]
        return version_code.replace('v', '').zfill(2)

    def __post_init__(self):
        from .doctype import DocumentType
        for doctype in DocumentType:
            name = doctype.name
            version_map = doctype.value[1]
            if not version_map: continue
            if version_map['??'] == self.__class__:
                self.doctype_code = name

        self.version_code = self.get_doctype_version()
        self.long_id_line.DOCTYPE = self.doctype_code
        self.long_id_line.VERSION = self.version_code
        self.short_id_line.DOCTYPE = self.doctype_code
        self.short_id_line.VERSION = self.version_code

    def consume_line(line: str, doc: Self) -> Self:
        print(f"\n[DEBUG] line: '{line}'")

        tdoc = line[0:1]
        if tdoc == "I" and not doc.long_id_line.FROM: # generic processing, we still don't know the doctype:  # Long id
            doc.long_id_line = LongIdentificationLine.from_str(line)
            return doc

        elif tdoc == "I" and not doc.short_id_line.FROM: # generic processing, we still don't know the doctype:  # Short id
            doc.short_id_line = ShortIdentificationLine.from_str(line)
            version_str = doc.short_id_line.VERSION if hasattr(doc, "short_id_line") else "" # ex: "09"
            doctype_str = doc.short_id_line.DOCTYPE if hasattr(doc, "short_id_line") else ""

            if doctype_str: # we just processed the short identification line
                from .doctype import DocumentType
                doctype_tup = DocumentType[doctype_str]
                doctype_class = doctype_tup.value[1].get(version_str)
                if doctype_class == None:
                    doctype_class = doctype_tup.value[1].get("??")
                    print(f"[WARN] using class {doctype_class} to parse document at version {version_str}. Some fields may be missing or become mixed")
                newdoc = doctype_class.from_document(doc)
                doc = newdoc
                print(f"[DEBUG] linemap: {doc.linemap.items()}")

            return doc

        lineclass = doc.linemap.get(tdoc)
        if lineclass == None:
            lineclass = doc.linemap.get("")
            print(f"[DEBUG] linemap: {doc.linemap.items()}")
            print(f"[DEBUG] lineclass: {lineclass}")
            if lineclass == None:
                print(f"[DEBUG] linemap: {doc.linemap.items()}")
                raise Exception(
                    "SINLI syntax error", f"El codi de registre {tdoc} no es reconeix i no s'ha definit cap classe sense prefix"
                )
        # we have a valid lineclass already
        doc.doc_lines.append(lineclass.from_str(line))
        return doc

    def consume_lines(lines, doc) -> Self:
        first = True
        for line in lines:
            if first:
                first = False
                continue
            doc = consume_line(line, doc)
        return doc

    @classmethod
    def from_str(cls, s: str) -> Self:
        doc = cls()
        doctype_s = ""
        cls.consume_lines(s.split_lines(), doc)
        return doc

    @classmethod
    def from_filename(cls, filename: str) -> Self:
        """
        El juego de caracteres recomendado es el 850 OEM – Multilingual Latín I // (DOS Latin 1 = CP 850)
        https://docs.python.org/3/library/codecs.html#module-codecs
        """
        doc = cls()
        with open(filename, encoding="cp850") as f:
            for line in f:
                line = line.strip()
                doc = cls.consume_line(line, doc)
        return doc

    @classmethod
    def from_document(cls, doc: Self) -> Self:
        new_doc = cls()
        new_doc.long_id_line = doc.long_id_line
        new_doc.short_id_line = doc.short_id_line
        new_doc.doc_lines = doc.doc_lines
        return new_doc

    def __str__(self) -> str:
        slines = []
        slines.append(str(self.long_id_line))
        slines.append(str(self.short_id_line))
        if len(self.doc_lines) > 0:
            slines.append(os.linesep.join([str(line) for line in self.doc_lines]))
        return os.linesep.join(slines)

    def to_readable(self) -> Self:
        new_doc = self.from_document(self)
        new_doc.long_id_line = self.long_id_line.to_readable()
        new_doc.short_id_line = self.short_id_line.to_readable()
        doc_lines = []
        for line in self.doc_lines:
            doc_lines.append(line.to_readable())
        new_doc.doc_lines = doc_lines

        return new_doc

    def to_json(self) -> str:
        return json.dumps([line.to_readable().to_dict() for line in self.doc_lines])

