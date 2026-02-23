# Oeil du Cyclone

*__Type__*: Cryptography

*Contexte* : 

Le cyclone Belal de catégorie 5 frappe l'île de la Réunion avec des vents de 280 km/h. Le code d'activation du système d'évacuation d'urgence a été fragmenté en 9 parts distribuées aux stations météo de l'île.

*Situation :*

  - 5 stations des hauts ont survécu → données complètes
  - 4 stations côtières submergées → 20 bits les plus bas perdus par fragment

*Objectif* : Reconstruire le code d'évacuation avant la prochaine vague.

*Paramètres :*

  - Premier : `p = 2^521 - 1` (Premier de Mersenne M521)
  - Seuil : 6 fragments sur 9 nécessaires
  - Bits perdus par station inondée : 20 bits
  - Format du flag : CCOI26{...}
  - Validation : `SHA256(flag)[:16] = f687cb74fdcefefc`
  - 
## Analyse

Type d'attaque : Shamir's Secret Sharing avec données partielles

Ce challenge implémente le partage de secret de Shamir :

  - Un secret est encodé comme le coefficient constant d'un polynôme de degré `k-1`
  - Le polynôme est évalué en n points pour créer n parts
  - Il faut minimum k parts pour reconstruire le polynôme (et donc le secret)

Notre cas :

  - Polynôme de degré 5 (car seuil = 6)
  - 9 parts au total : `(x, y)` où `x ∈ {1, 2, ..., 9}`
  - Secret = `P(0)` où P est le polynôme

***Le problème***

Nous avons :

  - 5 parts complètes : `(x, y) pour x ∈ {1, 2, 3, 4, 5}`
  - 4 parts partielles : `(x, y_partial) pour x ∈ {6, 7, 8, 9}`

Avec seulement 5 parts complètes, on ne peut reconstruire qu'un polynôme de degré 4, pas le vrai polynôme de degré 5.

***Solution*** : On doit récupérer AU MOINS 1 des 4 parts partielles en retrouvant ses 20 bits manquants.
