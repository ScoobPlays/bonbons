age = (int(input('How old are you? ')))
year_for_age = (int(input('What year do you wanna go to see your age? ')))

year_right_now = (int(2021))
age_variable_one = year_for_age - year_right_now + age

print(f'You will be {age_variable_one} in {year_for_age}.')
