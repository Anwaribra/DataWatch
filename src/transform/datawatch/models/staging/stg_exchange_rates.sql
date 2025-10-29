{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date'], 'type': 'btree'},
    ]
) }}

with exchange_rates_raw as (
    select 
        date::date as date,
        usd_egp_rate::numeric(10,4) as usd_egp_rate
    from {{ ref('exchange_rates') }}
    where date is not null
        and usd_egp_rate is not null
        and usd_egp_rate > 0
)

select 
    date,
    usd_egp_rate,
    'exchange_rate' as metric_type
from exchange_rates_raw
order by date
