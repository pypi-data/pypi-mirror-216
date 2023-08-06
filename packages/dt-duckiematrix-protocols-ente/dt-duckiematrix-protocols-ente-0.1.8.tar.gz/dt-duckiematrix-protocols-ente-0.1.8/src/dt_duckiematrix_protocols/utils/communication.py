from typing import Tuple


def parse_topic(topic: str) -> Tuple[str, str]:
    protocol, key = topic.split(":/", maxsplit=1)
    return protocol, key


def compile_topic(protocol: str, key: str) -> str:
    return f"{protocol}:/{key}"
