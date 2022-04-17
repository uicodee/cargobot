def make_connection_string(async_fallback: bool, user, password, database, host, port,) -> str:
    result = (
        f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    )
    if async_fallback:
        result += "?async_fallback=True"
    return result