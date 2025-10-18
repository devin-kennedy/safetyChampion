allBoards = [
    """pu pu or or or bl bl bl
pu pu pu or gr bl gr bl
pu pu pu or gr gr gr pu
pu pu pu pu pu pu pu pu
pu wh wh wh pu re re pu
pu wh ye wh ye re br br
pu pu ye ye ye re re br
pu pu pu pu pu pu br br""",
    """pu pu or or or bl bl bl
pu pu pu or gr bl gr bl
pu pu pu or gr gr gr pu
pu pu pu pu pu pu pu pu
pu pu pu pu pu re re pu
pu wh ye pu ye re br br
pu pu ye ye ye re re br
pu pu pu pu pu pu br br""",
    """pu pu pu pu pu pu or or
pu pu pu pu pu bl or or
pu pu pu gr pu bl wh or
pu pu re gr pu bl or or
ye pu pu gr pu bl or ye
ye ye pu gr pu bl ye ye
br ye ye ye ye ye ye br
br br br br br br br br""",
    """bk bk bk ye ye ye ye ye ye
bk wh wh wh wh bl bl bl ye
bk or wh pu pu pu bl bl ye
bk or pu pu pu pu pu gr ye
bk or pu pu br pu pu gr ye
bk or pu pu pu pu pu gr ye
re or or pu pu pu gr gr ye
re gr gr gr gr gr gr gr ye
re re ye ye ye ye ye ye ye"""
]

allColors = {
    "pu": "Purple",
    "or": "Orange",
    "bl": "Blue",
    "gr": "Green",
    "wh": "White",
    "ye": "Yellow",
    "re": "Red",
    "br": "Brown",
    "bk": "Black",
    "te": "Teal",
}

colorIcons = dict(zip(list(allColors.keys()), ["🟪", "🟧", "🟦", "🟩", "🔲", "🟨", "🟥", "🟫", "🔳", "⏹️"]))

validStates = ["E", "Q", "X"]
