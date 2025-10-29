{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date'], 'type': 'btree'},
    ]
) }}

with metals_raw as (
    select 
        date::timestamp::date as date,
        gold_price_usd::numeric(10,2) as gold_price_usd,
        silver_price_usd::numeric(10,2) as silver_price_usd,
        source
    from {{ ref('metals_prices') }}
    where date is not null
        and (gold_price_usd is not null or silver_price_usd is not null)
        and (gold_price_usd > 0 or silver_price_usd > 0)
)

select 
    date,
    gold_price_usd,
    silver_price_usd,
    source
from metals_raw
order by date
