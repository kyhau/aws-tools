from PyInquirer import Token, prompt, style_from_dict

custom_style = style_from_dict(
    {
        Token.Separator: "#6C6C6C",
        Token.QuestionMark: "#FF9D00 bold",
        Token.Selected: "#5F819D",
        Token.Pointer: "#FF9D00 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#5F819D bold",
        Token.Question: "",
    }
)


def prompt_single_selection(name, options):
    if not options:
        raise ValueError("No profiles retrieved for selection.")

    questions = [
        {
            "choices": options,
            "message": f"Please choose the {name}",
            "name": name,
            "type": "list",
        }
    ]
    return prompt(questions, style=custom_style)


def prompt_multi_selection(name, options, pre_selected_options):
    if not options:
        raise ValueError("No options retrieved for selection.")

    questions = [
        {
            "choices": [
                    {
                        "name": option,
                        "checked": True
                        if option in pre_selected_options
                        else False,
                    }
                for option in options
            ],
            "message": f"Please choose the {name}",
            "name": f"{name}s",
            "type": "checkbox",
        }
    ]
    return prompt(questions, style=custom_style)


def test_1():
    options = ["A", "B", "C", "D"]
    name = "grade"
    resp = prompt_single_selection(name, options)
    print(resp)  # {'grade': 'A'}


def test_2():
    options = ["A", "B", "C", "D"]
    pre_selected_options = ['B']
    name = "grade"
    resp = prompt_multi_selection(name, options, pre_selected_options)
    print(resp)  # {'grades': ['B']}


# if __name__ == "__main__":
#     test_1()
