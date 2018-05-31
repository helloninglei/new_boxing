from pypinyin import pinyin, Style


def hans_to_initial(hans):
    """返回中文词组第一个汉字的首字母"""
    first_hans = hans[0]
    first_letter = pinyin(first_hans, style=Style.FIRST_LETTER)
    return first_letter[0][0].upper()
