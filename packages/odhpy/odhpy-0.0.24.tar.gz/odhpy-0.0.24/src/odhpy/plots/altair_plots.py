import pandas as pd
import altair as alt
import numpy as np
from typing import Union

def wy_event_heatmap(df=Union[pd.DataFrame,pd.Series],criteria=1,y_title="Series",pass_label="Pass",fail_label="Fail",pass_colour="white",fail_colour="red",width=None,height=None,stroke='black',strokeWidth=0.3):
    """Returns an Altair heatmap chart from a timeseries input of event count by Water Year.

    Args:
        df (DataFrame | Series): Annual (WY) index timeseries of no. of 'events' in a year i.e. output of StorageLevelAssessment.AnnualDaysBelowSummary()
        criteria (int, optional): Minimum integer in df that triggers a 'failure'. Defaults to 1.
        y_title (str, optional): Y axis title. Defaults to "Series".
        pass_label (str, optional): Label for years that don't meet the criteria. Defaults to "Pass".
        fail_label (str, optional): Label for years that meet the criteria. Defaults to "Fail".
        pass_colour (str, optional): Colour for years that don't meet the criteria. Defaults to "white".
        fail_colour (str, optional): Colour for years that meet the criteria. Defaults to "red".
        width (int, optional): Width of chart output. Defaults to None.
        height (int, optional): Height of chart output. Defaults to None.
        stroke (str, optional): Colour of rectangle outline. Defaults to black.
        strokeWidth (float, optional): Width of rectangle outline. Defaults to 0.3.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    # If df input is a Series, first convert to DataFrame
    if type(df) is pd.Series:
        df=pd.DataFrame(df)

    # df column names must be str for Altair
    df.columns=[str(x) for x in df.columns]
    columns=df.columns.values


    # Lookup table to convert count of events by WY to 'pass' or 'fail
    lookup = pd.DataFrame({
    'key': ['1', '0'],
    'y': [fail_label,pass_label]
    })

    domain = [pass_label, fail_label]
    range = [pass_colour, fail_colour]

    # Altair needs vega expression. Generate based on criteria input
    vega_expr_str = 'if(datum.value>=' + str(criteria) + ',1,0)'

    # Default width and height expression
    if width == None:
        width = df.shape[0]*10
    if height == None:
        height = len(columns)*25
    
    chart_wy_event = alt.Chart(df.reset_index() # Reset index so that Altair can access Date index
    ).transform_fold( # Fold individual columns into single column
        columns,
        as_=['column','value']
    ).transform_calculate( # Convert count of WY events to 1 or 0 based on criteria
        value=vega_expr_str
    ).transform_lookup( # Convert 1 and 0 to pass and fail
        lookup='value',
        from_=alt.LookupData(lookup, key='key', fields=['y'])
    ).mark_rect(stroke=stroke, strokeWidth=strokeWidth
    ).encode(
        alt.X('index:O', title='Water Year'),
        alt.Y('column:N',sort=None, title=y_title),
        color=alt.Color('y:N', scale=alt.Scale(domain=domain,range=range), title="Key")
    ).properties(
        width=width,
        height=height
    )

    return chart_wy_event