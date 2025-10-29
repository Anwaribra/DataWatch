{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date_id'], 'type': 'btree'},
        {'columns': ['date'], 'type': 'btree'},
    ],
    unique_key=['date_id']
) }}

with date_range as (
    select generate_series(
        '2014-01-01'::date,
        (current_date + interval '2 years')::date,  
        '1 day'::interval
    )::date as date
)

select 
    date,
    -- Generate integer surrogate key in YYYYMMDD format (e.g., 20240101)
    -- This provides better join performance and allows date dimension to outlive fact data
    to_char(date, 'YYYYMMDD')::integer as date_id,
    extract(year from date) as year,
    extract(quarter from date) as quarter,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(dow from date) as day_of_week, -- 0=Sunday, 6=Saturday
    case when extract(dow from date) in (0, 6) then true else false end as is_weekend,
    extract(week from date) as week,
    to_char(date, 'Month') as month_name,
    to_char(date, 'Day') as day_name
from date_range
