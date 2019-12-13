from enum import Enum
from enum import unique
from lxml import etree


@unique
class QuestionType(Enum):
    none = 0  #
    radio = 1  #
    inputtext = 2

class QuestionQuery:
    a=0

class Question:
    type = QuestionType.none

    question_id = -1
    def __init__(self, html:etree._ElementTree,question_id):
        self.question_id = question_id
        self.set_type(html)

    def set_type(self, html:etree._ElementTree) -> None:
        res = html.xpath('//*[@id=\"divquestion'+self.question_id+
                         '\"]//@class=\"inputtext\"')

        if res:
            self.type = QuestionType.inputtext


