# Inflection
Inflection refers to morphological processes with which wordforms express [grammatical categories](../inflectionalcategories) like person, tense, or gender.
Inflections are conceptualized as linking a [wordform](../wordforms) (via a [wordformpart](../wordformpart)) with the following entities: a [stem](../stems) (of which it is an inflected form), an [inflectional value](inflectionalvalues) (for which it is inflected).
The multivalued nature of `Wordformpart_ID` allows multiple inflectional values expressed in a single morph.

## InflectionTable: `inflections.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
`Stem_ID` | `string` | singlevalued | The stem this wordform is an inflected form of.<br>References stems.csv.
`Value_ID` | `string` | singlevalued | The inflectional value being expressed.<br>References inflectionalvalues.csv.
`Wordformpart_ID` | list of `string` (separated by `,`) | multivalued | The part of the wordform expressing this value.<br>References wordformparts.csv.
`Form_ID` | `string` | singlevalued | The multi-word form this inflection references.<br>References forms.csv.