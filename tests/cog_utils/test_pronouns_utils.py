import sys
from pathlib import Path

from dotenv import load_dotenv

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

load_dotenv()

from libs.cog_utils.pronouns import parse_pronouns
from libs.cog_utils.pronouns.utils import (
    format_inline_references,
    format_link_references,
    format_multi_reference,
    format_term_references,
)

KNOWN_MULTI = "{Asexual}|{Aromantic}"
KNOWN_MULTI_RESULT = "([Asexual](https://en.pronouns.page/terminology#Asexual); [Aromantic](https://en.pronouns.page/terminology#Aromantic))"
KNOWN_NON_MULTI = "{Transgender}"
KNOWN_NON_MULTI_RESULT = (
    "[Transgender](https://en.pronouns.page/terminology#Transgender)"
)

LINK_REFERENCE = "http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0057%3Aentry%3Da)1=ἀ-"
IDEAL_LINK = "[ἀ-](http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0057%3Aentry%3Da%291)"
NORMAL_TERM = "#gender binary=binary"
WEIRD_TERM = "/trans=trans"
DIFFERENT_TERM = "masculinity"

IDEAL_TERM_RESULTS = {
    "binary": "[binary](https://en.pronouns.page/terminology#gender%20binary)",
    "trans": "[trans](https://en.pronouns.page/terminology#trans)",
    "masculinity": "[masculinity](https://en.pronouns.page/terminology#masculinity)",
}

TERM_DESCRIPTION = "an umbrella term referring to the {aromantic spectrum} and the {asexual spectrum}. Using it only with reference to asexuality is mistaken and leads to {aromantic erasure}."
KNOWN_DESCRIPTION = "an umbrella term referring to the [aromantic spectrum](https://en.pronouns.page/terminology#aromantic%20spectrum) and the [asexual spectrum](https://en.pronouns.page/terminology#asexual%20spectrum). Using it only with reference to asexuality is mistaken and leads to [aromantic erasure](https://en.pronouns.page/terminology#aromantic%20erasure)."

ANOTHER_DESCRIPTION = "from Ancient Greek negative prefix {http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0057%3Aentry%3Da)1=ἀ-} [a-], and English {#gender binary=binary}"
ANOTHER_KNOWN = "from Ancient Greek negative prefix [ἀ-](http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.04.0057%3Aentry%3Da%291) [a-], and English [binary](https://en.pronouns.page/terminology#gender%20binary)"

HARDEST_DESCRIPTION = "a term referring to people whose {#AGAB=gender assigned at birth} is different than their {gender identity}. It includes {#trans man=trans men} and {#trans woman=trans women} as well as {non-binary} people. Many, but not all, transgender people experience {gender dysphoria} or {#gender euphoria=euphoria}. Some opt for medical {transition} (e.g. {#HRT=hormone replacement therapy} or {#SRS=surgeries}), but not all (they may be unable due to financial or political reasons, or simply may not want to). Some opt for changing their {legal gender} marker, but not all. It should be noted that procedures of changing one's legal gender marker may be difficult or simply non-existent in certain countries; moreover, in many countries there is no option available for {non-binary} people. Whether (and how) a person transitions has no bearing on the validity of their identity."
HARDEST_KNOWN_DESCRIPTION = "a term referring to people whose [gender assigned at birth](https://en.pronouns.page/terminology#AGAB) is different than their [gender identity](https://en.pronouns.page/terminology#gender%20identity). It includes [trans men](https://en.pronouns.page/terminology#trans%20man) and [trans women](https://en.pronouns.page/terminology#trans%20woman) as well as [non-binary](https://en.pronouns.page/terminology#non-binary) people. Many, but not all, transgender people experience [gender dysphoria](https://en.pronouns.page/terminology#gender%20dysphoria) or [euphoria](https://en.pronouns.page/terminology#gender%20euphoria). Some opt for medical [transition](https://en.pronouns.page/terminology#transition) (e.g. [hormone replacement therapy](https://en.pronouns.page/terminology#HRT) or [surgeries](https://en.pronouns.page/terminology#SRS)), but not all (they may be unable due to financial or political reasons, or simply may not want to). Some opt for changing their [legal gender](https://en.pronouns.page/terminology#legal%20gender) marker, but not all. It should be noted that procedures of changing one's legal gender marker may be difficult or simply non-existent in certain countries; moreover, in many countries there is no option available for [non-binary](https://en.pronouns.page/terminology#non-binary) people. Whether (and how) a person transitions has no bearing on the validity of their identity."


def test_pronoun():
    pronouns = ["she", "they", "it"]
    res = parse_pronouns(pronouns)
    assert res == "she/her, they/them, it/its"


def test_format_link_references():
    formatted_link = format_link_references(LINK_REFERENCE)
    assert formatted_link == IDEAL_LINK


def test_format_term_references():
    formatted_link = format_term_references(NORMAL_TERM)
    assert formatted_link == IDEAL_TERM_RESULTS["binary"]

    other_link = format_term_references(WEIRD_TERM)
    assert other_link == IDEAL_TERM_RESULTS["trans"]

    another_link = format_term_references(DIFFERENT_TERM)
    assert another_link == IDEAL_TERM_RESULTS["masculinity"]


def test_format_inline_references():
    easy_format = format_inline_references(TERM_DESCRIPTION)
    assert easy_format == KNOWN_DESCRIPTION

    harder = format_inline_references(ANOTHER_DESCRIPTION)
    assert harder == ANOTHER_KNOWN

    hardest = format_inline_references(HARDEST_DESCRIPTION)
    assert hardest == HARDEST_KNOWN_DESCRIPTION


def test_format_multi_reference():
    formatted = format_multi_reference(KNOWN_MULTI)
    assert formatted == KNOWN_MULTI_RESULT

    non_multi = format_multi_reference(KNOWN_NON_MULTI)
    assert non_multi == KNOWN_NON_MULTI_RESULT
