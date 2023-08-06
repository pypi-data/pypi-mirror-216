'''
This is module that contains useful functions
'''
def process(movies, indent = False,level=0):
     '''
     prints each item in a list even if it contains another list
     set indent : True to enable indent, level: the number of levels for indenting
     '''
     for item in movies:
          if isinstance(item, list):
               process(item,indent, level+1)
          else:
               if indent:
                    print("\t" * level, end='')
               print(item)