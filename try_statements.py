c = 0

while True:
    try:
        x = int(input('Enter a number: '))
        break
    except ValueError:                          #I can add any type of exceptions
        print('That\'s not a valid number!')    #I can use different block or expections list in the except block.
    except KeyboardInterrupt:
        print('\nNo input taken!')
        break
    finally:
        c+=1
        print('\nAttempted Input {}\n'.format(c))
