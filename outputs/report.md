# Foundry Twin experiment report

Industry twin simulation using syntheic assumptions and data. Results are not validated foundry predictions, processing design rules, or manufacturing instructions.

Run ID: 97

## Baseline

```text
Process: demo_mature
Performance: 24576.00 TOPS | Power: 26.59 W
Area: 134.80 mm2 | Junction: 33.51 °C
Yield: 8.51% | Expected good dies/wafer: 28.67
Cost/good die: $402.10 | Lot duration: 4.20 days
Bottleneck: lithogrophy | Feasible in model: False
FailedChecks: Yield fraction, Cost per good die USD
```

## Constraints

| Check | Observed | Rule | Limit | Pass |
|---|---:|---:|:---:|
| Voltage floor | 0.8500 | >= | 0.6500 | True |
| Voltage ceiling | 0.8500 | <= | 1.0500 | True |
| Frequency at voltage (surrogate) | 1.5000 | <= | 2.2400 | True |
| Die area mm2 | 134.8000 | <= | 850.0000 | True |
| Gross die per wafer | 337 | >= | 1 | True |
| Performance TOPS | 24576.0000 | >= | 80 | True |
| Power W | 26.5860 | <= | 180 | True |
| Junction temperature °C | 33.5075 | <= | 95 | True |
| Yield fraction | 0.0851 | >= | 0.6000 | False |
| Cost per good die USD | 402.1036 | <= | 180 | False |
| Lot duration days | 4.2010 | <= | 30 | True |

## Grid search

Evaluated 100 candidates; 0 were feasible.

No candidate met every constraint. No optimum is claimed.

## Interpretation

This is finite-grid result under assumed parameters. Measured data, timing/power tools, licensed process rules and model validation are needed before industrial use.
