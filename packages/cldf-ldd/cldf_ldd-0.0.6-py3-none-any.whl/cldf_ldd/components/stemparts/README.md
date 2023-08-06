# Stemparts


## StemParts: `stemparts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
`Stem_ID` | `string` | singlevalued | The involved stem.<br>References stems.csv.
`Morph_ID` | `string` | singlevalued | The involved morph.<br>References morphs.csv.
`Index` | `string` | singlevalued | Specifies the position of a morph in a stem.
`Gloss_ID` | list of `string` (separated by `,`) | multivalued | The gloss the morph has in the stem.<br>References glosses.csv.