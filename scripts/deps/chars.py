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

def commonTopBorder(renderMode, size=80):
  output = ""
  output += "{btl}".format(btl=specialChars[renderMode]["borderTopLeft"])
  for i in range(size):
    output += "{bh}".format(bh=specialChars[renderMode]["borderHorizontal"])
  output += "{btr}".format(btr=specialChars[renderMode]["borderTopRight"])
  return output

def commonBottomBorder(renderMode, size=80):
  output = ""
  output += "{bbl}".format(bbl=specialChars[renderMode]["borderBottomLeft"])
  for i in range(size):
    output += "{bh}".format(bh=specialChars[renderMode]["borderHorizontal"])
  output += "{bbr}".format(bbr=specialChars[renderMode]["borderBottomRight"])
  return output

def padText(text, size=45):
  output = ""
  output += text
  for i in range(size - len(text)):
    output += " "
  return output

def commonEmptyLine(renderMode, size=80):
  output = ""
  output += "{bv}".format(bv=specialChars[renderMode]["borderVertical"])
  for i in range(size):
    output += " "
  output += "{bv}".format(bv=specialChars[renderMode]["borderVertical"])
  return output
