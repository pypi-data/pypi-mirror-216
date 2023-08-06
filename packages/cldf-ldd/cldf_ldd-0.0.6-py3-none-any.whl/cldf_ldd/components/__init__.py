from clldutils import jsonlib

try:
    from importlib.resources import files  # pragma: no cover
except ImportError:  # pragma: no cover
    from importlib_resources import files  # pragma: no cover

__all__ = [
    "WordformTable",
    "StemTable",
    "MorphTable",
    "InflectionTable",
    "InflValTable",
    "InflCatTable",
    "LexemeTable",
    "MorphemeTable",
    "DerivationTable",
    "DerivProcTable",
    "WordformParts",
    "FormParts",
    "FormStems",
    "StemParts",
    "GlossTable",
    "POSTable",
    "TextTable",
    "ExampleParts",
    "PhonemeTable",
    "SpeakerTable",
]

cldf_path = files("cldf_ldd") / "components"
WordformTable = jsonlib.load(cldf_path / "wordforms/WordformTable-metadata.json")
StemTable = jsonlib.load(cldf_path / "stems/StemTable-metadata.json")
MorphTable = jsonlib.load(cldf_path / "morphs/MorphTable-metadata.json")
InflectionTable = jsonlib.load(cldf_path / "inflections/InflectionTable-metadata.json")
InflValTable = jsonlib.load(cldf_path / "inflectionalvalues/InflValTable-metadata.json")
InflCatTable = jsonlib.load(
    cldf_path / "inflectionalcategories/InflCatTable-metadata.json"
)
LexemeTable = jsonlib.load(cldf_path / "lexemes/LexemeTable-metadata.json")
MorphemeTable = jsonlib.load(cldf_path / "morphemes/MorphemeTable-metadata.json")
DerivationTable = jsonlib.load(cldf_path / "derivations/DerivationTable-metadata.json")
DerivProcTable = jsonlib.load(
    cldf_path / "derivationalprocesses/DerivProcTable-metadata.json"
)
WordformParts = jsonlib.load(cldf_path / "wordformparts/WordformParts-metadata.json")
FormParts = jsonlib.load(cldf_path / "formparts/FormParts-metadata.json")
FormStems = jsonlib.load(cldf_path / "formstems/FormStems-metadata.json")
StemParts = jsonlib.load(cldf_path / "stemparts/StemParts-metadata.json")
GlossTable = jsonlib.load(cldf_path / "glosses/GlossTable-metadata.json")
POSTable = jsonlib.load(cldf_path / "partsofspeech/POSTable-metadata.json")
TextTable = jsonlib.load(cldf_path / "texts/TextTable-metadata.json")
ExampleParts = jsonlib.load(cldf_path / "exampleparts/ExampleParts-metadata.json")
PhonemeTable = jsonlib.load(cldf_path / "phonemes/PhonemeTable-metadata.json")
SpeakerTable = jsonlib.load(cldf_path / "speakers/SpeakerTable-metadata.json")

tables = [
    WordformTable,
    StemTable,
    MorphTable,
    InflectionTable,
    InflValTable,
    InflCatTable,
    LexemeTable,
    MorphemeTable,
    DerivationTable,
    DerivProcTable,
    WordformParts,
    FormParts,
    FormStems,
    StemParts,
    GlossTable,
    POSTable,
    TextTable,
    ExampleParts,
    PhonemeTable,
    SpeakerTable,
]
