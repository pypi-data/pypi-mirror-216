# Wordformparts
A wordformpart primarily connects a [morph](../morphs) with a [wordform](../wordforms), whereby the `Index` column refers to the `Morpho_Segments` of the wordform.
This "morph-in-a-wordform" can have multiple [glosses](gloss) (e.g. `1` and `PL`).

Wordformparts are also used to model zero marking.
In that case, they contain no `Morph_ID` and no `Index`.
[Inflections](../inflections) can refer to "zero" wordformparts the same way they refer to non-zero wordformparts associated with a morph.