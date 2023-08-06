# Morphemes
Morphemes are abstract entities that contain one or multiple [morphs](../morphs).


## MorphemeTable: `morphemes.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | A reference to a language (or variety) the morpheme belongs to.<br>References LanguageTable
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | singlevalued | <div> <p>A title, name or label for an entity.</p> </div> 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | singlevalued | A human-readable description.
`Parameter_ID` | list of `string` (separated by `; `) | multivalued | A reference to the meaning denoted by the morpheme.
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `; `) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 
[Part_Of_Speech](http://cldf.clld.org/v1.0/terms.rdf#partOfSpeech) | `string` | singlevalued | <div> <p> The part-of-speech of dictionary entry. </p> </div> <br>References partsofspeech.csv.