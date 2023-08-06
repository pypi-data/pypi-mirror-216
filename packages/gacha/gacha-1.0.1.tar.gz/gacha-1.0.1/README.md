# gacha
🔮 Gacha

![language](https://img.shields.io/badge/language-Python-009933)
![license](https://img.shields.io/badge/license-MIT-cafffe)

# 📑 Table of Contents
- [✨ Installation](#✨-installation)
    - [🐍 PyPi](#🐍-pypi)
- [🔎 Examples](#examples)
    - [🧾 Basic](#🧾-basic)
- [✨ Links](#✨-links)

# 📦 Installation
## 🐍 PyPi
```
pip install gacha
```

# 🔎 Examples
## 🧾 Basic
`examples/basic.py`
<details>

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
                    ...,
                ],
                name="Wanderlust_Invocation",
                description="https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation",
            ),
        ]
    )

    character = engine.roll()

    print(character.name)  # Jean
    print(character.description)  # https://genshin-impact.fandom.com/wiki/Jean

</details>

# ✨ Links
🐍 [*PyPi*](https://pypi.org/project/gacha/)\
🏠 [*Homepage*](https://github.com/elaresai/gacha)\
🐱 [*Repository*](https://github.com/elaresai/gacha)