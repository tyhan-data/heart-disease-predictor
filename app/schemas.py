from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum


class SexInfo(str, Enum):
    Male = "M"
    Female = "F"


class ChestPainTypeInfo(str, Enum):
    ATA = "ATA"
    NAP = "NAP"
    TA = "TA"
    ASY = "ASY"


class FastingBSInfo(str, Enum):
    No = '0'
    Yes = '1'


class RestingECGInfo(str, Enum):
    Normal = "Normal"
    ST = "ST"
    LVH = "LVH"


class ExerciseAnginaInfo(str, Enum):
    No = "N"
    Yes = "Y"


class STSlopeInfo(str, Enum):
    Up = "Up"
    Flat = "Flat"
    Down = "Down"


# Input data
class HeartDiseaseInput(BaseModel):

    Age: Annotated[
        int,
        Field(
            ...,
            ge=18,
            le=100,
            title="Age",
            examples=[40]
        )
    ]

    Sex: SexInfo

    ChestPainType: ChestPainTypeInfo  
    RestingBP: Annotated[
        int,
        Field(
            ...,
            ge=80,
            le=200,
            title="Resting Blood Pressure (mmHg)",
            examples=[120]
        )
    ]

    Cholesterol: Annotated[
        int,
        Field(
            ...,
            ge=85,
            le=600,
            title="Serum Cholesterol",
            examples=[200]
        )
    ]

    FastingBS: FastingBSInfo

    RestingECG: RestingECGInfo

    MaxHR: Annotated[
        int,
        Field(
            ...,
            ge=60,
            le=220,
            title="Maximum Heart Rate",
            examples=[150]
        )
    ]

    ExerciseAngina: ExerciseAnginaInfo

    Oldpeak: Annotated[
        float,
        Field(
            ...,
            ge=0,
            le=6,
            title="ST Depression",
            examples=[1.0]
        )
    ]

    ST_Slope: STSlopeInfo


# Prediction response
class HeartDiseasePrediction(BaseModel):
    HeartDisease: int
    probability: float