# Introduction
Very similar to the generation of dataset on 2020-02-18.
In addition we also limit the allowed length.
We take the length as it is seen in E. coli +- 15 aa.

"""
query ppiA: "gene:ppia annotation:(type:signal) taxonomy:gammaproteobacteria length:[175 TO 205]"
"""

"""
query ppiB: "gene:ppib taxonomy:gammaproteobacteria NOT annotation:(type:signal) length:[149 TO 179]"
"""
