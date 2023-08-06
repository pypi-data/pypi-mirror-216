"""Banners"""

from typing import Optional, Sequence

from attrs import define

from .characters import Character

__all__: Sequence[str] = ("Banner",)


@define
class Banner:
    """*Banner*

    # 🔌 Fields

    * `fallback` - Fallback of the banner
    * `name` - Name of the banner
    * `description` - Description of the banner

    # 🔎 Examples
    ```
    from gacha import Character, Banner

    Banner(
        "Wanderlust_Invocation",
        characters=[
            Character(0.003, name="Jean", description="https://genshin-impact.fandom.com/wiki/Jean"),
            Character(0.003, name="Qiqi", description="https://genshin-impact.fandom.com/wiki/Qiqi"),
            Character(0.003, name="Tighnari", description="https://genshin-impact.fandom.com/wiki/Tighnari"),
            Character(0.003, name="Keqing", description="https://genshin-impact.fandom.com/wiki/Keqing"),
            Character(0.003, name="Mona", description="https://genshin-impact.fandom.com/wiki/Mona"),
            Character(0.003, name="Dehya", description="https://genshin-impact.fandom.com/wiki/Dehya"),
            Character(0.003, name="Diluc", description="https://genshin-impact.fandom.com/wiki/Diluc"),
        ],
        name="Wanderlust_Invocation",
        description="https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation"
    )
    ```
    """

    fallback: str

    characters: Optional[Sequence[Character]] = None

    name: Optional[str] = None
    description: Optional[str] = None
