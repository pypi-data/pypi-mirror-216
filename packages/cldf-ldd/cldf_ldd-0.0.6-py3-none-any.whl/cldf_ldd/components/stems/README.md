# Stems
A stem is what [inflectional morphological processes](../inflections) are applied to to form a valid [wordform](../wordforms).
Inflectional morphology may not be needed for a valid form.
Stems can be [morphologically complex](../stemparts), being formed by processes like [derivation](../derivations) or composition (not yet modeled).

## StemTable: `stems.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | A reference to a language (or variety) the stem belongs to<br>References LanguageTable
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | singlevalued | <div> <p>A title, name or label for an entity.</p> </div> 
`Lexeme_ID` | `string` | singlevalued | The lexeme this stem belongs to.<br>References lexemes.csv.
`Parameter_ID` | list of `string` (separated by `; `) | multivalued | A reference to the meaning denoted by the stem.
`Morpho_Segments` | list of `string` (separated by ` `) | multivalued | A representation of the morphologically segmented stem.
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | multivalued | <div> <p> A list of segments (aka a sound sequence) is understood as the strict segmental representation of a <a href="http://linguistics-ontology.org/gold/2010/FormUnit">form unit</a> of a language, which is usually given in phonetic transcription. <a href="http://linguistics-ontology.org/gold/2010/Suprasegmental">Suprasegmental elements</a>, like tone or accent, of sound sequences are usually represented in a sequential form, although they are usually co-articulated along with the segmental elements of a sound sequence. Alternatively, suprasegmental aspects could also be represented as part of the <a href="#prosodicStructure">prosodic structure</a> of a word form. </p> </div> 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `; `) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 
[Part_Of_Speech](http://cldf.clld.org/v1.0/terms.rdf#partOfSpeech) | `string` | singlevalued | <div> <p> The part-of-speech of dictionary entry. </p> </div> <br>References partsofspeech.csv.