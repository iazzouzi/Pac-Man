from typing import Any


class GameState:
    def handle_events(self, events: Any) -> Any:
        pass

    def update(self) -> Any:
        pass

    def render(self, screen: Any) -> None:
        pass
