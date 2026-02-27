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

## Fragen

- Besser "Funktionen" wie toint32(float32 val) als cast?
  Ein expliziter Cast (int32) ist für eine C-ähnliche Sprache intuitiver und kompakter als eine Funktion. Die Frage ist hier aber, macht das den Compiler komplizierter? 

- Macht bei den Vergleichsoperatoren für float32 eine Toleranz für Ungenauigkeiten
  Sinn, oder soll `==` ganz unzulässig sein? (Vorschlag: `==` für float32 verbieten,
  stattdessen `abs(a - b) < epsilon` verwenden)