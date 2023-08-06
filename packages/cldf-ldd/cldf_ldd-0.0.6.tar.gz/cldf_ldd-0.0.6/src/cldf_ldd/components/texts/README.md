# Texts

Texts can roughly be defined as cohesive stretches of discourse in the object language.
They are part of the Boasian trilogy, and fundamental to corpus-based language description.

In CLDF, it can be conceptualized as a list of [Examples](https://github.com/cldf/cldf/tree/master/components/examples)[^1]: the `Text_ID` column references the text, and two more columns (called `Sentence_Number` and `Phrase_Number` in [lapollaqiang](https://github.com/cldf-datasets/lapollaqiang/tree/master/cldf)) store its position in the text.
The properties below should mostly be self-explanatory.
`Type` is intended to hold genres like 'personal narrative' or 'conversation'.
`Metadata` is a JSON field for things like tags, duration, etc.

[^1]: Of course, they only become examples when they are used as such, but this misnomer is not significant.

## TextTable: `texts.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | singlevalued | <div> <p>A title, name or label for an entity.</p> </div> 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | singlevalued | <div> <p>A description for an entity.</p> </div> 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 
`Type` | `string` | singlevalued | 
`Metadata` | `json` | singlevalued | 