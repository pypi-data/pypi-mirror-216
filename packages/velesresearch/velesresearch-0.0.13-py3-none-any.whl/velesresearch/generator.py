"Functions for generating survey package."
from __future__ import annotations
import os
from json import dump
from pathlib import Path
import fileinput
from pynpm import YarnPackage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .structure import Survey


def generate_survey(survey_object: "Survey", path: str | Path = os.getcwd()) -> None:
    "Generates survey Vite project"

    if isinstance(path, str):
        path = Path(path)

    YarnPackage(path)._run_npm(
        "create", "vite", f"{survey_object.label.casefold()}", "--template react-ts"
    )

    path = path / survey_object.label.casefold()

    YarnPackage(path).install()
    YarnPackage(path)._run_npm(
        "add", "survey-react-ui", "@json2csv/plainjs", "file-saver"
    )
    YarnPackage(path)._run_npm("add", "@types/file-saver", "--dev")

    # App.tsx
    with open(path / "src" / "App.tsx", "w", encoding="utf-8") as app_tsx_file:
        App_tsx = """import SurveyComponent from "./SurveyComponent";

function App() {
  return <SurveyComponent />
}

export default App;"""
        app_tsx_file.write(App_tsx)

    # survey.ts
    with open(path / "src" / "survey.ts", "w", encoding="utf-8") as survey_js:
        survey_js.write("export const json = ")

    with open(path / "src" / "survey.ts", "a", encoding="utf-8") as survey_js:
        from .structure import SurveyEncoder

        dump(survey_object, survey_js, cls=SurveyEncoder)

    # SurveyComponent.tsx
    with open(
        path / "src" / "SurveyComponent.tsx", "w", encoding="utf-8"
    ) as survey_component_file:
        SurveyComponent = """import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/defaultV2.min.css";
import "./index.css";
import { json } from "./survey.ts";

function MakeID(length: number) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function SurveyComponent() {
    const survey = new Model(json);
    survey.onComplete.add((sender) => {
        const result = Object.assign({ id: MakeID(8) }, sender.data);
        // send data to Django backend
        fetch(window.location.pathname + "submit/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(result)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
    return (<Survey model={survey} />);
}

export default SurveyComponent;"""
        survey_component_file.write(SurveyComponent)

    with open(path / "src" / "index.css", "w", encoding="utf-8") as index_css:
        index_css.write("")

    with open(path / "src" / "App.css", "w", encoding="utf-8") as app_css:
        app_css.write("")

    # remove unnecessary files
    if os.path.exists(path / "public" / "vite.svg"):
        os.remove(path / "public" / "vite.svg")
    if os.path.exists(path / "src" / "assets" / "react.svg"):
        os.remove(path / "src" / "assets" / "react.svg")

    index_html = path / "index.html"
    new_line = f"    <title>{survey_object.title}</title>\n"

    # use fileinput to modify the file
    for line in fileinput.input(index_html, inplace=True):
        if "<title>" in line and "</title>" in line:
            print(new_line, end="")
        else:
            print(line, end="")
