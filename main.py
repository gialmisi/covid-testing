import pandas as pd
import numpy as np

government_data_file = (
    "./data/20200416_acaps_-_covid-19_goverment_measures_dataset_v8.xlsx"
)
viral_data_file = "./data/time-series-19-covid-combined_csv.csv"


gov_data = pd.read_excel(government_data_file, sheet_name=1)

# Change me to see plots for a specific country
country = "Sweden"

gov_data_filtered = gov_data.loc[
    gov_data["COUNTRY"] == country, ["COUNTRY", "MEASURE", "DATE_IMPLEMENTED"]
].rename(columns={"DATE_IMPLEMENTED": "DATE"})
gov_data_filtered.DATE = pd.to_datetime(gov_data_filtered.DATE)

viral_data = pd.read_csv(viral_data_file)
viral_data_filtered = viral_data.loc[
    viral_data["Country/Region"] == country,
    ["Country/Region", "Confirmed", "Recovered", "Deaths", "Date"],
].rename(columns={"Country/Region": "COUNTRY", "Date": "DATE"})
viral_data_filtered.DATE = pd.to_datetime(viral_data_filtered.DATE)


merge = pd.merge(
    viral_data_filtered, gov_data_filtered, on=["DATE", "COUNTRY"], how="outer"
)


import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=merge["DATE"], y=merge["Confirmed"], name="Confirmed cases")
)
fig.add_trace(go.Scatter(x=merge["DATE"], y=merge["Deaths"], name="Deaths"))
fig.add_trace(
    go.Scatter(x=merge["DATE"], y=merge["Recovered"], name="Recovered")
)
# fig.add_trace(go.Scatter(x=merge["DATE"], y=merge["MEASURE"]))

for index, row in (
    merge.loc[:, ["DATE", "MEASURE", "Confirmed"]].dropna().iterrows()
):
    fig.add_annotation(
        x=row["DATE"], y=row["Confirmed"], text=str(row["MEASURE"])
    )

fig.update_annotations(
    dict(
        xref="x",
        yref="y",
        showarrow=True,
        arrowhead=7,
        ax=0,
        ay=-200,
        font=dict(family="Courier New, monospace", size=13, color="black"),
        textangle=90,
    )
)

fig.update_layout(
    title=f"Confirmed cases in {country}",
    showlegend=True,
    xaxis_title="Date",
    yaxis_title="Number of",
    font=dict(family="Courier New, monospace", size=22, color="#7f7f7f"),
)

fig.show()
