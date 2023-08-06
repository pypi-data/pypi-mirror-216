def add_class(name, style, startval):
    if not isinstance(style, list):
        raise TypeError("Style must be a list.")
    else:
        returnval = startval + "\n." + name + " {\n"
        for attribute in style:
            returnval = returnval + "    " + attribute + ";\n"
        returnval = returnval + "}\n"

        return returnval