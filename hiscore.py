def load():
    hiscore = 0
    try:
        with open("hiscore.dat") as file:
            contents = file.read()
            hiscore = float(contents)
    except (BaseException):
        pass
    return hiscore


def save(hiscore):
    with open("hiscore.dat", "w") as file:
        file.write(f"{hiscore}")
