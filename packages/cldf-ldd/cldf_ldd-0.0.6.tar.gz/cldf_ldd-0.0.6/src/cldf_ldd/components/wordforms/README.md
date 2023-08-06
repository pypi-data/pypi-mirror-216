# Wordforms
Wordforms are units analyzed as grammatical words in a given language.
Although there has been some discussion as to the universality of such a concept, it is useful for the description of many languages.
The morphological segmentation of wordforms is stored in the `Morpho_Segments` column via [an association table](../wordformparts).
`Stem_ID` optionally references a [stem](../stems) of which a wordform is an inflected form; wordforms are also connected to stems via [wordformstems](../formstems).

## WordformTable: `wordforms.csv`

Name/Property | Datatype | Cardinality | Description
 --- | --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | singlevalued | <div> <p>A unique identifier for a row in a table.</p> <p> To allow usage of identifiers as path components of URLs IDs must only contain alphanumeric characters, underscore and hyphen. </p> </div> 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | singlevalued | A reference to a language (or variety) the form belongs to<br>References LanguageTable
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | singlevalued | The written expression of the form.
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | singlevalued | A human-readable description
[Part_Of_Speech](http://cldf.clld.org/v1.0/terms.rdf#partOfSpeech) | `string` | singlevalued | <div> <p> The part-of-speech of dictionary entry. </p> </div> <br>References partsofspeech.csv.
`Parameter_ID` | list of `string` (separated by `; `) | multivalued | A reference to the meaning denoted by the form
`Morpho_Segments` | list of `string` (separated by ` `) | multivalued | A representation of the morphologically segmented form.
`Stem_ID` | `string` | singlevalued | The stem of which this wordform is an inflected form.<br>References stems.csv.
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | multivalued | <div> <p> A list of segments (aka a sound sequence) is understood as the strict segmental representation of a <a href="http://linguistics-ontology.org/gold/2010/FormUnit">form unit</a> of a language, which is usually given in phonetic transcription. <a href="http://linguistics-ontology.org/gold/2010/Suprasegmental">Suprasegmental elements</a>, like tone or accent, of sound sequences are usually represented in a sequential form, although they are usually co-articulated along with the segmental elements of a sound sequence. Alternatively, suprasegmental aspects could also be represented as part of the <a href="#prosodicStructure">prosodic structure</a> of a word form. </p> </div> 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | singlevalued | <div> <p> A human-readable comment on a resource, providing additional context. </p> </div> 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | multivalued | <div> <p>List of source specifications, of the form &lt;source_ID&gt;[], e.g. http://glottolog.org/resource/reference/id/318814[34], or meier2015[3-12] where meier2015 is a citation key in the accompanying BibTeX file.</p> </div> 