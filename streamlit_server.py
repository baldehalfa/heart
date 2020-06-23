import streamlit as st
import datetime
from enum import Enum, auto


class InputType(Enum):
    Numerical = auto()
    Categorical = auto()
    Date = auto()

    def get_input(self, label, options=None):
        if self == InputType.Numerical:
            return st.sidebar.number_input(label)
        elif self == InputType.Categorical:
            if options == None:
                raise ValueError("Please speicify options")
            return st.sidebar.selectbox(label, options)
        else:
            return st.sidebar.date_input(
                label,
                value=datetime.datetime(1970, 1, 1),
                min_value=datetime.datetime(1900, 1, 1, 0, 0),
                max_value=datetime.datetime.now(),
            )


class InputData:
    def __init__(self, label, input_type, options=None):
        self.label = label
        self.input_type = input_type
        self.options = options

        if input_type == InputType.Categorical and options == None:
            raise ValueError(
                "Categorical input should have types as categories which should be a dict type or an iterable"
            )

    def get_options_labels(self):
        if self.input_type != InputType.Categorical:
            return None
        if isinstance(self.options, dict):
            return list(self.options.keys())
        else:
            return self.options

    def convert(self, key):
        if self.input_type != InputType.Categorical:
            return key
        if isinstance(self.options, dict) and key in self.options:
            return self.options[key]
        else:
            return key


inputs = {
    "date": InputData("Date of birth", InputType.Date),
    "gender": InputData("Gender", InputType.Categorical, {"male": 0, "female": 1}),
    "cp": InputData(
        "Chest pain type",
        InputType.Categorical,
        {
            "typical angina": 1,
            "atypical angina": 2,
            "non-anginal pain": 3,
            "asymptomatic": 4,
        },
    ),
    "restbps": InputData("Resting blood pressure (mm Hg)", InputType.Numerical),
    "chol": InputData("Serum cholesterol (mg/dl)", InputType.Numerical),
    "fbs": InputData("Fasting blood sugar (mg/dl)", InputType.Numerical),
    "restecg": InputData(
        "Resting electrocardiographic results",
        InputType.Categorical,
        {
            "normal": 0,
            "having ST-T wave abnormality": 1,
            "showing probable or definite left ventricular hypertropy by Estes criteria": 2,
        },
    ),
    "thalach": InputData("Maximum heart rate achieved (bpm)", InputType.Numerical),
    "exang": InputData(
        "Exercise induced angina", InputType.Categorical, {"Yes": 1, "No": 0}
    ),
    "oldpeak": InputData(
        "ST depression induced by exercise relative to rest", InputType.Numerical
    ),
    "slope": InputData(
        "The slope of the peak exercise ST-segment",
        InputType.Categorical,
        {"upsloping value": 1, "flat value": 2, "downsloping value": 3},
    ),
    "ca": InputData(
        "Number of major vessels uncolored by flouroscopy",
        InputType.Categorical,
        [0, 1, 2, 3],
    ),
    "thal": InputData(
        "Thalassemia-caused Defect",
        InputType.Categorical,
        {"normal": 3, "fixed defect": 6, "reversible defect": 7},
    ),
}
inputs_data = {}


def model_converter(data):
    new_data = {}
    # process current data
    for k, v in data.items():
        new_data[k] = inputs[k].convert(v)

    # add age data (special)
    new_data["age"] = (datetime.date.today() - data["date"]).days // 356
    new_data["fbs"] = 0 if data["fbs"] < 120 else 1
    del new_data["date"]
    return new_data


def model_runner(data):
    data = model_converter(data)

    # run the model here and return the result so it can be rendered
    import random

    return random.randint(1, 100)


old = 0


def main():
    old = 0
    # st.title(f"Chance of having Heart Disease Finder {result}%")

    st.sidebar.title("Inputs")

    for k, v in inputs.items():
        inputs_data[k] = v.input_type.get_input(v.label, v.get_options_labels())

    result = model_runner(inputs_data)

    st.title(f"Chance of having Heart Disease {result}%")
    # st.subheader(f"Percentage of getting a heart disease of this patient is: {result}%")

    progress_bar = st.progress(old)
    progress_bar.progress(result)

    old = result


if __name__ == "__main__":
    main()
