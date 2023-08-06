# Wordformparts
A wordformpart primarily connects a [morph](../morphs) with a [wordform](../wordforms), whereby the `Index` column refers to the `Morpho_Segments` of the wordform.
This "morph-in-a-wordform" can have multiple [glosses](gloss) (e.g. `1` and `PL`).

Wordformparts are also used to model zero marking.
In that case, they contain no `Morph_ID` and no `Index`.
[Inflections](../inflections) can refer to "zero" wordformparts the same way they refer to non-zero wordformparts associated with a morph.

## WordformParts: `wordformparts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
`Wordform_ID` | `string` | singlevalued | The involved wordform.<br>References wordforms.csv.
`Morph_ID` | `string` | singlevalued | The involved morph.<br>References morphs.csv.
`Index` | `string` | singlevalued | Specifies the position of a morph in a wordform.
`Gloss_ID` | list of `string` (separated by `,`) | multivalued | The gloss the morph has in the wordform.<br>References glosses.csv.