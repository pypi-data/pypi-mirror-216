'''
This is a module that contains useful functions
'''
def process(list, level=0):
     '''
     prints each item in a list even if it contains another list
     '''
     for item in list:
          if isinstance(item, list):
               process(item, level+1)
          else:
               for each_level in range(level):
                    print("\t", end='')
               print(item)