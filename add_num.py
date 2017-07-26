total = 0

with open('../secondThou.txt', 'r') as inp:
   for line in inp:
       try:
           num = float(line)
           total += num
       except ValueError:
           print('{} is not a number!'.format(line))

print('Total of all numbers: {}'.format(total))
