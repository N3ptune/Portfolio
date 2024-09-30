def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            line_elements = line.strip().split(',')
            name = line_elements[0]
            zip_code = line_elements[-1]
            state = line_elements[-2]
            city = line_elements[-3]
            ad_line_2 = line_elements[-4]
            ad_line_1 = line_elements[-5]
            num_of_people = line_elements[-6]
            if ad_line_2 == '':
                new_line = f'{name}   {ad_line_1}, {city}, {state} {zip_code}     {num_of_people}\n'
                file.write(new_line)
            else:
                new_line = f'{name}   {ad_line_1}, {ad_line_2}, {city}, {state} {zip_code}      {num_of_people}\n'
                file.write(new_line)

if __name__ == '__main__':
    main('inya_jasonrachel_download.csv', 'output.txt')

