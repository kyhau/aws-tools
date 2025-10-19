from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# See also https://inquirerpy.readthedocs.io/en/latest/pages/style.html
# ?highlight=style#customising-style


def prompt_single_selection(name, options, message=None):
    if not options:
        raise ValueError("No options retrieved for selection.")

    return inquirer.select(
        message=message if message else f"Please choose the {name}",
        choices=options,
        default=None,
    ).execute()


def prompt_multi_selection(name, options, pre_selected_options, message=None):
    if not options:
        raise ValueError("No options retrieved for selection.")

    choices = [Choice(option, enabled=option in pre_selected_options) for option in options]

    return inquirer.checkbox(
        message=message if message else f"Please choose the {name}",
        choices=choices,
        cycle=True,
        transformer=lambda result: f"{len(result)} {name} selected",
    ).execute()


def test_1():
    options = ["A", "B", "C", "D"]
    name = "grade"
    resp = prompt_single_selection(name, options)
    print(resp)  # 'A'


def test_2():
    options = ["A", "B", "C", "D"]
    pre_selected_options = ["B"]
    name = "grade"
    resp = prompt_multi_selection(name, options, pre_selected_options)
    print(resp)  # ['B', 'C']


# if __name__ == "__main__":
#     test_1()
#     test_2()
