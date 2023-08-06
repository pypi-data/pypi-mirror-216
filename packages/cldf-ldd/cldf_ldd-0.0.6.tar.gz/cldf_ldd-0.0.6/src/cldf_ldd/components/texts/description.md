# Texts

Texts can roughly be defined as cohesive stretches of discourse in the object language.
They are part of the Boasian trilogy, and fundamental to corpus-based language description.

In CLDF, it can be conceptualized as a list of [Examples](https://github.com/cldf/cldf/tree/master/components/examples)[^1]: the `Text_ID` column references the text, and two more columns (called `Sentence_Number` and `Phrase_Number` in [lapollaqiang](https://github.com/cldf-datasets/lapollaqiang/tree/master/cldf)) store its position in the text.
The properties below should mostly be self-explanatory.
`Type` is intended to hold genres like 'personal narrative' or 'conversation'.
`Metadata` is a JSON field for things like tags, duration, etc.

[^1]: Of course, they only become examples when they are used as such, but this misnomer is not significant.