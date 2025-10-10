**Data preparation for Resale datasets**

1. Recorded differences in counts between *TOUCHABLE Resale Transaction Info* (Old cleaned dataset) and *Resale Transaction Info updated Sept 2025* (New dataset), to check for new data to be added to the cleaned dataset.  
   1. Within *TOUCHABLE Resale Transaction Info,* final\_round2 sheet was used, since it appeared to be the latest cleaned version of the Resale Transaction Info dataset by the previous team.  
2. Parsed and concatenated address fields into structured columns (Town, Development, Address, Unit Number) for *Resale Transaction Info updated Sept 2025*. Ref: CHAPA\_ParseData.ipynb.  
3. Checked for discrepancies between New and Old dataset, and saved a csv of the new Sept 2025 entries that weren't present in Old dataset. Ref: DisparityCheckforProperties\_resale\&applicant.ipynb.  
4. Merged these new entries to the Old cleaned dataset. Ref: Merging Final Round with updated Sept2025 Resale.ipynb.  
   