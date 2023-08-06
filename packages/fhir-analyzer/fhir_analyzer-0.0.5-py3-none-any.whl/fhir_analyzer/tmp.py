from fhir_analyzer.patient_similarity.patsim import Patsim
import json
import os
print(os.getcwd())

ex = {
    "resourceType": "Observation",
    "id": "f9c5653f-a8c8-4c07-89d9-e7e66dcce4c8",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "vital-signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "55284-4",
                "display": "Blood Pressure",
            }
        ],
        "text": "Blood Pressure",
    },
    "subject": {"reference": "urn:uuid:67816396-e325-496d-a6ec-c047756b7ce4"},
    "encounter": {"reference": "urn:uuid:3c16aa88-87cb-4d82-a640-89b52750f543"},
    "effectiveDateTime": "2009-12-20T22:52:53-05:00",
    "issued": "2009-12-20T22:52:53.991-05:00",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic Blood Pressure",
                    }
                ],
                "text": "Diastolic Blood Pressure",
            },
            "valueQuantity": {
                "value": 83.85333428922644,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic Blood Pressure",
                    }
                ],
                "text": "Systolic Blood Pressure",
            },
            "valueQuantity": {
                "value": 116.43901482684636,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
    ],
}

patsim = Patsim()
with open("../data/bundles/test_bundle_001.json", "r") as f:
    bundle = json.load(f)
    patsim.add_bundle(bundle)
patsim.add_coded_concept_feature(
    name="Diagnoses",
    resource_types=["Condition"],
    code_paths=["code.coding.code"],
    system_paths=["code.coding.system"],
)
print(patsim.feature_df)
