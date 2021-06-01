#%%
import re
#reverted_m:dict containing every user a user reverted 
#editcount:dict
#todo: remove the biggest 
def get_M(reverted_m:dict, edit_count:dict, n_involved:int):

    mutual = get_mutual(reverted_m, edit_count)
    values = [0]

    for couple in mutual:
        values.append(min(edit_count[couple[0]], edit_count[couple[1]]))

    values.remove(max(values))
    m =  n_involved * sum(values)
    return m

def get_mutual(reverted_m:dict, edit_count:dict):
    mutual = set()
    biggest_couple = 0

    for user, reverted in reverted_m.items():           #for each user check if the users it reverts reverts him 
        for rev in reverted:
            if rev in reverted_m.keys():
                if user in reverted_m[rev]:
                    if not is_bot(user) or not is_bot(rev):
                        if user > rev:              
                            mutual.add((user,rev))
                        elif user < rev:
                            mutual.add((rev,user))
    return mutual

def getG(chains):

    tot = 0
    utenti = set()
    for chain in chains:
        a = 9999999999
        for user in chain['users']:
            utenti.add(user)
            if chain['users'][user] != '':
                a =  min(a, int(chain['users'][user])) # for every chain in a page i take the users involved and i extract the minimun revision count
            else:
                a = min(a, 0)
        tot += a

    return ((tot * len(utenti)), str(utenti)) 


def is_bot(user):
    words = re.compile('bot', re.IGNORECASE)
    return bool(words.search(user))


def is_vandalism(comment):
    words = re.compile('vandal')
    if words.search(comment) :
        return True
    else:
        return False

def is_admin(groups):
    words = re.compile('sysop')
    return bool(words.search(groups))


def to_bool(value):
    if value == 'true':
        return True
    else:
        return False 

def combine_editors(revertors, editor):
    reverted_m = {}
  
    for user, reverters in revertors.items():
        for reverter in reverters:
            if reverter in editor and user != editor[reverter]:
                reverted_m.setdefault(user, []).append(editor[reverter])

    return reverted_m
# %%

# %%
