def get_category(doctype: str) -> str:
    if not doctype:
        return "Unknown"
    doctype = doctype.upper()

    checks = [
        ("APPRAISERSIGNATURE", "Appraiser Signature"),
        ("FORM/1004", "Residential Form"),
        ("FORM/REO", "REO Form"),
        ("FORM/MISMO", "MISMO Form"),
    ]

    for key, category in checks:
        if key in doctype:
            return category

    return "Unknown"
