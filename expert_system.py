from experta import *

"""
    Expert system for diagnosing diabetes in children
    @author: Kezimana Aimé Angelo.
"""


class Patient(Fact):
    """Info about the patient"""

    pass


def SUMFIELDS(p, *fields):
    return sum([p.get(x, 0) for x in fields])


class InreferenceEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.results = []

    @Rule(Patient(age=P(lambda x: x <= 5)))
    def concerned_person(self):
        self.declare(Fact(concerned=True))

    @Rule(Fact(concerned=True), Patient(glycemie=MATCH.glycemie))
    def hyper_glycemy(self, glycemie):
        if glycemie > 10:
            self.declare(Fact(hyperglycemic_risk=True))
            self.results.append("Warning! High blood sugar")
        else:
            self.declare(Fact(hyperglycemic_risk=False))

    @Rule(Fact(concerned=True), Patient(glycemie=MATCH.glycemie))
    def hypo_glycemy(self, glycemie):
        if glycemie < 4:
            self.results.append("Warning! Low blood sugar")
            self.declare(Fact(hypoglycemic_risk=True))
        else:
            self.declare(Fact(hypoglycemic_risk=False))

    @Rule(
        Fact(concerned=True),
        AS.p << Patient(),
        TEST(
            lambda p: SUMFIELDS(p, "shakiness", "hunger", "sweating", "headach", "pale")
            > 2
        ),
    )
    def has_signs_low_sugar(self, p):
        self.declare(Fact(has_signs_low_sugar=True))

    # If the patient is a child and has one or many signes or his blood sugar level is low
    @Rule(
        Fact(concerned=True),
        Fact(has_diabetic_parents=True),
        Fact(has_signs_low_sugar=True),
    )
    def protocole_risk_low(self):
        self.results.append("Warning! Child could be diabetic")

    # If the patient is a child and has one or many signes, and his blood sugar level is low and passed the test
    @Rule(
        Fact(concerned=True),
        Fact(hypoglycemic_risk=True),
        Fact(has_signs_low_sugar=True),
    )
    def protocole_alert_low(self):
        self.results.append("Alert! High risk of diabetes, Child must see a doctor")

    # If the patient is child and has at least one of his parents diabetic
    @Rule(Fact(concerned=True), Patient(diabetic_parents=True))
    def has_diabetic_parents(self):
        self.declare(Fact(has_diabetic_parents=True))

    @Rule(
        Fact(concerned=True),
        AS.p << Patient(),
        TEST(
            lambda p: SUMFIELDS(
                p,
                "urination",
                "thirst",
                "blurred_vision",
                "headach",
                "dry_mouth",
                "smelling_breath",
                "shortness_of_breath",
            )
            > 2
        ),
    )
    def has_signs_high_sugar(self, **_):
        self.declare(Fact(has_signs_high_sugar=True))

    @Rule(
        Fact(concerned=True),
        Fact(has_diabetic_parents=True),
        Fact(has_signs_high_sugar=True),
    )
    def protocole_risk_high(self):
        self.results.append("Warning! Child could be diabetic")

    @Rule(
        Fact(concerned=True),
        Fact(hyperglycemic_risk=True),
        Fact(has_signs_high_sugar=True),
    )
    def protocole_alert_high(self):
        self.results.append("Alert! High risk of diabetes, Child must see a doctor")
