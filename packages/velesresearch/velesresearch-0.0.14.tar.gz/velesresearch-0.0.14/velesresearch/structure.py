"Structural elements of the survey"
from __future__ import annotations
import warnings
import os
from pathlib import Path
from collections.abc import Sequence
import csv
import tarfile
from json import JSONEncoder
from pydantic import BaseModel, validator
from pynpm import YarnPackage
from .options import QuestionOptions, PageOptions, SurveyOptions
from .generator import generate_survey


def check_labels_for_spaces(cls, label):
    "Checks if label contains spaces"
    if " " in label:
        raise ValueError("Label should not contain spaces")
    return label


class Question(BaseModel):
    "General question class"
    label: str
    question_text: str
    answers: str | Sequence[str]
    question_type: str = "radio"
    options: QuestionOptions | None = None
    description: str | None = None

    def __str__(self):
        answers = "  - " + "\n  - ".join(self.answers)
        return (
            f"{self.label}:\n  {self.question_text} ({self.question_type})\n{answers}"
        )

    def __repr__(self):
        return f"Question({self.label})"

    _validate_label = validator("label", allow_reuse=True)(check_labels_for_spaces)

    @validator("question_type")
    def no_answers_for_yes_no_question(cls, value, values, config, field):
        "Exception if question_type is yes_no and there are answers"
        if value == "yes_no" and "answers" in values:
            answers = values["answers"]
            if answers:
                warnings.warn(
                    "There should be no answers for yes_no question type", UserWarning
                )
        return value


class Page(BaseModel):
    "General page class"
    label: str
    questions: Question | Sequence[Question]
    title: str | None = None
    description: str | None = None
    options: PageOptions | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.questions, Question):
            self.questions = [self.questions]

    @validator("questions")
    def check_labels(cls, questions):
        "Exception if there are questions with the same label"
        if not isinstance(questions, Question):
            labels = []
            for question in questions:
                labels.append(question.label)
            if len(labels) != len(set(labels)):
                raise ValueError("Questions labels in page must be unique")
        return questions

    def __str__(self):
        page = f"Page {self.label}:\n"
        for i in enumerate(self.questions):
            page += f"  {i[0] + 1}. {i[1].label}\n"
        return page

    def __repr__(self):
        return f"Page({self.label})"

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.questions[index]
        if isinstance(index, str):
            for question in self.questions:
                if question.label == index:
                    return question

    _validate_label = validator("label", allow_reuse=True)(check_labels_for_spaces)


class Survey(BaseModel):
    "General survey class"
    label: str
    pages: Page | Sequence[Page]
    title: str | None = None
    description: str | None = None
    options: SurveyOptions | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.pages, Page):
            self.pages = [self.pages]

    @validator("pages")
    def check_labels(cls, pages):
        "Exception if there are pages with the same label"
        if not isinstance(pages, Page):
            labels = []
            for page in pages:
                labels.append(page.label)
            if len(labels) != len(set(labels)):
                raise ValueError("Pages labels in survey must be unique")
        return pages

    def __str__(self):
        survey = "Survey:\n"
        for i in enumerate(self.pages):
            survey += f"  {i[0] + 1}. {i[1].label}\n"
        return survey

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.pages[index]
        if isinstance(index, str):
            for given_page in self.pages:
                if given_page.label == index:
                    return given_page

    def unpack(self, labels: bool = False) -> list[str] | list[Question]:
        "Make survey list of Questions"
        questions = []
        for page in self.pages:
            for question in page.questions:
                questions.append(question)
        if not labels:
            return questions
        labels_list = []
        for i in questions:
            labels_list.append(i.label)
        return labels_list

    def build_survey(
        self,
        path: str | Path = os.getcwd(),
        create_csv: bool = True,
        create_tar_gz: bool = True,
    ) -> None:
        """Builds survey package."""

        if isinstance(path, str):
            path = Path(path)

        path = path / self.label.casefold()

        YarnPackage(path)._run_npm("build")

        with open(path / "dist" / "fields.csv", "w", encoding="UTF8") as f:
            csv.writer(f).writerow(["id"] + self.unpack(labels=True))
        if create_tar_gz:
            with tarfile.open(path / f"{self.label}.tar.gz", "w:gz") as tar:
                for root, dirs, files in os.walk(path / "dist"):
                    for file_name in files:
                        tar.add(os.path.join(root, file_name), arcname=file_name)

    def create(
        self, path: str | Path = os.getcwd(), build: bool = True, fields: bool = True
    ):
        "Create survey"
        generate_survey(self, path=path)
        if build:
            self.build_survey(path=path)

    _validate_label = validator("label", allow_reuse=True)(check_labels_for_spaces)


class SurveyEncoder(JSONEncoder):
    "Create SurveyJS-compliant json from Question object"

    def default(self, o):
        # dictionary for mapping question types to SurveyJS types
        # "veles_argument_name": "surveyjs_argument_name
        surveyjs_types = {
            "radio": "radiogroup",
            "checkbox": "checkbox",
            "text": "text",
            "text_long": "comment",
            "dropdown": "dropdown",
            "dropdown_multi": "tagbox",
            "yes_no": "boolean",
            "ranking": "ranking",
        }

        if isinstance(o, Question):
            json = {
                "name": o.label,
                "type": surveyjs_types[o.question_type],
                "title": o.question_text,
                "description": o.description,
                "choices": o.answers,
            }

            if o.options:
                # dictionary for mapping question options to SurveyJS options
                # "veles_argument_name": ["surveyjs_argument_name", default_value]
                surveyjs_question_options = {
                    "required": ["isRequired", False],
                    "answers_order": ["choicesOrder", "none"],
                    "inherit_answers": ["choicesFromQuestion", None],
                    "inherit_answers_mode": ["choicesFromQuestionMode", "all"],
                    "comment": ["hasComment", False],
                    "comment_text": ["commentText", "Other"],
                    "comment_placeholder": ["commentPlaceHolder", ""],
                    "visible": ["visible", True],
                    "other": ["hasOther", False],
                    "other_text": ["otherText", "Other"],
                    "other_placeholder": ["otherPlaceHolder", ""],
                    "none": ["hasNone", False],
                    "none_text": ["noneText", "None"],
                    "clear_button": ["showClearButton", False],
                }
                opts = o.options.__dict__
                for key in opts.keys():
                    if opts[key] != surveyjs_question_options[key][1]:
                        json[surveyjs_question_options[key][0]] = opts[key]

        elif isinstance(o, Page):
            json = {
                "name": o.label,
                "elements": [self.default(q) for q in o.questions],
            }

            if o.title:
                json["title"] = o.title
            if o.description:
                json["description"] = o.description
            if o.options:
                # dictionary for mapping page options to SurveyJS options
                # "veles_argument_name": ["surveyjs_argument_name", default_value]
                surveyjs_page_options = {
                    "read_only": ["readOnly", False],
                    "time_limit": ["maxTimeToFinish", None],
                    "visible": ["visible", True],
                }
                opts = o.options.__dict__
                for key in opts.keys():
                    if opts[key] != surveyjs_page_options[key][1]:
                        json[surveyjs_page_options[key][0]] = opts[key]

        elif isinstance(o, Survey):
            json = {
                "title": o.title,
                "description": o.description,
                "pages": [self.default(p) for p in o.pages],
            }

            if o.options:
                # dictionary for mapping survey options to SurveyJS options
                # "veles_argument_name": ["surveyjs_argument_name", default_value]
                surveyjs_survey_options = {
                    "language": ["locale", "en"],
                    "url_on_complete": ["navigateToUrl", None],
                }
                opts = o.options.__dict__
                for key in opts.keys():
                    if opts[key] != surveyjs_survey_options[key][1]:
                        json[surveyjs_survey_options[key][0]] = opts[key]
        else:
            raise TypeError(
                f"Object of type {type(o)} is not JSON serializable by this encoder"
            )
        return json
