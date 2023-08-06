# Derivational processes
A derivational process is an operation that turns one [stem](../stems) into another.
Which stems undergo which processes to yield which new stems is described in [derivations](../derivations).

## DerivProcTable: `derivationalprocesses.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | singlevalued | <div> <p>A title, name or label for an entity.</p> </div> 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | singlevalued | <div> <p>A description for an entity.</p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | <div> <p> An identifier referencing a language either </p> <ul> <li>by providing a foreign key into the LanguageTable or</li> <li>by using a known encoding scheme.</li> </ul> </div> <br>References LanguageTable