# Goal
I want to find the ideal query terms to split the proteins of a specific organism into two groups:

1. Proteins that stay in the cytoplasm.
2. Proteins that get exported, preferably to the periplasm
3. Somehow avoid other cellular locations (like transmembrane proteins)

If necessary (but rather not),
use additional software to predict location.

## Filter out periplasmic proteins
1. signal peptide
2. gene ontology annotation (goa): periplasmic space 

## Filter out cytoplasmic proteins
1. NO signal peptide 
2. goa:cytoplasm or goa:cytosol

```
(goa:(cytoplasm) OR goa:(cytosol)) NOT annotation:(type:signal) AND organism:"yourOrganism"
```

## Confirmation for likely twin
1. sequence identity above (30 percent)
2. Same EC number (same function)

```
annotation:(type:signal) goa:("periplasmic space") AND organism:"yourOrganism"
```
