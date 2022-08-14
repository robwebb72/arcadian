def load() -> float:
    hiscore: float = 0
    try:
        with open("hiscore.dat") as file:
            contents = file.read()
            hiscore = float(contents)
    except (FileNotFoundError, ValueError):
        pass
    return hiscore


def save(score: float) -> None:
    with open("hiscore.dat", "w") as file:
        file.write(f"{score}")
