
from typing import Optional

from libgravatar import Gravatar


def get_gravatar(email: str) -> Optional[str]:
    grav = Gravatar(email)
    return grav.get_image(size=200, use_ssl=True, default='', force_default=False, filetype_extension=False,  rating='', )