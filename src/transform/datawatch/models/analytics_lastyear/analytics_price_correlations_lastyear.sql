{{ config(
    materialized='view',
    schema='analytics_lastyear',
    description='Price correlation matrix for last year data - relationships between metals and exchange rates',
    tags=['analytics_lastyear', 'analytics']
) }}

with fact_data as (
    select 
        date,
        gold_price_usd,
        silver_price_usd,
        usd_egp_rate,
        gold_price_egp,
        silver_price_egp
    from {{ ref('fact_daily_metrics_lastyear') }}
    where gold_price_usd is not null
        and silver_price_usd is not null
        and usd_egp_rate is not null
)

select
    'Gold USD vs Silver USD' as metric_pair,
    corr(gold_price_usd, silver_price_usd) as correlation
from fact_data

union all

select
    'Gold USD vs USD/EGP' as metric_pair,
    corr(gold_price_usd, usd_egp_rate) as correlation
from fact_data

union all

select
    'Silver USD vs USD/EGP' as metric_pair,
    corr(silver_price_usd, usd_egp_rate) as correlation
from fact_data

union all

select
    'Gold EGP vs Silver EGP' as metric_pair,
    corr(gold_price_egp, silver_price_egp) as correlation
from fact_data

