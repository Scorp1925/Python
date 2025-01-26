integer = 10
float_num = 10.5
complex_num = 3+4j

sum_result = integer + float_num
product_result = integer * float_num
division_result = integer / float_num

string = "Пример строки"
multi_line_string = """Многостраничная
строка
как пример"""

concatinated_string = string + "конкатенация строки"

formated_string = f"integer: {integer}, float: {float_num}, string: {string}"

boolean_true = True
boolean_false = False

add_result = boolean_true and boolean_false
or_result = boolean_true or boolean_false
not_result = not boolean_true

print(f"Integer: {integer}, Float: {float_num}, Complex: {complex_num}")
print(f"Sum: {sum_result}, Product: {product_result}, Division: {division_result}")
print(f"String: {string}, Multi-line String {multi_line_string}")
print(f"Concatenated string: {concatinated_string}")
print(f"Formated string: {formated_string}")
print(f"Boolean True: {boolean_true}, Boolean False: {boolean_false}")
print(f"AND result: {add_result}, OR result {or_result}, NOT result: {not_result}")
