# %%
import pymongo
import time

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

# %%

user_more_reverts = get_more_reverts('user')
pages_more_reverts = get_more_reverts('page')
user_more_reverts = get_reverts_on_revisions(user_more_reverts)



# %%
