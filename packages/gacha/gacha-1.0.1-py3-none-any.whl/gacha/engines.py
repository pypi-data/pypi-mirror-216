"""Engines"""

from random import choices
from typing import Optional, Sequence

from attrs import define

from .banners import Banner
from .characters import Character

__all__: Sequence[str] = ("Engine",)


MULTIPLIER = 100


@define
class Engine:
    """*Engine*

    # 🔌 Fields
    * `banners` - Banners of the engine

    # 🔎 Examples
    ```
    from gacha import Engine, Banner, Character

    Engine(
        [
            Banner(
                "Wanderlust_Invocation",
                characters=[
                    Character(
                        0.003,
                        name="Jean",
                        description="https://genshin-impact.fandom.com/wiki/Jean",
                    ),
                    Character(
                        0.003,
                        name="Qiqi",
                        description="https://genshin-impact.fandom.com/wiki/Qiqi",
                    ),
                    Character(
                        0.003,
                        name="Tighnari",
                        description="https://genshin-impact.fandom.com/wiki/Tighnari",
                    ),
                    Character(
                        0.003,
                        name="Keqing",
                        description="https://genshin-impact.fandom.com/wiki/Keqing",
                    ),
                    Character(
                        0.003,
                        name="Mona",
                        description="https://genshin-impact.fandom.com/wiki/Mona",
                    ),
                    Character(
                        0.003,
                        name="Dehya",
                        description="https://genshin-impact.fandom.com/wiki/Dehya",
                    ),
                    Character(
                        0.003,
                        name="Diluc",
                        description="https://genshin-impact.fandom.com/wiki/Diluc",
                    ),
                    ...,
                ],
                name="Wanderlust_Invocation",
                description="https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation",
            ),
        ]
    )
    ...
    ```
    """

    banners: Optional[Sequence[Banner]] = None

    def roll(self, fallback: str, count: int = 1) -> list[Character]:
        """*roll*

        # Arguments

        * `fallback` - Fallback of the banner
        * `count` - Count of the rolls

        # 🔎 Examples
        ```
        from gacha import Engine, Banner, Character

        engine = Engine(
            [
                Banner(
                    "Wanderlust_Invocation",
                    characters=[
                        Character(
                            0.003,
                            name="Jean",
                            description="https://genshin-impact.fandom.com/wiki/Jean",
                        ),
                        Character(
                            0.003,
                            name="Qiqi",
                            description="https://genshin-impact.fandom.com/wiki/Qiqi",
                        ),
                        Character(
                            0.003,
                            name="Tighnari",
                            description="https://genshin-impact.fandom.com/wiki/Tighnari",
                        ),
                        Character(
                            0.003,
                            name="Keqing",
                            description="https://genshin-impact.fandom.com/wiki/Keqing",
                        ),
                        Character(
                            0.003,
                            name="Mona",
                            description="https://genshin-impact.fandom.com/wiki/Mona",
                        ),
                        Character(
                            0.003,
                            name="Dehya",
                            description="https://genshin-impact.fandom.com/wiki/Dehya",
                        ),
                        Character(
                            0.003,
                            name="Diluc",
                            description="https://genshin-impact.fandom.com/wiki/Diluc",
                        ),
                    ],
                    name="Wanderlust_Invocation",
                    description="https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation",
                ),
            ]
        )

        character = engine.roll()

        print(character.name)  # Jean
        print(character.description)  # https://genshin-impact.fandom.com/wiki/Jean
        ```
        """
        k = count

        for banner in self.banners:
            if banner.fallback != fallback:
                continue

            population = []
            weights = []

            for character in banner.characters:
                weight = character.weight * MULTIPLIER

                population.append(character)
                weights.append(weight)

            return choices(population, weights=weights, k=k)

        raise ValueError(fallback)