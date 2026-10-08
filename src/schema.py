"""Loads a document-type definition from YAML.

Everything the pipeline knows about a document type comes from the file loaded here.
Run `python -m src.schema config/<file>.yaml` to print what was loaded.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

FieldType = Literal["string", "date", "number", "email", "phone", "enum"]


class FieldSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    type: FieldType
    required: bool = False
    description: str
    keywords: list[str] = []
    validate_regex: Optional[str] = None
    enum_values: Optional[list[str]] = None

    @field_validator("validate_regex")
    @classmethod
    def _regex_compiles(cls, value):
        if value is not None:
            re.compile(value)
        return value

    @model_validator(mode="after")
    def _enum_has_values(self):
        if self.type == "enum" and not self.enum_values:
            raise ValueError(f"field '{self.name}' is an enum but lists no enum_values")
        return self


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_name: str
    doc_type: str
    doc_id_prefix: str
    input_glob: str
    review_threshold: float = 0.7
    max_chars: int = 12000
    system_prompt: str
    fields: list[FieldSpec]

    @model_validator(mode="after")
    def _unique_names(self):
        names = [spec.name for spec in self.fields]
        if len(names) != len(set(names)):
            raise ValueError("field names must be unique")
        if not names:
            raise ValueError("a schema needs at least one field")
        return self

    @property
    def field_names(self) -> list[str]:
        return [spec.name for spec in self.fields]

    @property
    def label_suffix(self) -> str:
        return self.schema_name.removeprefix("schema_")


def load_schema(path: str | Path) -> Schema:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Schema(**data)


if __name__ == "__main__":
    loaded = load_schema(sys.argv[1])
    print(f"{loaded.schema_name}: {len(loaded.fields)} fields, threshold {loaded.review_threshold}")
    for spec in loaded.fields:
        flag = "required" if spec.required else "optional"
        print(f"  - {spec.name} ({spec.type}, {flag})")
