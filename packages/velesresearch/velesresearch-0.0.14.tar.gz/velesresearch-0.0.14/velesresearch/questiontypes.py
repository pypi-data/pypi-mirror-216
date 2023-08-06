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


def text(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for text type."
    return question(
        label,
        question_text,
        *answers,
        question_type="text",
        description=description,
        options=options
    )


def text_long(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for text_long type."
    return question(
        label,
        question_text,
        *answers,
        question_type="text_long",
        description=description,
        options=options
    )


def dropdown(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for dropdown type."
    return question(
        label,
        question_text,
        *answers,
        question_type="dropdown",
        description=description,
        options=options
    )


def dropdown_multi(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for dropdown_multi type."
    return question(
        label,
        question_text,
        *answers,
        question_type="dropdown_multi",
        description=description,
        options=options
    )


def yes_no(label, question_text, description=None, options=None):
    "Wrapper around question function for yes_no type."
    return question(
        label,
        question_text,
        question_type="yes_no",
        description=description,
        options=options,
    )


def ranking(label, question_text, *answers, description=None, options=None):
    "Wrapper around question function for ranking type."
    return question(
        label,
        question_text,
        *answers,
        question_type="ranking",
        description=description,
        options=options
    )
