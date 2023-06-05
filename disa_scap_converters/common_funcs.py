#!python


def get_file_contents(file_to_parse):
    """
    read in the file contents into a list
    """
    with open(file_to_parse, encoding="utf8") as input_file:
        input_contents = input_file.read()
    return input_contents.split("><")



def fix_severity_wording(severity):
    """
    Some severities get messed up due to length not being the same
    this fixes that so that makes it consistent
    """
    if "high" in severity.lower():
        return "high"
    if "low" in severity.lower():
        return "low"
    if "medium" in severity.lower():
        return "medium"