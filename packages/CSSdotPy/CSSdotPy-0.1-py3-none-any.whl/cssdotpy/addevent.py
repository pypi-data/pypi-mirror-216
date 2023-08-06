def add_event_to_element(element, event, style, startval):
    if not isinstance(style, list):
        raise TypeError("Style must be a list.")
    else:
        returnval = startval + "\n" + element + ":" + event + " {\n"
        for attribute in style:
            returnval = returnval + "    " + attribute + ";\n"
        returnval = returnval + "}\n"

        return returnval
    
def add_event_to_class(name, event, style, startval):
    if not isinstance(style, list):
        raise TypeError("Style must be a list.")
    else:
        returnval = startval + "\n." + name + ":" + event + " {\n"
        for attribute in style:
            returnval = returnval + "    " + attribute + ";\n"
        returnval = returnval + "}\n"

        return returnval