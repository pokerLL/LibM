import random
#引用Faker库生成伪数据
import faker
#实例化，将变量保存至fk，传参数‘zh_CN'来生成中文随机数据
fk = faker.Faker("zh_CN")

#随机生成名字
def username():
    return fk.name()


def categorylist():

    category = ["考研资料","四六级英语","历史","科技","地理人文","论文","课外读物","军事", "都市", "玄幻","医疗","名著","课内资源",
                "艺术","哲学","科普","政治","宗教","法律","美学","心理","天文","考古","冒险"]
    return category


def publisher():
    publishers = ['师范大学出版社', '教育出版社', '课程教材发展中心', '大学出版社']
    return fk.city_name()+random.choice(publishers)


def bookname():
    book_name = ["天虚空", "玄派", "狂浪乾坤", "纯阳极", "天霸", "玄冰仙", "鬼镜", "极杀", "禅风暴", "无限凶", "两仪天", "仙武道", "天仙九天", "无情秘", "归元寒",
                 "无相魅", "武动神", "双极焰", "醉凶", "玄派", "断情斗", "柔神", "天圣", "太极九重天", "妖九重天", "仙阴", "先天独尊", "阳天道", "凶杀", "魅疾",
                 "战神地煞", "妖秘", "冻荒", "幽宇宙", "天仙影", "神梦", "杀变", "玄派", "冥武", "天海天罡", "七曜传说", "狂战", "仙九重天", "幻风暴", "风刃天地",
                 "冻荒", "绝情极", "武动绝", "六壬冽", "斩钢天河", "宝神", "仙魅", "不死梦", "九宫曲", "气冲天", "玄派", "万里传承", "惊疾", "钢霸", "阴阳皇",
                 "终极焰", "武动梦", "霸巅峰", "神鬼", "两仪炎", "玄派", "惊天梦", "至尊天煞", "魅妖", "紫微玄天", "无极冻", "幽天罗", "邪玄", "天地重生", "魔战",
                 "绝对重生", "冥梦", "斗杀", "极品天煞", "日月镜", "先天刚", "气冲苍穹", "元始狂", "玄派", "炼玄", "天烈", "邪疾", "魂圣", "剑道霸", "八卦烈",
                 "宝天河", "傲世寒", "毒天极", "魔荒", "超级天煞", "天海天", "横扫传承", "武动武", "魅传", "极品焚", "山河天地", "玄派", "鬼天道", "鬼玄天",
                 "星象巅峰", "绝地鬼", "千里凶", "唯我宇宙", "紫微地煞", "百里秘", "锋玄", "狂浪炼", "镜战", "刚刚", "惊九重天", "焰王座", "新狂", "不灭动",
                 "宝禅", "玄派", "至高影", "秘幻", "狂独尊", "极锋", "风云荒", "紫微九天", "冥邪", "蛊神"]
    return fk.first_name() + fk.first_name() + random.choice(book_name)


def account():
    return chr(random.randint(65, 90)) + fk.ean8()


def sentence():
    return fk.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)


def gender():
    gender = ["man", "woman", "unknown"]
    return random.choice(gender)


def datebefore():
    return fk.date_time_this_century(before_now=True, after_now=False, tzinfo=None)


def dateafter():
    return fk.date_time_this_century(before_now=False, after_now=True, tzinfo=None)


def chapters():
    str = "出世"
    for i in range(random.randint(10, 50)):
        str = str + "," + fk.word(ext_word_list=None)
    return str

# if __name__ == "__main__":
#     ls = []
#     for i in range(30):
#         ls.append(publisher())
#     print(ls)
