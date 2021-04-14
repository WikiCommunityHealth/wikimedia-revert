import re

def get_M(reverted_m, edit_count, page):

    mutual = set()
    biggest_couple = 0

    for user, reverted in reverted_m.items():
        for rev in reverted:
            if rev in reverted_m.keys():
                if user in reverted_m[rev]:
                    if not is_bot(user) or not is_bot(rev):
                        if user > rev:              
                            mutual.add((user,rev))
                        elif user < rev:
                            mutual.add((rev,user))
    m = 0
    for couple in mutual:
        partial = edit_count[couple[0]] * edit_count[couple[1]]
        m += partial

    m *= len(mutual)

    return m

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