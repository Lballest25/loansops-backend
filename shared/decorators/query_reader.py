import os
from functools import wraps


from typing import Callable, Any


def sql_query_reader(
    base_dir: str, relative_path: str
) -> Callable[[Any], Callable]:

    sql_folder = os.path.join(base_dir, "sql")
    query_file = os.path.join(sql_folder, relative_path)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                with open(query_file, "r") as file:
                    setattr(
                        wrapper,
                        "query",
                        file.read(),  # type: ignore[attr-defined]
                    )
            except FileNotFoundError:
                raise FileNotFoundError(f"The file {query_file} was not found")
            return func(*args, **kwargs)

        return wrapper

    return decorator
