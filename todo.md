
# aggiustare il fatto che le json war per utente perdono qualcosa



colonne: 20 char 

3 timestamp
4 comment 

5 user id 
6 user text historical 
7 user text 
8 user blocks hist
9 user blocks
10 user groups hist 
11 user groups
12 user isbot hist
13 user isbot 
17 user_is_anonymous
18 user_registration_timestamp
20 user_first_edit_timestamp
21 user_revision_count
22 user_seconds_since_previous_revision

23 page id
24 page historycal name
... cose della pagina 
28

32 page_creation_timestamp
33 page_first_edit_timestamp
34 page_revision_count

52 revision id
53 revision parent id 
54 revision is_minor_edit
57 revision lenght
58 revision diff lenght 
59 revision sha1
64 revision isrevertata
65 revision reverter id 
66 revision seconds_to_identity_revert
67 revision isrevertatore



1 2 14 15 16 19 29 30 31 35-51 55 56 60 61 62 63 68




simplechain approssimano ma abbastanza affidabili

nop = number of pages

nop created                     8415868
nop > one edit                  8412779 
nop created ns0                 3328862
nop > one edit revisions ns0    3283713
nop with reverts                 157743
nop with reverts ns0             126569


1) sort_dataset : tsv raw dataset -> tsv which contains revert sorted by page (wars)
2) create_json  : wars -> json file which contains info about chains (json)
3) compute_by_month: json -> tsv which contains stats per page by month (monthly/pages/all.tsv) -> tsv stats per user by month (monthly/users/all.tsv)








```

## tsv reverts by month 
simple metrics about reverts and vandalism by month for each page 

```
title       pageid    year_month     nrev      nrev_vandalism
```








## done 
dai json ho estratto i dati e creato un tsv con i dati separati per mese come sopra specificato 
ho poi calcolato diverse metriche come 
### from json

- plot : numero di pagine raggruppate per longest_chain
- plot : numero di catene per ogni mese 
- plot : numero di pagine raggruppate per media (arrotondata all'intero piu vicino)
- file : numero di catene per utente 
- file : numero di revert che (non) sono in una catena 
### from tsv

- plot + file : numero di pagine con almeno una catena per ogni mese 
- file : numero di mesi in cui una pagina ha almeno una catena 


# todo

## in progress 
n revert vandalismo ( guardo se nel commento sta scritto vandal)
n revert per mese per pagina !!togliere carlo
catene senza non registrati

n revert subiti/fatti da un utente registrato/non/admin x pagina
    reg-reg (revert da uno registrato a uno registrato) reg non admin
    admin-reg 
    reg-admin
    admin-admin

n mutual revert per pagina e per mese
    reg-reg
    admin-reg
    admin-admin
## todo davvero



mutual revert guarda di volta in volta 

fare per utente quanti revertha fatto agli altri 

3 revert rule ( max 3 revert in 1 pag in 24 h)

usare parent id per simplechain

le date è meglio salvarle come 01 e non 1 per sort



grafico revert per mese mettere le candele 