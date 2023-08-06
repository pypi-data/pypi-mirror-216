def add_element(element, style, startval):
    if not isinstance(style, list):
        raise TypeError("Style must be a list.")
    else:
        returnval = startval + "\n" + element + " {\n"
        for attribute in style:
            returnval = returnval + "    " + attribute + ";\n"
        returnval = returnval + "}\n"

        return returnval