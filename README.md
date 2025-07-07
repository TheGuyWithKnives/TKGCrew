# Disciplína HRAVĚ

Jednoduchá aplikace pro hravé budování disciplíny. Každý den automaticky generuje plán aktivit z několika kategorií a při nesplnění nabízí náhodně vybraný trest. Výsledky si můžete odškrtávat v příkazové řádce.

## Základní používání

```
python3 discipline_hrave.py --generate   # vygeneruje plán na dnešek
python3 discipline_hrave.py --show       # zobrazí plán
python3 discipline_hrave.py --check pohyb  # označí úkol 'pohyb' jako splněný
```

Data se ukládají do souboru `state.json`.
