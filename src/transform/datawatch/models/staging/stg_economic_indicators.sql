{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date'], 'type': 'btree'},
    ]
) }}

with economic_indicators_raw as (
    select 
        date::date as date,
        inflation_rate::numeric(6,2) as inflation_rate,
        gdp_growth_rate::numeric(6,2) as gdp_growth_rate,
        unemployment_rate::numeric(6,2) as unemployment_rate,
        source
    from {{ ref('economic_indicators') }}
    where date is not null
)

select 
    date,
    inflation_rate,
    gdp_growth_rate,
    unemployment_rate,
    source
from economic_indicators_raw
order by date
