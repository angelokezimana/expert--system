from fastapi import Form
from pydantic import BaseModel


class PatientForm(BaseModel):
    age: int
    glycemie: int
    shakiness: bool
    hunger: bool
    sweating: bool
    headach: bool
    diabetic_parents: bool
    pale: bool
    urination: bool
    thirst: bool
    blurred_vision: bool
    dry_mouth: bool
    smelling_breath: bool
    shortness_of_breath: bool

    @classmethod
    def as_form(
        cls,
        age: int = Form(),
        glycemie: int = Form(),
        shakiness: bool = Form(),
        hunger: bool = Form(),
        sweating: bool = Form(),
        headach: bool = Form(),
        diabetic_parents: bool = Form(),
        pale: bool = Form(),
        urination: bool = Form(),
        thirst: bool = Form(),
        blurred_vision: bool = Form(),
        dry_mouth: bool = Form(),
        smelling_breath: bool = Form(),
        shortness_of_breath: bool = Form(),
    ):
        return cls(
            age=age,
            glycemie=glycemie,
            shakiness=shakiness,
            hunger=hunger,
            sweating=sweating,
            headach=headach,
            diabetic_parents=diabetic_parents,
            pale=pale,
            urination=urination,
            thirst=thirst,
            blurred_vision=blurred_vision,
            dry_mouth=dry_mouth,
            smelling_breath=smelling_breath,
            shortness_of_breath=shortness_of_breath,
        )
