def clean_metadata_keys(metadata: dict) -> dict:
    clean = {}

    for k, v in metadata.items():
        key = k.replace("\x00", "")
        value = v.replace("\x00", "")

        # Normalize key patterns
        if key.startswith("%%DOCU"):
            key = "DOCTYPE"

        clean[key] = value

    return clean
