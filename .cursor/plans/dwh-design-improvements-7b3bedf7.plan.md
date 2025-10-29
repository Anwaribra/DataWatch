<!-- 7b3bedf7-4559-4b06-bea7-6f94fccc0c7f d9dce36b-cdcc-4254-b2d6-88eddb842bf9 -->
# DWH Design Improvements Plan

## Critical Issues to Fix

### 1. Fix Date Redundancy Issue

**Current Problem**: `date_id` is just `date` cast, creating redundancy without benefits.
**Solution**:

- Option A: Remove `date_id` from fact table, keep only `date` and use it as FK to `dim_date.date`
- Option B: Create proper integer surrogate key (YYYYMMDD format: 20240101) in `dim_date`, keep `date_id` in fact
- **Recommendation**: Option B - proper surrogate keys improve join performance and enable date dimension to outlive fact data

**Files to modify**:

- `src/transform/datawatch/models/dim_date.sql`: Change `date_id` to integer (YYYYMMDD format)
- `src/transform/datawatch/models/fact_daily_metrics.sql`: Update join logic and ensure `date_id` is properly set
- `src/transform/datawatch/models/schema.yml`: Update descriptions

### 2. Fix Filtering Logic Bug

**Current Problem**: Line 77 filters out ALL rows when exchange rate is NULL
**Solution**: Remove restrictive WHERE clause, allow NULL exchange rates if other metrics exist

**File to modify**:

- `src/transform/datawatch/models/fact_daily_metrics.sql`: Remove or modify WHERE clause (line 77)

### 3. Add Primary Key and Constraints

**Current Problem**: No primary key on fact table
**Solution**: Add composite primary key on `(date_id)` or unique constraint

**Files to modify**:

- `src/transform/datawatch/models/fact_daily_metrics.sql`: Add unique constraint in config
- `src/transform/datawatch/models/schema.yml`: Update tests

### 4. Add Missing Indexes

**Current Problem**: Only index on `date_id`, missing `date` index for joins
**Solution**: Add index on `date` column for join performance

**File to modify**:

- `src/transform/datawatch/models/fact_daily_metrics.sql`: Add date index to config

### 5. Fix Schema Documentation

**Current Problem**: References removed `egx30` column
**Solution**: Remove egx30 reference from schema.yml

**File to modify**:

- `src/transform/datawatch/models/schema.yml`: Remove egx30 column definition

### 6. Optimize Calculated Columns Strategy

**Current Problem**: All calculated columns in fact table (storage overhead)
**Solution**: Evaluate moving some to mart/analytics layer, or add comments explaining why they're materialized

**Files to review**:

- Keep calculated columns for performance, but add documentation on why
- Consider creating separate mart for frequently used transformations

### 7. Implement Incremental Strategy (Future Enhancement)

**Current Problem**: Full refresh every run
**Solution**: Add incremental strategy for fact table updates
**Priority**: Lower - implement after core fixes

## Implementation Order

1. Fix schema.yml (remove egx30) - Quick win
2. Fix filtering logic bug - Critical for data completeness
3. Add primary key and indexes - Data integrity and performance
4. Fix date redundancy (surrogate key) - Design improvement
5. Add incremental strategy - Optimization for later

## Testing Strategy

After each change:

- Run `dbt run` to ensure models build
- Run `dbt test` to verify constraints
- Verify data completeness (check row counts before/after filtering fix)
- Performance test joins with new indexes