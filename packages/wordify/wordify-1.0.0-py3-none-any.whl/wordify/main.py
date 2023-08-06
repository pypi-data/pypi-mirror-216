p = 0
m = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion",
     "decillion", "un-decillion", "duo-decillion", "tre-decillion", "quattuor-decillion", "quin-decillion", "sex-decillion", "septen-decillion", "octo-decillion", "novem-decillion",
     "vigintillion", "un-vigintillion", "duo-vigintillion", "tres-vigintillion", "quattuor-vigintillion", "quin-vigintillion", "ses-vigintillion", "septen-vigintillion", "octo-vigintillion", "novem-vigintillion",
     "trigintillion", "un-trigintillion", "duo-trigintillion", "tres-trigintillion", "quattour-trigintillion", "quin-trigintillion", "ses-trigintillion", "septen-trigintillion", "otcto-trigintillion", "novem-trigintillion",
     "quadragintillion", "un-quadragintillion", "duo-quadragintillion", "tre-quadragintillion", "quattuor-quadragintillion", "quin-quadragintillion", "sex-quadragintillion", "septen-quadragintillion", "octo-quadragintillion", "novem-quadragintillion",
     "quinquagintillion", "un-quinquagintillion", "duo-quinquagintillion", "tre-quinquagintillion", "quattuor-quinquagintillion", "quin-quinquagintillion", "sex-quinquagintillion", "septen-quinquagintillion", "octo-quinquagintillion", "novem-quinquagintillion",
     "sexagintillion", "un-sexagintillion", "duo-sexagintillion", "tre-sexagintillion", "quattuor-sexagintillion", "quin-sexagintillion", "sex-sexagintillion", "septen-sexagintillion", "octo-sexagintillion", "novem-sexagintillion",
     "septuagintillion", "un-septuagintillion", "duo-septuagintillion", "tre-septuagintillion", "quattuor-septuagintillion", "quin-septuagintillion", "sex-septuagintillion", "septen-septuagintillion", "octo-septuagintillion", "novem-septuagintillion",
     "octogintillion", "un-octogintillion", "duo-octogintillion", "tre-octogintillion", "quattuor-octogintillion", "quin-octogintillion", "sex-octogintillion", "septen-octogintillion", "octo-octogintillion", "novem-octogintillion",
     "nonagintillion", "un-nonagintillion", "duo-nonagintillion", "tre-nonagintillion", "quattuor-nonagintillion", "quin-nonagintillion", "sex-nonagintillion", "septen-nonagintillion", "octo-nonagintillion", "novem-nonagintillion",
     "centillion"]


def prepare_number(num):
    if len(num) % 3 == 1:
        num = '00' + num
    elif len(num) % 3 == 2:
        num = '0' + num
    return num


def write_ones(num):
    switch = {
        '9': 'nine',
        '8': 'eight',
        '7': 'seven',
        '6': 'six',
        '5': 'five',
        '4': 'four',
        '3': 'three',
        '2': 'two',
        '1': 'one',
        '0': '',
    }
    return switch.get(num, "Invalid Input")


def write_tens(num):
    switch = {
        '9': 'ninety',
        '8': 'eighty',
        '7': 'seventy',
        '6': 'sixty',
        '5': 'fifty',
        '4': 'forty',
        '3': 'thirty',
        '2': 'twenty',
        '0': '',
    }
    return switch.get(num, "Invalid Input")


def write_tens_of_ten(num):
    switch = {
        '19': 'nineteen',
        '18': 'eighteen',
        '17': 'seventeen',
        '16': 'sixteen',
        '15': 'fifteen',
        '14': 'fourteen',
        '13': 'thirteen',
        '12': 'twelve',
        '11': 'eleven',
        '10': 'ten',
    }
    return switch.get(num, "Invalid Input")


def fun(num):
    global p
    res = ""
    if num[0] != '0':
        res += write_ones(num[0]) + " hundred "
    if num[1] != '0':
        if num[1] != '1':
            res += write_tens(num[1]) + " "
            res += write_ones(num[2]) + " "
        else:
            res += write_tens_of_ten(f"{num[1]}{num[2]}") + " "
    else:
        res += write_ones(num[2]) + " "
    res += f"{m[p]} and "
    p += 1
    return res


def translate(num):
    lst = []
    result = ""
    for i in range(len(num) - 3, -1, -3):
        lst.insert(0, fun(num[i:i + 3]))
    for n in lst:
        result += n
    return result[:-6]


number = prepare_number(str(input("Enter a number : ")))
print(translate(number))
