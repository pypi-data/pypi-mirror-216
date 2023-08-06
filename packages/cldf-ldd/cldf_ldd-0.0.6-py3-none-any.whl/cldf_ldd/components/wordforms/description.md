# Wordforms
Wordforms are units analyzed as grammatical words in a given language.
Although there has been some discussion as to the universality of such a concept, it is useful for the description of many languages.
The morphological segmentation of wordforms is stored in the `Morpho_Segments` column via [an association table](../wordformparts).
`Stem_ID` optionally references a [stem](../stems) of which a wordform is an inflected form; wordforms are also connected to stems via [wordformstems](../formstems).