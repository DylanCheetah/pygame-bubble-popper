"""Scene

Base class for a scene.
"""

import pygame


# Classes
# =======
class Scene(object):
    """Base class for a scene.
    
    To create a scene class, extend this class. Then define a constructor which loads resources needed
    by the scene. If the scene changes any global game states, you may also need to define a destructor
    which restores the previous game states. The `on_event`, `update`, and `render` methods need to be
    overidden in derived classes.
    """
    _active = None

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle a pygame event.
        
        Parameters:
        event - the pygame event to handle
        """
        pass

    def update(self, dt: float) -> None:
        """Execute per-frame scene logic.
        
        Parameters:
        dt - the delta time in seconds
        """
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render the scene.
        
        Parameters:
        screen - the display surface
        """
        pass

    def make_active(self) -> None:
        """Make this scene active.
        
        Only one scene can be active at a time. Calling this will make the active scene inactive. If
        you need to have multiple active scenes for purposes such as rendering a pause menu over the
        game scene, then you need to create a sub-scene within the constructor of your main scene and
        manually call the `on_event`, `update`, and `render` methods of the sub-scene as needed.
        """
        Scene._active = self

    @staticmethod
    def get_active() -> "Scene":
        """Get the active scene.
        
        Returns:
        the active scene object
        """
        return Scene._active
