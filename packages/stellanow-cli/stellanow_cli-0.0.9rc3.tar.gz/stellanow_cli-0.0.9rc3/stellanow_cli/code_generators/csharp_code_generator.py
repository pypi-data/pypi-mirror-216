"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import difflib
import json
import logging
import re

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterator

from ..api import StellaEventDetailed, StellaField, StellaEntity
from .code_generator import CodeGenerator
from ..exceptions.cli_exceptions import (
    StellaNowCLINamespaceNotFoundException,
    StellaNowCLINoEntityAssociatedWithEventException
)
from ..utils.utils import snake_to_camel, snake_to_lower_camel, remove_comments


logger = logging.getLogger(__name__)


def field_type_mapping(value_type: str) -> str:
    mapping = {
        'Decimal': 'decimal',
        'Integer': 'int',
        'Boolean': 'bool',
        'String': 'string',
        'Date': 'DateOnly',
        'DateTime': 'DateTime'
    }
    return mapping.get(value_type, 'object')  # default to object if unknown


def field_format_mapping(value_type: str) -> str:
    mapping = {
        'Decimal': '.ToString("F2", CultureInfo.InvariantCulture)',
        'Integer': '.ToString()',
        'Boolean': '.ToString().ToLower()',
        'String': '',
        'Date': '.ToString("yyyy-MM-dd")',
        'DateTime': '.ToString("yyyy-MM-ddTHH:mm:ssZ")'
    }
    return mapping.get(value_type, '')


def escape_reserved_words(word: str) -> str:
    reserved_words = [
        "abstract", "as", "base", "bool", "break", "byte", "case", "catch", "char", "checked",
        "class", "const", "continue", "decimal", "default", "delegate", "do", "double", "else",
        "enum", "event", "explicit", "extern", "false", "finally", "fixed", "float", "for",
        "foreach", "goto", "if", "implicit", "in", "int", "interface", "internal", "is", "lock",
        "long", "namespace", "new", "null", "object", "operator", "out", "override", "params",
        "private", "protected", "public", "readonly", "ref", "return", "sbyte", "sealed",
        "short", "sizeof", "stackalloc", "static", "string", "struct", "switch", "this", "throw",
        "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort", "using", "virtual",
        "void", "volatile", "while"
    ]

    return f"{word}_" if word in reserved_words else word


@dataclass
class CSharpField:
    original_name: str
    csharp_name: str
    type: str
    format: str

    @classmethod
    def from_stella_field(cls, field: StellaField):
        return cls(
            original_name=field.name,
            csharp_name=escape_reserved_words(snake_to_lower_camel(field.name)),
            type=field_type_mapping(field.valueType),
            format=field_format_mapping(field.valueType)
        )

    def to_constructor_parameter_declaration(self):
        return f'{self.type} {self.csharp_name}'


@dataclass
class CSharpEntity:
    original_name: str
    csharp_name: str

    @classmethod
    def from_stella_field(cls, entity: StellaEntity):
        return cls(
            original_name=entity.name,
            csharp_name=escape_reserved_words(snake_to_lower_camel(entity.name)) + "Id",
        )

    def to_entity_type_declaration(self):
        return f'new EntityType("{self.original_name}", {self.csharp_name})'

    def to_constructor_parameter_declaration(self):
        return f'string {self.csharp_name}'


class CsharpCodeGenerator(CodeGenerator):
    @staticmethod
    def generate_class(event: StellaEventDetailed, **kwargs) -> str:
        template = CsharpCodeGenerator.load_template('csharp')

        namespace = kwargs.get('namespace', 'StellaNowSDK.Messages')

        fields = [CSharpField.from_stella_field(field) for field in event.fields]
        entities = [CSharpEntity.from_stella_field(entity) for entity in event.entities]
        if not entities:
            raise StellaNowCLINoEntityAssociatedWithEventException()

        rendered = template.render(
            className=snake_to_camel(event.name),
            eventName=event.name,
            constructorArguments=', '.join([
                ', '.join([entity.to_constructor_parameter_declaration() for entity in entities]),
                ', '.join([field.to_constructor_parameter_declaration() for field in fields])
            ]),
            entitiesList=', '.join([entity.to_entity_type_declaration() for entity in entities]),
            fields=fields,
            namespace=namespace,
            eventJson=json.dumps(asdict(event), indent=4),
            eventId=event.id,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        )

        return rendered

    @staticmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        return f"{snake_to_camel(event_name)}Message.cs"

    @classmethod
    def get_diff(cls, event: StellaEventDetailed, existing_code: str) -> Iterator[str]:
        # Extract namespace from the existing code
        namespace_search = re.search(r'namespace (.*);', existing_code)
        if namespace_search is None:
            raise StellaNowCLINamespaceNotFoundException()

        namespace = namespace_search.group(1)

        new_code = cls.generate_class(event, **{'namespace': namespace})

        existing_code_no_comments = remove_comments(existing_code)
        new_code_no_comments = remove_comments(new_code)

        # Use difflib to compare the new and existing code
        diff = difflib.unified_diff(existing_code_no_comments.splitlines(keepends=True),
                                    new_code_no_comments.splitlines(keepends=True))

        return (line for line in diff if line.startswith('- ') or line.startswith('+ ') and not (
                    line.startswith('---') or line.startswith('+++')))
