search_list = ['Pick up eggs', 'Grab some bread', 'Bank statement', 'Run some miles']
search_term = 'some'

new_list = []
for items in search_list:
    new_list.append(items.split())


for item in new_list:
    if search_term in item:
        print ' '.join(item)
        
# testing