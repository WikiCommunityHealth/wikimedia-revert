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
3) compute_by_month: json -> tsv which contains stats per page by month (monthly_wars)

# json 

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
    "n_reverts": 3, 
    "mean": 3.0, 
    "longest": 3, 
    "M": 0, 
    "lunghezze": {"3": 1}
}

# monthly wars

## structure 
title    year_month    nchain    nrev    mean    longest     

# info
I use the start date of a chain for classification 