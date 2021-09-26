#Inputs

age = input('How old are you? ')
years_in_the_future = input('How many years do you wanna go into the future (10, 20, 30) to see your age? ')
current_year = 2021

#Variables

age_in_the_future = (int(age)) + (int(years_in_the_future))
the_year_in_the_future = (int(age) + int(years_in_the_future) + int(current_year))

#Print Command

print(f'Your age at {the_year_in_the_future} is gonna be {age_in_the_future}.')
