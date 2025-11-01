# Data Quality Checks with Soda Core

This directory contains data quality checks for the EIS Data Warehouse using Soda Core.

## Files

The quality checks are organized into separate files for better maintainability:

- `configuration.yml` - Database connection configuration 
- `checks_dim_date.yml` - Dimension table checks (dim_date)
- `checks_fact_daily_metrics.yml` - Fact table checks (fact_daily_metrics)
- `checks_staging.yml` - All staging table checks (stg_exchange_rates, stg_metals_prices, stg_economic_indicators, stg_stock_indices)
- `checks_cross_table.yml` - Cross-table integrity checks



### 3. Run Data Quality Checks

```bash 
# layers checks
soda scan -d eis_db quality/configuration.yml quality/checks_dim_date.yml
soda scan -d eis_db quality/configuration.yml quality/checks_fact_daily_metrics.yml
soda scan -d eis_db quality/configuration.yml quality/checks_staging.yml
soda scan -d eis_db quality/configuration.yml quality/checks_cross_table.yml
```

## Check Categories

### Dimension Table Checks (dim_date)
- Primary key integrity (date_id uniqueness)
- Data type validation
- Temporal attribute validation (year, month, day ranges)
- Completeness checks

### Fact Table Checks (fact_daily_metrics)
- Foreign key integrity (date_id reference to dim_date)
- Price data validity (gold, silver prices)
- Exchange rate validation
- Calculated column consistency (EGP prices, per-gram conversions)
- Economic indicator ranges
- Stock index validation
- Data completeness thresholds
- Cross-table integrity checks

### Staging Table Checks
- **stg_exchange_rates**: Exchange rate validity, data freshness
- **stg_metals_prices**: Price ranges, completeness
- **stg_economic_indicators**: Economic indicator ranges, year-end date validation
- **stg_stock_indices**: Index value ranges, data freshness

### Cross-Table Integrity
- Date alignment between fact and dimension tables
- Data consistency between staging and fact tables

## Check Types

1. **Row Count Checks**: Verify tables have data
2. **Missing Data Checks**: Ensure critical fields are not null
3. **Uniqueness Checks**: Verify primary keys and unique constraints
4. **Range Checks**: Validate data falls within expected ranges
5. **Validity Checks**: Ensure data types and formats are correct
6. **Referential Integrity**: Verify foreign key relationships
7. **Calculated Column Checks**: Validate derived metrics match their formulas
8. **Data Freshness**: Ensure recent data exists
9. **Cross-Table Consistency**: Verify data consistency across related tables



## Troubleshooting

### Connection Issues
- Verify database credentials in environment variables
- Check network connectivity to database
- Ensure database user has SELECT permissions on all tables

### Check Failures
- Review failed_rows queries to identify problematic data
- Adjust ranges/thresholds if legitimate data falls outside expected bounds
- Check data freshness if most_recent_date checks fail

