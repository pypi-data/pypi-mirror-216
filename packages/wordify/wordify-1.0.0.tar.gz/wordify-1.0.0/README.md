# wordify
Wordify is a Python class that converts a given number into its word representation. It can convert numbers up to centillions.

## Usage

1. Import the `Converter` class
    ```python
   from wordify.converter import Converter
   ```

2. Create an instance of the `Converter` class by providing a number to be converted.
    ```python
    number = "12345"
    converter = Converter(number)
    ```

3. Convert the number to its word representation using the `convert` method.
    ```python
    word_representation = converter.convert()
    ```

4. Print the word representation.
    ```python
    print(word_representation)
    ```

## Example

```python
from converter import Converter

# Create a Converter instance with a number
number = "12345"
converter = Converter(number)

# Convert the number to words
word_representation = converter.convert()

# Print the word representation
print(word_representation) # Output : twelve thousand and three hundred forty five
```

## Customization

You can set a new number for conversion using the `set_number` method.
```python
converter.set_number("987654321")
```
After setting the new number, you need to call the `convert` method again to obtain the word representation.

## License

The code in this repository is licensed under the MIT License.

You can find the full text of the license in the [LICENSE](https://github.com/fathiabdelmalek/wordify/blob/main/LICENSE) file. For more information, please visit the repository on [GitHub](https://github.com/fathiabdelmalek/wordify).