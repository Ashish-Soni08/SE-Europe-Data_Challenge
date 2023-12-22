# Schneider Electric European Datascience Hackathon 2023
![SE Logo](https://github.com/Ashish-Soni08/SE-Europe-Data_Challenge/blob/main/images/schneider_electric_logo.png)

*Organised by: NUWE* <br>
![Nuwe Logo](https://github.com/Ashish-Soni08/SE-Europe-Data_Challenge/blob/main/images/nuwe_logo.png)


*EcoForecast: Revolutionizing Green Energy Surplus Prediction in Europe*

**Date:** 18th November to 21st November, 2023

**Team Member:** *Ashish Soni and Ishiita Pal* 

**Tech Stack:** *Python*

# Instructions
Install dependencies by running:
<button class="btn" data-clipboard-target="#requirements-code"></button>
<pre><code id="requirements-code">pip install -r requirements.txt</code></pre>
<button class="btn" data-clipboard-target="#requirements-code"></button>
<pre><code id="requirements-code">run_pipeline.sh</code></pre> 


## **Problem Statement:** 
With increasing digitalization and the ever-growing reliance on data servers, the significance of sustainable computing is on the rise. Schneider Electric, a pioneer in digital transformation and energy management, brought this innovative challenge to play our part in reducing the carbon footprint of the computing industry. We aim to predict which European country will have the highest surplus of green energy in the next hour. This information will be critical in making important decisions, such as optimizing computing tasks to use green energy effectively and, consequently, reducing CO2 emissions.

## **Objective:** 
Create a model capable of predicting the country (from a list of nine) that will have the most surplus of green energy in the next hour. For this task, we consider both the energy generation from renewable sources (wind, solar, geothermic, etc.), and the load (energy consumption). The surplus of green energy is considered to be the difference between the generated green energy and the consumed energy.

The countries to focus on are: Spain, UK, Germany, Denmark, Sweden, Hungary, Italy, Poland, and the Netherlands.
Their country codes: SE, UK, DE, DK, SE, HU, IT, PO, NE

## **Data Collection**

The `data_ingestion.py` script collects raw time-series data of various time granularities from the ENTSO-E Transparency portal using it [API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html). The collected data comprises both energy generation from renewable sources and electricity consumption (load) for specified European countries. The chosen time period for the analysis is from *01-01-2022 to 01-01-2023*.

### Load Data Collection
The script fetches electricity consumption (load) data for each country, providing insights into the energy consumption patterns. This data is crucial for understanding the overall demand for energy in each region.

Load Data contains the following columns for each `country` - `StartTime`, `EndTime`, `AreaID`, `UnitName`, `Load`

### Green Energy Generation Data Collection
In addition to load data, the script retrieves energy generation data, filtering out non-green energy sources. The filtering process involves selecting specific PsrTypes, representing various green energy types. This ensures that the collected data focuses exclusively on renewable and environmentally friendly energy sources. 

Generation Data contains the following columns for each `country` and `PsrType` - `StartTime`, `EndTime`, `AreaID`, `UnitName`, `PsrType`, `quantity`

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

## **Data Processing:**
There are `3` data processing scripts that include different steps of data wrangling to get the data into the final desired format as required for the challenge.
1. `data_processing_1.py` - convert datatypes to appropraite format, keep required columns, fill missing values, interpolate values and save as new csv files. The `PsrType` are provided for each of the mentioned countries and are aggregated at different intervals (15 min, 30 min, or 1h), depending on the country. All the data was homogenized to 1-hour intervals for consistency.
2. `data_processing_2.py` - processes and aggregates energy generation and load data for multiple European countries, merging them into consolidated country-specific files
3. `final_data_processing.py` - automates the merging of energy data for multiple European countries into a single DataFrame.  It handles the merging process by consolidating country-specific files from an intermediate directory into a final processed.csv file.
The processed.csv has the following columns:
`green_energy_SP`, `green_energy_UK`, `green_energy_DE`, `green_energy_DK`, `green_energy_HU`, `green_energy_SE`, `green_energy_IT`, `green_energy_PO`, `green_energy_NL`, `SP_Load`, `UK_Load`, `DE_Load`, `DK_Load`, `HU_Load`, `SE_Load`, `IT_Load`, `PO_Load`.

## **Model Training and Testing**

We inferred and made the the following decisions on the basis of our prelimianary analysis from the information provided to us.
1. It is a Multi-variate time series with Multiclass Classification Task.
2. The Recommended Training and Testing Split: 80:20. Since this is time-series data, we performed a chronological split (not random).
3. There are `7008` data points for training the model and `1752` data points for testing the model.
4. We trained Random Forest Classifier as a baseline because it is intuitive to understand and its explainability. 

**Instruction**: `You will also need to add an additional column that will be your label: the ID of the country with the bigger surplus of green energy for the next hour.` 

**Results Discussion:** By adding the `label` column based on the highest surplus for an hour, we had only few countries represented in the `label` column. This will impact the model's ability to predict other class labels, and also the resulting model had a low f1_score(macro): `0.55`. Since it was our first time wrangling time series data for a classification task, there were challenges to get the data into the right format for predictive modelling techniques. Therefore, we also did not train any models further.  

**Conclusion:** The data format required for the task has to be investigated in more depth and then we can do better with our predictive modeling approach. But due to a shorter period of time we were unable to bring this project to a successful conclusion.

## Hackathon Results
We achieved the `3rd` Rank in the Hackathon.
<br> [GreenProphets - EcoForecast: Revolutionizing Green Energy Surplus Prediction in Europe - Report](https://github.com/Ashish-Soni08/SE-Europe-Data_Challenge/blob/main/GreenProphets%20-%20EcoForecast_%20Revolutionizing%20Green%20Energy%20Surplus%20Prediction%20in%20Europe%20-%20Report.pdf)


