from enum import Enum,auto
from enum import unique
from lxml import etree


@unique
class Choice(Enum):
    single = auto()
    multiple = auto()
    combobox = auto()
    file_upload = auto()


@unique
class QuestionType(Enum):
    none = auto() #
    choose = Choice(Enum)
    #radio =  auto() #
   # inputtext = auto()

class QuestionQuery:
    a=0

class Xpath_str:
    div_question='//*[@id=\"divquestion'

class Question:
    type = QuestionType.none

    question_id = -1
    def __init__(self, html:etree._ElementTree,question_id):
        self.question_id = question_id
        self.set_type(html)

    def set_type(self, html:etree._ElementTree) -> None:



        switchs ={

        }
        # html.xpath('//*[@id=\"divquestion' + self.question_id +
        #            '\"]/@class=\"table\"'):
        if html.xpath('//*[@id=\"divquestion'+self.question_id+
                         '\"]//@class=\"inputtext\"'):
            self.type=QuestionType.inputtext
        elif  html.xpath()

    def is_single_chose(self):
        # // *[ @ id = "divquestion1"] / ul

        if html.xpath(Xpath_str.div_question + self.question_id +
                     '/@class="url'):
        
        if res:
            self.type = QuestionType.inputtext


