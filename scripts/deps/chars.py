specialChars = {
  "latin": {
    "rightArrowFull": "►",
    "upArrowFull": "▲",
    "upArrowLine": "↑",
    "downArrowFull": "▼",
    "downArrowLine": "↓",
    "borderVertical": "║",
    "borderHorizontal": "═",
    "borderTopLeft": "╔",
    "borderTopRight": "╗",
    "borderBottomLeft": "╚",
    "borderBottomRight": "╝"
  },
  "simple": {
    "rightArrowFull": "→",
    "upArrowFull": "↑",
    "upArrowLine": "↑",
    "downArrowFull": "↓",
    "downArrowLine": "↓",
    "borderVertical": "│",
    "borderHorizontal": "─",
    "borderTopLeft": "┌",
    "borderTopRight": "┐",
    "borderBottomLeft": "└",
    "borderBottomRight": "┘"
  },
  "ascii": {
    "rightArrowFull": ">",
    "upArrowFull": "^",
    "upArrowLine": "^",
    "downArrowFull": "v",
    "downArrowLine": "v",
    "borderVertical": "|",
    "borderHorizontal": "-",
    "borderTopLeft": "/",
    "borderTopRight": "\\",
    "borderBottomLeft": "\\",
    "borderBottomRight": "/"
  }
}

def commonTopBorder(renderMode):
  return ("{btl}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{btr}").format(
    btl=specialChars[renderMode]["borderTopLeft"],
    btr=specialChars[renderMode]["borderTopRight"],
    bh=specialChars[renderMode]["borderHorizontal"]
  )

def commonBottomBorder(renderMode):
  return ("{bbl}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
      "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bbr}").format(
    bbl=specialChars[renderMode]["borderBottomLeft"],
    bbr=specialChars[renderMode]["borderBottomRight"],
    bh=specialChars[renderMode]["borderHorizontal"]
  )

def commonEmptyLine(renderMode):
  return "{bv}                                                                                {bv}".format(bv=specialChars[renderMode]["borderVertical"])

