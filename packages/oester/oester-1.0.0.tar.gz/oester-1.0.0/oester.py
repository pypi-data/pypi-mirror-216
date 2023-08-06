'''
This is module that contains useful functions
'''
def process(movies):
     '''
     prints each item in a list even if it contains another list
     '''
     for item in movies:
          if isinstance(item, list):
               process(item)
          else:
               print(item)
