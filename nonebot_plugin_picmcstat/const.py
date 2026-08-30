import re
from typing import Literal, TypeAlias

from mcstatus.motd.components import (
    AnyFormatting,
    AnyMinecraftColor,
    BedrockFormatting,
    BedrockMinecraftColor,
    JavaFormatting,
    JavaMinecraftColor,
)

ServerTypeRaw: TypeAlias = Literal["je", "be"]
ServerType: TypeAlias = Literal[ServerTypeRaw, "auto"]

CODE_COLOR = {
    "0": "#000000",
    "1": "#0000AA",
    "2": "#00AA00",
    "3": "#00AAAA",
    "4": "#AA0000",
    "5": "#AA00AA",
    "6": "#FFAA00",
    "7": "#AAAAAA",
    "8": "#555555",
    "9": "#5555FF",
    "a": "#55FF55",
    "b": "#55FFFF",
    "c": "#FF5555",
    "d": "#FF55FF",
    "e": "#FFFF55",
    "f": "#FFFFFF",
    "g": "#DDD605",
}
STROKE_COLOR = {
    "0": "#000000",
    "1": "#00002A",
    "2": "#002A00",
    "3": "#002A2A",
    "4": "#2A0000",
    "5": "#2A002A",
    "6": "#2A2A00",
    "7": "#2A2A2A",
    "8": "#151515",
    "9": "#15153F",
    "a": "#153F15",
    "b": "#153F3F",
    "c": "#3F1515",
    "d": "#3F153F",
    "e": "#3F3F15",
    "f": "#3F3F3F",
    "g": "#373501",
}
# Bedrock-only material colors (from Minecraft Bedrock), values match the
# official Bedrock palette. Java edition has no such codes.
BEDROCK_MATERIAL_CODE_COLOR = {
    "h": "#E3D4D1",  # quartz
    "i": "#CECACA",  # iron
    "j": "#443A3B",  # netherite
    "m": "#971607",  # redstone
    "n": "#B4684D",  # copper
    "p": "#DEB12D",  # gold
    "q": "#119F36",  # emerald
    "s": "#2CBAA8",  # diamond
    "t": "#21497B",  # lapis
    "u": "#9A5CC6",  # amethyst
    "v": "#EB7214",  # resin
}
BEDROCK_MATERIAL_STROKE_COLOR = {
    "h": "#383534",
    "i": "#333232",
    "j": "#110E0E",
    "m": "#250501",
    "n": "#2D1A13",
    "p": "#372C0B",
    "q": "#04280D",
    "s": "#0B2E2A",
    "t": "#08121E",
    "u": "#261731",
    "v": "#3B1D05",
}
CODE_COLOR_BEDROCK = {
    **CODE_COLOR,
    "g": "#FFAA00",
    **BEDROCK_MATERIAL_CODE_COLOR,
}
STROKE_COLOR_BEDROCK = {
    **STROKE_COLOR,
    "g": "#2A2A00",
    **BEDROCK_MATERIAL_STROKE_COLOR,
}
STYLE_BBCODE = {
    "l": ["[b]", "[/b]"],
    "m": ["[del]", "[/del]"],
    "n": ["[u]", "[/u]"],
    "o": ["[i]", "[/i]"],
    "k": ["[obfuscated]", "[/obfuscated]"],  # placeholder
}
OBFUSCATED_PLACEHOLDER_REGEX = re.compile(
    r"\[obfuscated\](?P<inner>.*?)\[/obfuscated\]",
)


def _build_enum_color_map(
    enum_cls: type[AnyMinecraftColor],
    mapping: dict[str, str],
) -> dict[AnyMinecraftColor, str]:
    """Map mcstatus color enum members to the plugin's hex colors.

    Only members whose code exists in the mapping are included (e.g. Java
    edition has no ``g`` Minecoin gold in mcstatus v14).
    """
    return {m: mapping[m.value] for m in enum_cls if m.value in mapping}


# Java edition colors / styles
ENUM_CODE_COLOR: dict[AnyMinecraftColor, str] = _build_enum_color_map(
    JavaMinecraftColor, CODE_COLOR
)
ENUM_STROKE_COLOR: dict[AnyMinecraftColor, str] = _build_enum_color_map(
    JavaMinecraftColor, STROKE_COLOR
)

# Bedrock edition colors / styles (minecraft code ``g`` and material colors)
# material color codes added in Bedrock; Java edition does not have them
ENUM_CODE_COLOR_BEDROCK: dict[AnyMinecraftColor, str] = _build_enum_color_map(
    BedrockMinecraftColor, CODE_COLOR_BEDROCK
)
ENUM_STROKE_COLOR_BEDROCK: dict[AnyMinecraftColor, str] = _build_enum_color_map(
    BedrockMinecraftColor, STROKE_COLOR_BEDROCK
)

# Java / Bedrock formatting members; bedrock has no under/::strikethrough,
# so those lookups are simply absent for bedrock
ENUM_STYLE_BBCODE: dict[AnyFormatting, list[str]] = {}
for fmt_cls in (JavaFormatting, BedrockFormatting):
    for k, v in STYLE_BBCODE.items():
        try:
            ENUM_STYLE_BBCODE[fmt_cls(k)] = v
        except ValueError:
            pass

GAME_MODE_MAP = {"Survival": "生存", "Creative": "创造", "Adventure": "冒险"}
FORMAT_CODE_REGEX = r"§[0-9abcdefgklmnor]"