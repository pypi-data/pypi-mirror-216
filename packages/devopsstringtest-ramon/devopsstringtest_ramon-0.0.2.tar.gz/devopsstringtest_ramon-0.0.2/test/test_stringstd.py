from stringstandardization import stringstd


def test_full_name():
    name = "Kelly Frazão"
    std_name = stringstd.standardize(name)
    assert len(std_name.split(' ')) > 1
