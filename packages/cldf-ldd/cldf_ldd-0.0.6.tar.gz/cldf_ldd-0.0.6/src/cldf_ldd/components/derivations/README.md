# Derivations
A derivation relates a [stem](../stems) or a [root](../morphs) to a derived stem via a [derivational process](../derivationalprocesses).
Optionally, it can reference one or multiple morph(s) contained in the derived stem.


## DerivationTable: `derivations.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
`Process_ID` | `string` | singlevalued | The derivational process involved.<br>References derivationalprocesses.csv.
`Target_ID` | `string` | singlevalued | The derived stem.<br>References stems.csv.
`Source_ID` | `string` | singlevalued | The stem to which the derivational process applies.<br>References stems.csv.
`Root_ID` | `string` | singlevalued | The root to which the derivational process applies.<br>References morphs.csv.
`Stempart_IDs` | list of `string` (separated by `,`) | multivalued | Specifies one or multiple morphs in the stem marking the derivation.<br>References stemparts.csv.
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 