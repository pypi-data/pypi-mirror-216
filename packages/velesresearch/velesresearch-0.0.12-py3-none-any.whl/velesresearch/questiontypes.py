"Wrappers for different question types."

from .tools import question


def radio(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for radio type."
    return question(
        label,
        question_text,
        *answers,
        question_type="radio",
        description=description,
        options=options
    )


def checkbox(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for checkbox type."
    return question(
        label,
        question_text,
        *answers,
        question_type="checkbox",
        description=description,
        options=options
    )
