#!/usr/bin/env python
# coding: utf-8

# In[3]:


from csv import reader

#All I did here was open file, read, convert to a list of list, working with lists helps to manipulate better. I also 
# removed the header column and assigned the header to android_header. Then I assigned all the data exluding the header 
# to android. Same with the apple store data

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[4]:


#This function is just to view the data easily. As you can see in the output.
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# In[5]:


#deleted bad data here
del android[10472]
print(len(android))


# In[6]:


# This is still part of the cleaning process in data analysis. I have created an empty list for duplicate apps and unique
# apps. We want to remove all bad data. So remove duplicate entries
duplicate_apps = []
unique_apps = []
duplicate_ios_apps = []
ios_unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

for app in ios:
    name = app[0]
    if name in ios_unique_apps:
        duplicate_ios_apps.append(name)
    else:
        ios_unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])
print('\n')
print('Number of duplicate ios apps:', len(duplicate_ios_apps))



# In[8]:


#Here I have created a dictionary which hold name and key, and highest rating as value
reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print(len(reviews_max))


# In[ ]:


#further cleaning of data that may have multiple of highest reviews 
android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[ ]:


explore_data(android_clean, 0, 3, True)


# In[ ]:


# we want to check here to make sure the app is for an english audience. So we remove apps that may contain more than 3 letters
# not in the english dictionary. The number 127 is from the ascii table
def is_english(string):
    non_asciiCount = 0
    
    for character in string:
        if ord(character) > 127:
            non_asciiCount += 1
    
    if non_asciiCount > 3:
        return False
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))


# In[ ]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# In[ ]:


#Isolating The free apps

android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))

                


# In[ ]:


#Function to get frequency Tables

def freq_table(dataset,index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    table_percentages = {}
    for key in table:
        percentage = (table[key]/total) * 100
        table_percentages[key] = percentage
        
    return table_percentages

#helper function
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

#Most common apps 

display_table(ios_final, -5) #prime_genre
            


# In[ ]:


display_table(android_final, 1) #Category


# In[ ]:


# Genre in playStore
display_table(android_final, 9)


# In[ ]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)
        
    


# In[ ]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[ ]:


Reference_total = []

for app in ios_final:
    if app[-5] == 'Reference':
        Reference_total.append(float(app[7]))
        print(app[1], ':', app[7])

total = 0
for num in Reference_total:
    total += num
    avg = total/len(Reference_total)
print('reference genre average: ', avg)
    


# In[ ]:


unique_genres_ios = []

for app in ios_final:
    genre = app[-5]
    if genre not in unique_genres_ios:
        unique_genres_ios.append(genre)
print(unique_genres_ios)


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])
