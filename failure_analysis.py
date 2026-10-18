def diagnosis_template(case_id):
    return {
        "case_id": case_id,
        "root_cause": "",
        "diagnosis": "",
        "fix": "",
        "before_score": None,
        "after_score": None,
    }
