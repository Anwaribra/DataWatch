{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date'], 'type': 'btree'},
    ]
) }}

with stock_indices_raw as (
    select 
        date::date as date,
        sp500::numeric(10,2) as sp500
    from {{ ref('stock_indices') }}
    where date is not null
)

select 
    date,
    sp500
from stock_indices_raw
order by date
