# ExampleParts

Example parts simply connect wordforms with examples, along with the meaning the form has in this context.

## ExampleParts: `exampleparts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
`Wordform_ID` | `string` | singlevalued | <br>References wordforms.csv.
`Example_ID` | `string` | singlevalued | 
`Index` | `string` | singlevalued | Specifies the position of a form in a sentence.
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | singlevalued | A reference to the meaning denoted by the form<br>References ParameterTable