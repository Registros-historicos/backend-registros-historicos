from typing import Any, Iterable, Optional, Sequence
from django.db import connection


def call_fn_one(fn_name: str, args: Sequence[Any]) -> Any:
    sql = f"SELECT {fn_name}({', '.join(['%s'] * len(args))})"
    with connection.cursor() as cur:
        cur.execute(sql, args)
        row = cur.fetchone()
    return row[0] if row else None


def call_fn_rows(fn_name: str, args: Sequence[Any]) -> list[dict]:  # <-- Modifiqué a list[dict]
    sql = f"SELECT * FROM {fn_name}({', '.join(['%s'] * len(args))})"
    with connection.cursor() as cur:
        cur.execute(sql, args)
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]

    return [dict(zip(cols, r)) for r in rows]


def exec_fn_void(fn_name: str, args: Sequence[Any]) -> None:
    sql = f"SELECT {fn_name}({', '.join(['%s'] * len(args))})"
    with connection.cursor() as cur:
        cur.execute(sql, args)