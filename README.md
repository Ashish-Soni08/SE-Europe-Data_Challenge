# Schneider Electric European Datascience Hackathon 2023

![NUWE]]("images/schneider_electric_logo.png")

Organied by: NUWE
![NUWE]]("images/nuwe_logo.png")

*EcoForecast: Revolutionizing Green Energy Surplus Prediction in Europe*

**Date:** 18th November to 20th November, 2023

## **Problem Statement:** 
With increasing digitalisation and the ever-growing reliance on data servers, the significance of sustainable computing is on the rise. Schneider Electric, a pioneer in digital transformation and energy management, brought this innovative challenge to play our part in reducing the carbon footprint of the computing industry. We aim to predict which European country will have the highest surplus of green energy in the next hour. This information will be critical in making important decisions, such as optimizing computing tasks to use green energy effectively and, consequently, reducing CO2 emissions.

## **Objective:** 
Create a model capable of predicting the country (from a list of nine) that will have the most surplus of green energy in the next hour. For this task, we consider both the energy generation from renewable sources (wind, solar, geothermic, etc.), and the load (energy consumption). The surplus of green energy is considered to be the difference between the generated green energy and the consumed energy.

The countries to focus on are: Spain, UK, Germany, Denmark, Sweden, Hungary, Italy, Poland, and the Netherlands.
Their country codes: SE, UK, DE, DK, SE, HU, IT, PO, NE


## 1. **Raw Data Collection**

The `data_ingestion.py` script collects raw time-series data of various time granularities from the ENTSO-E Transparency portal using it API: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html. The collected data comprises both energy generation from renewable sources and electricity consumption (load) for specified European countries.

### Load Data Collection
The script fetches electricity load data for each country, providing insights into the energy consumption patterns. This data is crucial for understanding the overall demand for energy in each region.

### Green Energy Generation Data Collection
In addition to load data, the script retrieves energy generation data, filtering out non-green energy sources. The filtering process involves selecting specific PsrTypes, representing various green energy types. This ensures that the collected data focuses exclusively on renewable and environmentally friendly energy sources. 

The PsrTypes include: 
- Biomass (B01)
- Geothermal (B09)
- Hydro Pumped Storage (B10)
- Hydro Run-of-river and poundage (B11)
- Hydro Water Reservoir (B12)
- Marine (B13)
- Other renewable (B15)
- Solar (B16)
- Wind Offshore (B18)
- Wind Onshore (B19)


## 2. **Data Processing:** 
The data collected had to be processed so that the columns look like the provided `test.csv`:
,green_energy_SP,green_energy_UK,green_energy_DE,green_energy_DK,green_energy_HU,green_energy_SE,green_energy_IT,green_energy_PO,green_energy_NL,SP_Load,UK_Load,DE_Load,DK_Load,HU_Load,SE_Load,IT_Load,PO_Load.
