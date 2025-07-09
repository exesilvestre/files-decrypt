def get_category(doctype: str) -> str:
    if not doctype:
        return "Unknown"
    doctype = doctype.upper()
    if "APPRAISERSIGNATURE" in doctype:
        return "Appraiser Signature"
    if "FORM/1004" in doctype:
        return "Residential Form"
    if "FORM/REO" in doctype:
        return "REO Form"
    if "FORM/MISMO" in doctype:
        return "MISMO Form"
    if doctype.startswith("IMAGE"):
        return "Image"
    if doctype.startswith("FORM"):
        return "Generic Form"
    return "Other"