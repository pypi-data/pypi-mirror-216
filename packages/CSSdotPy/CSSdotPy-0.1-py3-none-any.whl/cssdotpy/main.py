from cssdotpy.addelement import add_element
from cssdotpy.addclass import add_class
from cssdotpy.addevent import add_event_to_element, add_event_to_class

class CSS():
    def __init__(self):
        self.__css__ = ""
    def addElement(self, element, style):
        self.__css__ = add_element(element=element, style=style, startval=self.__css__)
    def addClass(self, name, style):
        self.__css__ = add_class(name=name, style=style, startval=self.__css__)
    def addEventToElement(self, element, event, style):
        self.__css__ = add_event_to_element(element=element, event=event, style=style, startval=self.__css__)
    def addEventToClass(self, name, event, style):
        self.__css__ = add_event_to_class(name=name, event=event, style=style, startval=self.__css__)
    def returnCSS(self):
        return self.__css__

