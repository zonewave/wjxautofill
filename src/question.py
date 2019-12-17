from enum import Enum, auto
from enum import unique
from lxml import etree


@unique
class NoTableQuestion(Enum):
    radio = auto()
    checkbox = auto()
    text = auto()
    file_upload = auto()
    select = auto()
    mul_select = auto()
    sort = auto()  # 排序题
    nps = auto()  # nps 量表题


class TableQuestion(Enum):
    mul_text = auto()
    arrary_text = auto()
    table_text = auto()  #
    table_num_text = auto()
    array_radio = auto()
    array_checkbox = auto()
    # array_scaletable=array_radio
    array_ruler = auto()
    talbe_select = auto()
    proportion = auto()  # 比重题
    shopitem = auto()


@unique
class QuestionType(Enum):
    none = auto()  #
    sing = NoTableQuestion(Enum)
    table = TableQuestion(Enum)
    # radio =  auto() #


class Xpath_str:
    div_content = '//*[@id="divquestion{0}"]'


class Question:
    type = QuestionType.none
    row,col=0,0
    is_table=False
    question_id = -1

    def __init__(self, html: etree._ElementTree, question_id):
        self.question_id = question_id
        self.html = html
        self.content_xpath = Xpath_str.div_content.format(question_id)
        self.set_type(html)


    def set_type(self, html: etree._ElementTree) -> None:
        self.table_check()

    def table_check(self):
        xpath = self.html.xpath
        if xpath(self.content_xpath + '//*[@class="shop-item"]'):
            self.type = QuestionType.table.value.shopitem
        elif xpath('//*[@id="q6_1" and @class="underline"]') :
            self.type = QuestionType.table.value.mul_text
        elif xpath(self.content_xpath + '/table'):
            table_tmp = xpath(self.content_xpath + 'table[1]')
            arrflag=True
            if table_tmp[0].xpath('thead'):
                arrflag=False

            if arrflag:
                # if table_tmp[0].xpath('')
                #     // *[ @ id = "divquestion7"] / table / tbody / tr[1] / td / div / textarea


            self.type = QuestionType.table
            arrary_text = auto()
            table_text = auto()  #
            table_num_text = auto()
            array_radio = auto()
            array_checkbox = auto()
            # array_scaletable=array_radio
            array_ruler = auto()
            talbe_select = auto()
            proportion = auto()  # 比重题
