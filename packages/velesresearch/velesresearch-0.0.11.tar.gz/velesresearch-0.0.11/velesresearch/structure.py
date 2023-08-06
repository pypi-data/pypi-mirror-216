"Structural elements of the survey"
from __future__ import annotations
import os
from pathlib import Path
from collections.abc import Sequence
import csv
import tarfile
from json import JSONEncoder
from pydantic import BaseModel, validator
import numpy as np
from pynpm import YarnPackage
from .options import QuestionOptions, PageOptions, SurveyOptions
from .generator import generate_survey


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
            for page in self.pages:
                if page.label == index:
                    return page

    def unpack(self, labels: bool = False):
        "Make survey list of Questions"
        questions = []
        for page in self.pages:
            for question in page.questions:
                questions.append(question)
        if not labels:
            return questions
        labels = []
        for i in questions:
            labels.append(i.label)
        return labels

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


class SurveyEncoder(JSONEncoder):
    "Create SurveyJS-compliant json from Question object"

    def default(self, o):
        # dictionary for mapping question types to SurveyJS types
        surveyjs_types = {"radio": "radiogroup", "checkbox": "checkbox"}

        if isinstance(o, Question):
            json = {
                "name": o.label,
                "type": surveyjs_types[o.question_type],
                "title": o.question_text,
                "choices": o.answers,
            }

            if o.options:
                # dictionary for mapping question options to SurveyJS options
                surveyjs_question_options = {
                    "required": ["isRequired", False],
                    "answers_order": ["choicesOrder", "none"],
                    "inherit_answers": ["choicesByUrl", None],
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
            # dictionary for mapping page options to SurveyJS options
            surveyjs_page_options = {
                "read_only": ["readOnly", False],
                "time_limit": ["maxTimeToFinish", None],
                "visible": ["visible", True],
            }

            json = {
                "name": o.label,
                "elements": [self.default(q) for q in o.questions],
            }

            if o.title:
                json["title"] = o.title
            if o.description:
                json["description"] = o.description
            if o.options:
                opts = o.options.__dict__
                for key in opts.keys():
                    if opts[key] != surveyjs_page_options[key][1]:
                        json[surveyjs_page_options[key][0]] = opts[key]

        if isinstance(o, Survey):
            # dictionary for mapping survey options to SurveyJS options
            surveyjs_survey_options = {
                "language": ["locale", "en"],
                "url_on_complete": ["navigateToUrl", None],
            }

            json = {
                "title": o.title,
                "description": o.description,
                "pages": [self.default(p) for p in o.pages],
            }

            if o.options:
                opts = o.options.__dict__
                for key in opts.keys():
                    if opts[key] != surveyjs_survey_options[key][1]:
                        json[surveyjs_survey_options[key][0]] = opts[key]

        return json
