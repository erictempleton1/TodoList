search_list = ['Pick up eggs', 'Grab some bread', 'Bank statement']

new_list = []
for items in search_list:
    new_list.append(items.split())

for item in new_list:
    if 'some' in item:
        print ' '.join(item)