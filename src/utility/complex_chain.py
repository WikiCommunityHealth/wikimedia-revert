# non funziona la metto qui per non buttarla via magari torna utile

def complex_chains():

    #dump_in = bz2.open(dataset, 'r')
    dump_in = open(dataset, 'r')  # for uncompressed
    dump_out = open('wars.json', 'w')
    line = dump_in.readline()

    dump_out.write('[')

    inizio = datetime.now()

    open_chains = []
    complete_chains = []
    users = []
    page = ''
    page_chains = {}

    war = {
        "page": 'titolo',
        "chains": []

    }

    catena = {
        "users": ['pippo', 'pluto'],
        "revisions": []
    }

    while line != '':

        #line = dump_in.readline().rstrip().decode('utf-8')[:-1]
        line = dump_in.readline().rstrip()[:-1]  # for uncompressed
        values = line.split('\t')

        if line == '' or len(values) < 69 or values[28] != '0':
            continue

        page_name = values[25]
        rev_id = values[52]
        reverter = values[65]
        is_reverted = values[64]
        utente = values[7]

        utenti = []

        added = False
        exist = False

        # check if this revision is part of a chain
        if page_name == page:
            for chain in open_chains:  # check if this rev is part of an existing  chain

                # if the one you want to insert already exists don't add it
                for i in range(len(chain)):
                    if chain[i] == reverter:
                        exist = True

                # if the last element of the chain match with the current revision id
                if chain[-1] == rev_id:
                    added = True
                    if is_reverted == 'true' and not exist:                           # continue the chain
                        chain.append(reverter)
                        utenti.append(utente)

                    else:                                               # end of the chain this revision is not reverted
                        if len(chain) > 2:
                            catena['revisions'] = chain
                            catena['users'] = utenti
                            war['chains'].append(catena)
                            complete_chains.append(chain)
                        open_chains.remove(chain)

            if not added and not exist:

                open_chains.append([rev_id, reverter])

        else:
            if(len(complete_chains) > 0):
                page_chains[page] = complete_chains
                war['page'] = page

                dump_out.write(json.dumps(war))
                dump_out.write(',\n')
            page = page_name
            complete_chains = []
            open_chains = []

    dump_out.write(']')
    return page_chains
