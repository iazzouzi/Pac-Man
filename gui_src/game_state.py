from typing import Any


class GameState:
    """Base class representing a state of the game."""

    def handle_events(self, events: Any) -> Any:
        """Handle user events for the game state.

        Args:
            events (Any): A collection of events,
                (e.g., from pygame.event.get()).

        Returns:
            Any: The result of the event handling, indicating the next state.
        """
        pass

    def update(self) -> Any:
        """Update the logic of the game state.

        Returns:
            Any: The result of the state update, indicating the next state.
        """
        pass

    def render(self, screen: Any) -> None:
        """Render the game state to the screen.

        Args:
            screen (Any): The display surface to render the state onto.
        """
        pass
