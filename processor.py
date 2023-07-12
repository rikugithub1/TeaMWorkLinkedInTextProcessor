import resource
import os
import pandas as pd
import numpy as np
import re


# Works only if all every post has reactions, comments, and reposts
# Otherwise, 'None' will be shown since it skips 
file_name = "./linkedin-stats-unprocessed.txt"

print(f'File Size is {os.stat(file_name).st_size / (1024 * 1024)} MB')

txt_file = open(file_name)

count = 0

lst = []

df = pd.DataFrame()

post = 1
prev_line = ''

posts = []
reactions = []
comments = []
reposts = []

# image = 0, video = 1, other (repost, text, link) = 2
post_types = [1,0,2,2,0,1,0,0,0,0,1,0,0,2,0,0,0,0,2,2,2,2,0,0,0,1,0,0,2,2,0,0,0,2,2,2,2,2,2,1,2,0,0,2,0,0,2,2,0]

for line in txt_file:
    if re.match(r'^[\d,]+ comments$', line):
        reactions.append(int(re.sub("[^\d\.]", "", prev_line.strip())))
        comments.append(int(re.sub("[^\d\.]", "", line.strip())))

    elif re.match(r'^[\d,]+ reposts$', line):
        reposts.append(int(re.sub("[^\d\.]", "", line.strip())))
        posts.append(post)
        post += 1
    
    prev_line = line
    

txt_file.close()

posts.reverse()  # Reverse the list of posts

# Ensure all lists have the same length
max_len = max(len(posts), len(reactions), len(comments), len(reposts))
posts += [None] * (max_len - len(posts))
reactions += [None] * (max_len - len(reactions))
comments += [None] * (max_len - len(comments))
reposts += [None] * (max_len - len(reposts))

data = {
    'Post Order (Old To New)': posts,
    'Reactions': reactions,
    'Comments': comments,
    'Reposts': reposts,
}

df = pd.DataFrame(data)

df = df.sort_values(by='Post Order (Old To New)', ascending=True)

# Calculate C2R ratio
df['C2R'] = df['Comments'] / df['Reactions']

# Calculate maximum C2R
max_c2r = df['C2R'].max()

# Calculate the number of posts with C2R greater than average
posts_above_avg_c2r = df[df['C2R'] > df['C2R'].mean()].shape[0]

# Calculate the percentage of posts with C2R greater than average
percent_posts_above_avg_c2r = (posts_above_avg_c2r / df.shape[0]) * 100

avg_reactions = df['Reactions'].mean()
avg_comments = df['Comments'].mean()
avg_reposts = df['Reposts'].mean()
avg_c2r = df['C2R'].mean()

type_mapping = {0: 'images', 1: 'video', 2: 'other (repost, text, link)'}
df['Type'] = [type_mapping.get(post_type) for post_type in post_types]

print(df)

print('Avg Reactions', avg_reactions)
print('Avg Comments', avg_comments)
print('Avg Reposts', avg_reposts)
print('Avg C2R', avg_c2r)
print('Max C2R', max_c2r)
print('Number of posts > avg C2R: ', df[df['C2R'] > df['C2R'].mean()].shape[0])
print('% of posts > avg C2R: ', percent_posts_above_avg_c2r)

avg_reactions_by_type = df.groupby('Type')['Reactions'].mean()
avg_comments_by_type = df.groupby('Type')['Comments'].mean()
avg_c2r_by_type = df.groupby('Type')['C2R'].mean()

print('\nAverage Reactions by Post Type:')
print(avg_reactions_by_type)

print('\nAverage Comments by Post Type:')
print(avg_comments_by_type)

print('\nAverage C2R Ratio by Post Type:')
print(avg_c2r_by_type)

df.to_csv('google-linkedin-statistics.csv', index=False)

print('Peak Memory Usage =', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
print('User Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_utime)
print('System Mode Time =', resource.getrusage(resource.RUSAGE_SELF).ru_stime)

