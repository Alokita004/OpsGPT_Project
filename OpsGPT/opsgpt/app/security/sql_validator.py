from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator
import re


class SQLRequest(BaseModel):
    sql: str = Field(..., min_length=1)

    @model_validator(mode="before")
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class SQLValidationError(Exception):
    pass


PROHIBITED = [
    r"\binsert\b",
    r"\bupdate\b",
    r"\bdelete\b",
    r"\bdrop\b",
    r"\balter\b",
    r"\btruncate\b",
    r"\bcreate\b",
    r"\bmerge\b",
    r"\bcall\b",
]


def validate_sql(sql: str, allow_tables: List[str] | None = None) -> bool:
    # Basic checks: no semicolons (prevent multi-statement) and only allow SELECT / WITH
    lowered = sql.lower()
    if ";" in sql:
        raise SQLValidationError("Multiple statements or semicolons are not allowed")

    # Only allow SELECT or WITH starting
    if not re.match(r"^(\s*)(with|select)\b", lowered):
        raise SQLValidationError("Only SELECT and WITH queries are allowed")

    # Prohibit dangerous keywords
    for pat in PROHIBITED:
        if re.search(pat, lowered):
            raise SQLValidationError(f"Prohibited SQL keyword detected: {pat}")

    # Allowlist tables: ensure all referenced tables are in allow_tables if provided
    if allow_tables:
        # crude: find occurrences of table names after from or join
        found = re.findall(r"(?:from|join)\s+([`\"]?\w+[`\"]?)", lowered)
        found = [f.strip('`"') for f in found]
        for f in found:
            if f not in allow_tables and f != 'dual':
                raise SQLValidationError(f"Access to table '{f}' is not allowed")

    return True
