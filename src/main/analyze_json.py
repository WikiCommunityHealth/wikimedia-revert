
#%%
dataset_folder = '/home/gandelli/dev/data/wars/'
i = 10

pagine = 0
 

for i in range (0,10):
    dump_in = open(f"{dataset_folder}wars_{i}.json")
    line = dump_in.readline()
    while(line != ''):
        line = dump_in.readline()
        pagine +=1
# %%
