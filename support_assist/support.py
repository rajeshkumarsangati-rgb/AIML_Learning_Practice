"""Support assistant module starter."""

from __future__ import annotations


class SupportAssistant:
    """Simple support assistant stub."""

    def __init__(self, name: str = "Support Assistant") -> None:
        self.name = name

    def greet(self) -> str:
        return f"Hello! I am {self.name}."

    def handle_request(self, request: str) -> str:
        return f"Request received: {request}"


def main() -> None:
    assistant = SupportAssistant()
    print(assistant.greet())


if __name__ == "__main__":
    main()
