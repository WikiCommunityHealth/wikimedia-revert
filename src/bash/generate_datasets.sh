#!/bin/bash
LANG=$1
TAB='  '

if [ -z "$LANG" ]
then
echo usage ./generate_datasets.sh _language_
exit
fi


mkdir -p /home/gandelli/dev/data/"$LANG"/admin/page
mkdir -p /home/gandelli/dev/data/"$LANG"/admin/user
mkdir -p /home/gandelli/dev/data/"$LANG"/chains/page
mkdir -p /home/gandelli/dev/data/"$LANG"/chains/user
mkdir -p /home/gandelli/dev/data/"$LANG"/chains/month
mkdir -p /home/gandelli/dev/data/"$LANG"/chains/page_reg/



START="$(date -u +%M)"
echo inizio 
python3 /home/gandelli/dev/wikimedia-revert/src/main/create/sort_dataset.py "$LANG"
now="$(date -u +%M)"
echo "$TAB" sorted and filtered "$(($now-$START))" min
echo
echo CHAINS 

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_chains_page_json.py "$LANG"
now="$(date -u +%M)"
echo  "$TAB"finish page "$(($now-$START))" min

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_chains_user_json.py "$LANG"
now="$(date -u +%M)"
echo "$TAB"finish user "$(($now-$START))" min

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_chains_both_month_tsv.py "$LANG"
now="$(date -u +%M)"
echo finish monthly "$(($now-$START))" min


echo 
echo GROUP
python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_admin_page_mutual_month.py "$LANG"
now="$(date -u +%M)"
echo finish page mutual "$(($now-$START))" min

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_admin_page_revert_month.py "$LANG"
now="$(date -u +%M)"
echo finish page revert "$(($now-$START))" min

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_admin_user_mutual_month.py "$LANG"
now="$(date -u +%M)"
echo finish user mutual "$(($now-$START))" min

python3 /home/gandelli/dev/wikimedia-revert/src/main/create/c_admin_user_revert_month.py "$LANG"
now="$(date -u +%M)"
echo finish user revert "$(($now-$START))" min


echo
echo DATABASE
python3 merge_dataset.py "$LANG"
now="$(date -u +%M)"
echo merged"$(($now-$START))" min

python3 save.py "$LANG"
now="$(date -u +%M)"
echo saved on the database "$(($now-$START))" min