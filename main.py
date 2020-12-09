# %%
import pymongo
import time
import matplotlib.pyplot as plt
import pandas as pd

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['wikimedia_history_it_2020']
pages = db['pages']
revisions = db['revisions']
users = db['users']

# METHODS

# sort from numbers of revert
def get_more_reverts(type):

    if type == 'page':

        pipe = [{"$match": {"revision.is_identity_revert": True}},
                {"$group": {"_id": "$page.title", "total_revert": {"$sum": 1}}},
                {"$sort": {"total_revert": -1}}]

        return list(db.revisions.aggregate(pipe, allowDiskUse=True))

    else:

        pipe = [{"$match": {"revision.is_identity_revert": True}},
                {"$group": {"_id": "$event_user.id",
                            "total_revision": {"$max": '$event_user.revision_count'},
                            "total_revert": {"$sum": 1}}},
                {"$sort": {"total_revert": -1}}]

        return list(db.revisions.aggregate(pipe, allowDiskUse=True))
# update the given dict adding the revert on revision and sorting from it
def get_reverts_on_revisions(user_rev):
    for user in user_rev:
        user['rev_on_rev'] = 0
        if user['_id'] != None:
            user['rev_on_rev'] = user['total_revert']/user['total_revision']

    return sorted(user_rev, key = lambda k: k['rev_on_rev'],  reverse=True)

def get_reverts_for_month():
    pipe = [{"$match": {"revision.is_identity_revert": True}},
            {"$group": {"_id": {'$month': '$event_timestamp'}, "n_revert": {"$sum": 1}}},
            {"$sort": {"_id": 1}}]

    return list(db.revisions.aggregate(pipe, allowDiskUse=True))

def get_reverts_for_year():
    pipe = [{"$match": {"revision.is_identity_revert": True}},
            {"$group": {"_id": {'$year': '$event_timestamp'}, "n_revert": {"$sum": 1}}},
            {"$sort": {"_id": 1}}]

    return list(db.revisions.aggregate(pipe, allowDiskUse=True))



# %%
t1 = time.time()
#metriche generali 
n_users = users.find({'event_type': 'create'}).count()
n_pages_created = pages.find({'event_type' : 'create'}).count() + pages.find({'event_type' : 'create-page'}).count() 
n_pages_deleted = pages.find({'event_type' : 'delete'}).count()
n_pages = n_pages_created - n_pages_deleted

n_revisions = revisions.count()
n_reverts = revisions.find({'revision.is_identity_revert': True}).count()


#metriche revert
pages_more_reverts = get_more_reverts('page')
user_more_reverts = get_more_reverts('user')
user_more_reverts = get_reverts_on_revisions(user_more_reverts)


avg_reverts_on_revisions = n_reverts / n_revisions
reverts_for_month = get_reverts_for_month()

t2 = time.time()
# %%


# plot the number of revert for each month 
df = pd.DataFrame(reverts_for_month)
plt.bar(df['_id'], df['n_revert'])


# %%



# %%
