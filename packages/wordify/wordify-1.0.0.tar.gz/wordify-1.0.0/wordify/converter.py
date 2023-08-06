class Converter:
    """
    A class for converting numbers to words.
    """

    _number_names = [
        "", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion",
        "septillion", "octillion", "nonillion", "decillion", "un-decillion", "duo-decillion",
        "tre-decillion", "quattuor-decillion", "quin-decillion", "sex-decillion", "septen-decillion",
        "octo-decillion", "novem-decillion", "vigintillion", "un-vigintillion", "duo-vigintillion",
        "tres-vigintillion", "quattuor-vigintillion", "quin-vigintillion", "ses-vigintillion",
        "septen-vigintillion", "octo-vigintillion", "novem-vigintillion", "trigintillion",
        "un-trigintillion", "duo-trigintillion", "tres-trigintillion", "quattour-trigintillion",
        "quin-trigintillion", "ses-trigintillion", "septen-trigintillion", "otcto-trigintillion",
        "novem-trigintillion", "quadragintillion", "un-quadragintillion", "duo-quadragintillion",
        "tre-quadragintillion", "quattuor-quadragintillion", "quin-quadragintillion",
        "sex-quadragintillion", "septen-quadragintillion", "octo-quadragintillion",
        "novem-quadragintillion", "quinquagintillion", "un-quinquagintillion", "duo-quinquagintillion",
        "tre-quinquagintillion", "quattuor-quinquagintillion", "quin-quinquagintillion",
        "sex-quinquagintillion", "septen-quinquagintillion", "octo-quinquagintillion",
        "novem-quinquagintillion", "sexagintillion", "un-sexagintillion", "duo-sexagintillion",
        "tre-sexagintillion", "quattuor-sexagintillion", "quin-sexagintillion", "sex-sexagintillion",
        "septen-sexagintillion", "octo-sexagintillion", "novem-sexagintillion", "septuagintillion",
        "un-septuagintillion", "duo-septuagintillion", "tre-septuagintillion",
        "quattuor-septuagintillion", "quin-septuagintillion", "sex-septuagintillion",
        "septen-septuagintillion", "octo-septuagintillion", "novem-septuagintillion", "octogintillion",
        "un-octogintillion", "duo-octogintillion", "tre-octogintillion", "quattuor-octogintillion",
        "quin-octogintillion", "sex-octogintillion", "septen-octogintillion", "octo-octogintillion",
        "novem-octogintillion", "nonagintillion", "un-nonagintillion", "duo-nonagintillion",
        "tre-nonagintillion", "quattuor-nonagintillion", "quin-nonagintillion", "sex-nonagintillion",
        "septen-nonagintillion", "octo-nonagintillion", "novem-nonagintillion", "centillion"
    ]

    _ones_names = {
        '9': 'nine', '8': 'eight', '7': 'seven', '6': 'six', '5': 'five',
        '4': 'four', '3': 'three', '2': 'two', '1': 'one', '0': '',
    }

    _tens_names = {
        '9': 'ninety', '8': 'eighty', '7': 'seventy', '6': 'sixty', '5': 'fifty',
        '4': 'forty', '3': 'thirty', '2': 'twenty', '0': '',
    }

    _tens_of_ten_names = {
        '19': 'nineteen', '18': 'eighteen', '17': 'seventeen', '16': 'sixteen',
        '15': 'fifteen', '14': 'fourteen', '13': 'thirteen', '12': 'twelve',
        '11': 'eleven', '10': 'ten',
    }

    def __init__(self, number):
        """
        Initialize the Converter with a number.

        Args:
            number (str): The number to be converted.
        """
        self.original_number = number
        self.padded_number = self._pad_number()
        self._position = 0

    def _pad_number(self):
        """
        Pad the number with zeros to make its length divisible by 3.

        Returns:
            str: The padded number.
        """
        padding = (3 - len(self.original_number) % 3) % 3
        return '0' * padding + self.original_number

    def _convert_ones(self, digit):
        """
        Convert a single-digit number to its corresponding word.

        Args:
            digit (str): The single-digit number to be converted.

        Returns:
            str: The word representation of the number.
        """
        return self._ones_names.get(digit, "Invalid Input")

    def _convert_tens(self, digit):
        """
        Convert a tens place digit to its corresponding word.

        Args:
            digit (str): The tens place digit to be converted.

        Returns:
            str: The word representation of the number.
        """
        return self._tens_names.get(digit, "Invalid Input")

    def _convert_tens_of_ten(self, number):
        """
        Convert a number in the tens-of-ten range (10-19) to its corresponding word.

        Args:
            number (str): The number in the tens-of-ten range to be converted.

        Returns:
            str: The word representation of the number.
        """
        return self._tens_of_ten_names.get(number, "Invalid Input")

    def _convert_group_to_word(self, group):
        """
        Convert a group of three digits to its corresponding word representation.

        Args:
            group (str): The group of three digits to be converted.

        Returns:
            str: The word representation of the group.
        """
        res = ""
        if group[0] != '0':
            res += self._convert_ones(group[0]) + " hundred "
        if group[1] != '0':
            if group[1] != '1':
                res += self._convert_tens(group[1]) + " "
                res += self._convert_ones(group[2]) + " "
            else:
                res += self._convert_tens_of_ten(f"{group[1]}{group[2]}") + " "
        else:
            res += self._convert_ones(group[2]) + " "
        res += f"{self._number_names[self._position]} and "
        self._position += 1
        return res

    def set_number(self, new_number):
        """
        Sets a new number for conversion.

        Args:
            new_number (str): The new number to be converted.

        Returns:
            None
        """
        self.original_number = new_number
        self.padded_number = self._pad_number()
        self._position = 0

    def convert(self):
        """
        Convert the number to its word representation.

        Returns:
            str: The word representation of the number.
        """
        result = ""
        for i in range(len(self.padded_number) - 3, -1, -3):
            group = self.padded_number[i:i + 3]
            result = self._convert_group_to_word(group) + result
        return result[:-6]


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        number = str(sys.argv[1])
    else:
        number = str(input("Enter a number "))
    converter = Converter(number)
    print(converter.convert())
