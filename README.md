# wikimedia-revert

pip install -r requirements.txt

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

## json 
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

## monthly wars

### structure 
```
title    year_month    nchain    nrev    mean    longest     more_than5      more_than7      more_than9      G
```
### info
I use the start date of a chain for classification 

G is a metric that's similar to M which evalue the chains in a page, when in a chain are involved users with a big edit count G will be bigger

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

catene senza non registrati
n revert vadalismo 
n revert per mese per pagina 
n revert subiti/fatti da un utente registrato/non/admin x pagina
    reg-reg (revert da uno registrato a uno registrato) reg non admin
    admin-reg 
    reg-admin
    admin-admin

n mutual revert per pagina e per mese
    reg-reg
    admin-reg
    admin-admin