from __future__ import annotations

from urllib.parse import urlencode, urlparse

from pydantic import PostgresDsn


def normalize_postgres_dsn_for_atoti_sql(url: PostgresDsn, /) -> object:
    parts = urlparse(url)

    query_parts: list[str] = []

    if parts.query:
        query_parts.append(parts.query)

    if parts.username or parts.password:
        query_parts.append(
            urlencode({"user": parts.username, "password": parts.password})
        )

    return PostgresDsn(
        # This is how Pydantic creates an instance from parts.
        None,
        scheme="postgresql",
        host=str(parts.hostname),
        port=str(parts.port) if parts.port else None,
        path=parts.path,
        query="&".join(query_parts) if query_parts else None,
        fragment=parts.fragment,
    )
