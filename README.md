# wikimedia-revert
On wikipedia everyone can edit a page.

The [hystory](https://en.wikipedia.org/w/index.php?title=Volcanic_rock&action=history). of a page contains a snapshot of it for each edit 


On wikipedia everyone can delete an edit restoring the previous edit, this is a **revert**.

# Dataset structure 

it's a tsv, each line is an event, there are different type of events: 
- **revision**: edit 
- **page**: create, move, restore, etc of a page  
- **user**: create, delete, change group (become an admin) 

this is the official information page.

https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history_dumps

this is my information page about fields i use. 

https://docs.google.com/spreadsheets/d/1oyo59K_FfGTl7C5Q96NjvnWeAbWv1ILVSdvSrF1Pz8E/edit#gid=297287992


# created 
from the wikimedia dataset i computed different other datasets


```sorted_by_pages.tsv``` : same as wikimedia but only with revision events and sorted by page name

## chains 
a chain happens when the targetted edit of a revert is a revert(which could belong to a chain)

for each page is saved each chain and some statistics about it 

```wars_json/pages```
```
{
    "title": "Loligo_vulgaris", 
    "chains": 
    [{
        "revisions": ["113715375", "113715381", "113715393"], 
        "users": {"62.18.117.244": "", "Leo0428": "17181"}, 
        "len": 3, 
        "start": "2020-06-15 22:16:23.0", 
        "end": "2020-06-15 22:17:38.0"
    }], 
    "n_chains": 1, 
    "n_reverts_in_chains": 3, 
    "n_reverts": 38
    "mean": 3.0, 
    "longest": 3, 
    "G": 0,
    "M": 0, 
    "lunghezze": {"3": 1}
}
```
similarly, it's possibile to see every chain a user got involved 
```wars_json/users```
```
{
    "title": "Loligo_vulgaris", 
    "chains": 
    [{
        "revisions": ["113715375", "113715381", "113715393"], 
        "users": {"62.18.117.244": "", "Leo0428": "17181"}, 
        "len": 3, 
        "start": "2020-06-15 22:16:23.0", 
        "end": "2020-06-15 22:17:38.0"
    }], 
    "n_chains": 1, 
    "n_reverts_in_chains": 3, 
    "n_reverts": 38
    "mean": 3.0, 
    "longest": 3, 
    "G": 0,
    "M": 0, 
    "lunghezze": {"3": 1}
}
```
from this json i computed the metric by month adding more_than and involved
```monthly pages```
```
title    year_month    nchain   nrev    mean    longest     more_than5      more_than7      more_than9      G   involved
```

```monthly users```
``` 
user    year_month    nchain   nrev    mean    longest     more_than5      more_than7      more_than9      G    involved
```


## admin

### pages

```reverts```
```
page_id     page_name    adm_adm    adm_reg     reg_adm     reg_reg     not_reg     reg
```

```mutual```

```
page_id     page_name    adm_adm    adm_reg     reg_reg     not_reg     reg
```

### user
```
user     group    year_month    tot_received     t_reg     t_not     t_adm     tot_done     d_reg     d_not     d_adm    
```













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

## json chains pages

## json chains users
same as json chains users but the title is the username and without M

## tsv chains by month

### structure 

### info
I use the start date of a chain for classification 

G is a metric that's similar to M which evalue the chains in a page, when in a chain are involved users with a big edit count G will be bigger


## tsv reverts admin
**adm_adm** refert to the number of reverts an admin made to another admin 
**reg** refer to the number of revert made by registered user (admin included)

```
page_id     page_name    adm_adm    adm_reg     reg_adm     reg_reg     not_reg     reg
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
