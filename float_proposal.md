# Erweiterung um float32

Erweitere die Sprache NanoC um einen primitiven Datentyp float32.

## Typdefinition

float32 ist ein 32-Bit IEEE-754 Gleitkommatyp.

int32 bleibt ein 32-Bit signed Integer.

```c
float32 factor = 3.567
```

## Literale

Ganzzahlen wie 2 sind immer vom Typ int32.

Dezimalzahlen wie 2.0 sind immer vom Typ float32.

-2.0 wird vom Compiler so behandelt wie bisher -2.

## Typregeln

Es gibt keine automatische Typumwandlung zwischen int32 und float32.

Alle Umwandlungen müssen explizit per Cast erfolgen:

(float32)x

(int32)y

Operatoren dürfen nur auf Operanden desselben Typs angewendet werden.

Vergleichsoperatoren zwischen int32 und float32 sind ohne expliziten Cast verboten.

Modulo-Operator, boolsche und bitweise Operatoren sind nur für int32 erlaubt.

## Division

int32 / int32 führt Ganzzahldivision aus. Das Ergebnis ist ein int32-Wert.

Beispiel: 5 / 2 == 2.

float / float führt Gleitkommadivision aus. Das Ergebnis ist ein float32-Wert.

## Funktionsaufrufe

Funktionsparameter müssen exakt typgleich sein.

Keine implizite Konvertierung bei Funktionsaufrufen.

## Spezialwerte

float32 unterstützt kein NaN, oder ähnliches. Alle float32-Operationen, die zu undefinierten Ergebnissen führen würden, liefern stattdessen 0.0.

## Einschränkungen

float32 ist nur für einfache Variablen erlaubt.

Arrays von float32 sind nicht erlaubt.

## printf-Ausgabe

Für die Ausgabe von float32-Werten wird printf um die Formate %f und %g erweitert. %g empfiehlt sich für kompakte Darstellung mit maximal 6 signifikanten Stellen.

## Weitere Funktionen

`str$` sollten auch für float32 funktionieren. Evtl. ist ein synonym für %g sinnvoll, z.B. `gstr$`.

`abs` sollte für int32 eingeführt und dann auch für float32 funktionieren.

`hex$` ist nur für int32 sinnvoll.

## Designentscheidungen

- **Cast-Syntax**: `(float32)x` und `(int32)y` sind einer Funktionssyntax vorzuziehen –
  kompakter und für eine C-ähnliche Sprache intuitiver. Die Cast-Syntax erfordert im Parser
  einen kurzen Lookahead, ist aber klar implementierbar.

- **`==` für float32 verboten**: Float-Gleichheitsvergleich ist in Embedded-Kontexten
  fast immer ein Bug. Stattdessen `abs(a - b) < epsilon` verwenden.

## Offene Implementierungsfragen

- **`ret_val` in der VM** ist aktuell `int32_t` – müsste zu `uint32_t` (oder einer Union)
  werden, damit float-Rückgabewerte bitweise korrekt transportiert werden.

- **Externe Funktionen**: `nc_pop_num`/`nc_push_num` arbeiten auf `int32_t`.
  Für float-taugliche External-Functions wären `nc_pop_float`/`nc_push_float`
  sowie eine neue Typkonstante `NB_FLOAT` erforderlich.

- **`abs`**: Als Built-in-Opcode `k_ABS_N1` realisiert (analog zu `k_RND_N1`).
  ✓ Implementiert für int32. Für float32 wäre ein separater `k_FABS_N1`-Opcode nötig.

- **`str$` vs. `gstr$`**: `str$` intern mit `%g` reicht aus, wenn `str$` ohnehin
  nur formatted-output ist. `gstr$` als Alias ist nicht notwendig.

## Status

**Implementierung aktuell nicht geplant.** Der Footprint würde durch zusätzliche
Float-Opcodes, erweiterte Symboltabelle (Typtracking) und neue API-Funktionen
spürbar steigen. Der konkrete Mehrwert für die Zielplattformen muss erst
geklärt werden, bevor mit der Umsetzung begonnen wird.

Wenn die Implementierung erfolgt, ist zu klären, ob die Float-Operationen auch für externe Funktionen verfügbar sein sollen, oder ob sie auf interne VM-Operationen beschränkt bleiben. Aktuell sehe ich keinen Bedarf für Float-External-Functions, da die meisten Anwendungsfälle in Embedded-Umgebungen mit Integer-Arithmetik auskommen.