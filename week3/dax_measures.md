# DAX Measures and Calculations

## 1. CALCULATE() – Apply Filters on Measures

```DAX
Online Sales =
CALCULATE(
    [Total Sales],
    'Sales Transactions'[Channel] = "Online"
)
```

**Explanation:** `CALCULATE()` changes the filter context. This measure calculates total sales only for Online transactions.

---

## 2. YTD Sales using DATESYTD()

```DAX
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD('Calendar'[Date])
)
```

**Explanation:** `DATESYTD()` returns dates from the beginning of the year through the current date. `CALCULATE()` evaluates total sales over those dates.

**Requirement:** Use a proper Calendar/Date table related to `'Sales Transactions'[Date]`.

---

## 3. Running Total using EARLIER()

`EARLIER()` is designed for row context in calculated columns, not normal measures. Therefore, a running total using `EARLIER()` is written as a calculated column:

```DAX
Running Total Sales =
CALCULATE(
    SUMX(
        FILTER(
            'Sales Transactions',
            'Sales Transactions'[Date] <= EARLIER('Sales Transactions'[Date])
        ),
        'Sales Transactions'[Units] * 'Sales Transactions'[Unit_Price]
    )
)
```

**Explanation:** For each row, `EARLIER()` returns the current row's date. `FILTER()` selects transactions up to that date, and `CALCULATE()` sums their sales.

**Note:** In modern Power BI, a running-total measure is generally preferred over an `EARLIER()` calculated column.

---

## 4. Calculated Column – Profit Margin %

Assuming `Product_ID` relates Sales Transactions to Product Catalogue:

```DAX
Profit Margin % =
VAR SalesAmount =
    'Sales Transactions'[Units] *
    'Sales Transactions'[Unit_Price]
VAR CostAmount =
    'Sales Transactions'[Units] *
    RELATED('Product Catalogue'[COGS])
RETURN
    DIVIDE(
        SalesAmount - CostAmount,
        SalesAmount,
        0
    )
```

**Explanation:** Profit margin is calculated as `(Sales - Cost) / Sales`. `RELATED()` retrieves the product COGS from the related Product Catalogue table.

---

## 5. Context Transition – Row Context to Filter Context

```DAX
Sales from Current Product =
CALCULATE(
    [Total Sales]
)
```

**Explanation:** When `CALCULATE()` is evaluated inside a row context, it converts the current row context into filter context. This allows `[Total Sales]` to be evaluated for the current row or product.

**In simple terms:**

`Row Context → CALCULATE() → Filter Context`

---

## Supporting Base Measure

The measures above use this base measure:

```DAX
Total Sales =
SUMX(
    'Sales Transactions',
    'Sales Transactions'[Units] *
    'Sales Transactions'[Unit_Price]
)
```

## Summary

| DAX Concept | Purpose |
|---|---|
| `CALCULATE()` | Changes filter context |
| `DATESYTD()` | Calculates year-to-date sales |
| `EARLIER()` | Accesses an earlier row context in calculated columns |
| Calculated Column | Calculates values row by row |
| Context Transition | Converts row context into filter context using `CALCULATE()` |
