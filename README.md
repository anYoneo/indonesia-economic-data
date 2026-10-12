# Indonesia Economic Data (open dataset)

Clean, ready-to-use economic time series for **Indonesia** — no API key, no signup, no
scraping. Plain CSV. Updated automatically.

Maintained by [anYoneo](https://github.com/anYoneo). If Indonesia is not the only country you
need — or you need the full revision history — see [Paid tiers](#paid-tiers) at the bottom.

## What is in here

`data/indonesia_annual.csv` — 13 annual indicators, full history
(e.g. GDP, GDP per capita, inflation, population, unemployment, life expectancy, FDI,
internet users, agriculture value added, fertilizer consumption, food production index,
official exchange rate, CPI index).

`data/usd_idr_daily.csv` — daily USD/IDR reference rate, last 5 years.

Neither file needs pandas to read; they are plain CSV with a header row.

## Columns

| column | meaning |
|---|---|
| `series_id` | stable identifier, e.g. `wb:idn:NY.GDP.MKTP.CD` |
| `nama` | human-readable name |
| `satuan` | unit of measure |
| `periode` | period the value refers to (`2023` for annual, `2026-10-09` for daily) |
| `nilai` | the value (empty = the source published no figure for that period) |
| `sumber` | upstream source |
| `lisensi` | license of that source |

## Source and license

World Bank Open Data (**CC BY 4.0**) and ECB reference rates, via the Frankfurter API.
Both permit commercial use with attribution. **You must keep the attribution file
(`ATRIBUSI.txt`) if you redistribute this data.** See it for the exact wording.

## Honest notes

- Empty `nilai` means the upstream source did not publish a value for that period.
  This is normal for some indicator/country combinations — it is not an error here.
- Sources **revise** historical figures. This free export contains only the latest value
  known to us at export time. The revision history is part of the paid dataset.
- Currency: values are in the unit stated in `satuan` (USD, IDR, index, percent,
  or person depending on the indicator).

## Updating it yourself

The data comes from public sources, so you can always refresh it:

```bash
pip install requests
python scripts/fetch_update.py
```

## Paid tiers

This free export covers **Indonesia, annual indicators, latest values only**.

| | Free (this repo) | Paid |
|---|---|---|
| Countries | Indonesia | Indonesia + Malaysia, Philippines, Singapore, Thailand, Vietnam |
| Indicators | 13 annual + USD/IDR daily | Full catalogue (85+ series) |
| Formats | CSV | CSV, XLSX, Parquet |
| Revision history | — | **Every value ever published, with the date we first saw it** |
| Access | Download | REST API + dataset download |

The **revision history** is the part you cannot get anywhere else, including from the World
Bank: when a source revises a number, the old value disappears from their site permanently.
We record every value as we see it, so the archive grows every day and cannot be
reconstructed later by anyone.

- **API**: [Indonesia Macro and Market Data on RapidAPI](https://rapidapi.com/anYoneo/api/indonesia-macro-and-market-data)
- **Dataset download**: [Lynk.id](https://lynk.id/kybow/p199y6wmnv1k)

## License

Code in this repository: MIT. Data: see `ATRIBUSI.txt` (CC BY 4.0 and compatible terms).
