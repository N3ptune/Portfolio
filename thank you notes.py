def main(outfile):
    while True:
        mode = input('What mode? ')
        if mode == 'single':
            guest = input('Guest: ')
            adj = input("Adjective: ")
            gift = input("Gift: ")
            nice_thing = input('Nice thing: ')

            with open(outfile, 'a') as file:
                phrase = f"Dear {guest},\n\nThank you for the {adj} {gift}. {nice_thing}. We have both wanted one of those for so long!! We're so lucky to have such a thoughtful person like you in our lives. Thank you again for thinking of us and helping us celebrate this happy time in our lives.\n\nFondly, \n\nRachel and Jason Brooks\n\n"
                file.write(phrase)
            print("Note added")
        elif mode == 'double':
            guest = input('Guest(s): ')
            adj = input("Adjective: ")
            gift = input("Gift: ")
            nice_thing = input('Nice thing: ')

            with open(outfile, 'a') as file:
                phrase = f"Dear {guest},\n\nThank you for the {adj} {gift}. {nice_thing}. We have both wanted one of those for so long!!  We're so lucky to have such thoughtful people in our lives. Thank you again for thinking of us and helping us celebrate this happy time in our lives.\n\nFondly, \n\nRachel and Jason Brooks\n\n"
                file.write(phrase)
                print("Note added")
        else:
            print("All done!")
            break


def main_revised(output):
    while True:
        mode = input('What mode?')
        if mode == 'single'.lower():
            guest = input('Guest: ')
            adj = input("Adjective: ")
            gift = input("Gift: ")
            nice_thing = input('Nice thing: ')
            with open(output, 'a') as file:
                phrase = f"Thank you for the {adj} {gift}. {nice_thing}. We have both wanted one of those for so long!! We're so lucky to have such a thoughtful person like you in our lives. Thank you again for thinking of us and helping us celebrate this happy time in our lives."
                file.write(f"{guest}:      {phrase}")
        elif mode == 'double'.lower():
            guest = input('Guest: ')
            adj = input("Adjective: ")
            gift = input("Gift: ")
            nice_thing = input('Nice thing: ')
            with open(output, 'a') as file:
                phrase = f"Thank you for the {adj} {gift}. {nice_thing}. We have both wanted one of those for so long!!  We're so lucky to have such thoughtful people in our lives. Thank you again for thinking of us and helping us celebrate this happy time in our lives."
                file.write(f"{guest}:      {phrase}")
        else:
            print('All done!')
            break

            
if __name__ == '__main__':
    main_revised('thank_you_revised.txt')
