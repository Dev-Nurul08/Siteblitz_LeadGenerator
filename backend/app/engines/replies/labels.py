"""
Reply labels (spec row 14) and the deterministic rules behind the safety labels. Pure functions, no network.

Labels (one message can carry several):
    interested · question · price · sample_requested · not_now · wrong_person      <- the model (commercial)
    stop · complaint_legal · out_of_office · bounce                                <- these rules, never the model
    needs_review                                                                    <- no label could be given

The rules read only what the sender wrote now (parsing.split_reply: quoted history, our own unsubscribe line and the
"-- " signature removed). If nothing is left (a reply written under the quote), they read the whole text without
'>' lines and without our footer, so a stop written in an odd place is still seen.

STOP - English (any form unless a "don't / do not / never" stands right before the verb):
    stop · unsubscribe / un-subscribe / unsub · opt out / opt-out · remove me / us / my email · take me off ·
    delete my email / data / details · don't (or do not / never) email / mail / contact / message / write / send ·
    no more emails · not interested · no interest · no thanks / no thank you · leave me alone ·
    we / I don't need a website / this / your services · a reply that is only "no" / "nope" / "remove"
    Not a stop: "don't stop", "one-stop", "non-stop", "bus stop", "full stop", "stop by", "stop working";
    "unsubscribe" on a newsletter-footer line (with a link, "newsletter", "mailing list", "click", "manage").
STOP - Hindi / Hinglish (romanised and Devanagari):
    band karo / band kar do / bandh kijiye · mat bhejo / mat bhejiye / mat bhejna · mail (message, contact) mat karo
    · dobara (phir se, aage se) mat · nahi chahiye (not after "aur" / "kuch aur") · rehne do / rehne dijiye ·
    zarurat nahi · interest nahi · a reply that is only "nahi" / "na" ·
    बंद करो / बंद कर दो · मत भेजो / मत भेजिए · नहीं चाहिए · रहने दो · ज़रूरत नहीं · रुचि नहीं · दोबारा मत · परेशान मत
STOP - Gujarati (romanised and script):
    nathi joitu / joiti / joie nathi · mokalsho nahi / na mokalsho · jarur nathi · rehva do · band karo ·
    નથી જોઈતું / જોઈતી · જોઈતું નથી · બંધ કરો · મોકલશો નહીં · ના મોકલશો · જરૂર નથી · રહેવા દો · રસ નથી
A click on the unsubscribe link (List-Unsubscribe one-click or the page) is handled by the website and reaches the
app through the suppression list; it needs no rule here.

COMPLAINT / LEGAL (credible = a spam report or a legal threat; weak = only the word spam / scam / fraud):
    report you / reported this (as spam) · marked as spam · this is spam · spamming / spammer · legal action /
    notice · lawyer / attorney · sue · consumer court / forum · court case · police complaint / cyber cell / cyber
    crime · file a complaint / complaint against · harass / harassment · DPDP / GDPR / data protection / IT Act /
    privacy law · illegal / unlawful · shikayat · complaint karunga · case kar dunga · vakil / kanooni ·
    शिकायत · पुलिस · वकील · कानूनी · अदालत · स्पैम · ફરિયાદ · પોલીસ · વકીલ · કાનૂની · સ્પામ
    Not a complaint: "in my spam folder", "went to junk", "no complaints".

COMMITMENT REQUESTS (the sender asks for something only the founder may promise; no draft, flagged):
    discount · deadline / date · guarantee · refund · contract (see the lists below).
"""

import re
from dataclasses import dataclass, field
from typing import Optional

INTERESTED, QUESTION, PRICE, SAMPLE_REQUESTED, NOT_NOW, STOP, OUT_OF_OFFICE, WRONG_PERSON, BOUNCE, COMPLAINT_LEGAL = (
    "interested", "question", "price", "sample_requested", "not_now", "stop", "out_of_office", "wrong_person",
    "bounce", "complaint_legal")
NEEDS_REVIEW = "needs_review"
LABELS = (INTERESTED, QUESTION, PRICE, SAMPLE_REQUESTED, NOT_NOW, STOP, OUT_OF_OFFICE, WRONG_PERSON, BOUNCE,
          COMPLAINT_LEGAL)
SAFETY_LABELS = (STOP, COMPLAINT_LEGAL, OUT_OF_OFFICE, BOUNCE)
COMMERCIAL_LABELS = (INTERESTED, QUESTION, PRICE, SAMPLE_REQUESTED, NOT_NOW, WRONG_PERSON)
DRAFT_LABELS = COMMERCIAL_LABELS
SNAPSHOT_LABELS = (INTERESTED, SAMPLE_REQUESTED)
# An answer to these is owed within 1 business day (spec row 11 "interested reply"; the task adds question, price,
# sample). Messages the model could not label (needs_review) count too: they may be interested.
BACKLOG_LABELS = (INTERESTED, QUESTION, PRICE, SAMPLE_REQUESTED, NEEDS_REVIEW)


def normalise(text: str) -> str:
    text = (text or "").replace("’", "'").replace("‘", "'").replace("`", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.lower().split())


# ─── stop ───────────────────────────────────────────────────────────────────

_NEGATOR_BEFORE = re.compile(r"(?:\bdon'?t|\bdo\s+not|\bdont|\bnever|\bwon'?t|\bwill\s+not|\bplease\s+don'?t|"
                             r"\bno\s+need\s+to|\bnot\s+to)\s+(?:please\s+|ever\s+|you\s+)?$")
_STOP_EXCLUDED_BEFORE = re.compile(r"(?:\bone[\s-]|\bnon[\s-]|\bbus\s|\bfull\s|\bpit\s|\blast\s|\bnext\s|"
                                   r"\bfirst\s|\btruck\s)$")
_STOP_EXCLUDED_AFTER = re.compile(r"^(?:[\s-]+(?:by|in|working|work|loading|responding|functioning|over|being|"
                                  r"shop|watch))\b")
_FOOTER_LINE = re.compile(r"https?://|www\.|\(link removed\)|newsletter|mailing\s+list|click|manage\s+(?:your\s+)?"
                          r"(?:preferences|subscription)|email\s+preferences|update\s+your\s+preferences|"
                          r"view\s+(?:it\s+)?in\s+(?:your\s+)?browser", re.IGNORECASE)

# (name, pattern, may be negated by a "don't" right before it)
_STOP_EN = (
    ("stop", re.compile(r"\bstop\b"), True),
    ("unsubscribe", re.compile(r"\bun-?\s?subscribe\b|\bunsub\b"), True),
    ("opt out", re.compile(r"\bopt(?:\s|-)?out\b"), True),
    ("remove me", re.compile(r"\bremove\s+(?:me|us|my|our|this\s+(?:e-?mail|address|id))\b"), True),
    ("take me off", re.compile(r"\btake\s+(?:me|us|my\s+(?:e-?mail|name|address))\s+off\b"), True),
    ("delete my data", re.compile(r"\b(?:delete|erase)\s+(?:my|our|all\s+my)\s+(?:e-?mail|address|data|personal\s+"
                                  r"data|details|number|id|information|info)\b"), True),
    ("don't email", re.compile(r"\b(?:don'?t|do\s+not|dont|never|pls\s+don'?t)\s+(?:ever\s+)?(?:e-?mail|mail|contact|"
                               r"message|msg|write|send|spam|bother|disturb|call)\b"), False),
    ("no more emails", re.compile(r"\bno\s+more\s+(?:e-?mails?|mails?|messages?|msgs?)\b"), False),
    ("not interested", re.compile(r"\bnot\s+(?:at\s+all\s+)?interested\b|\bno\s+interest\b|\buninterested\b"),
     False),
    ("no thanks", re.compile(r"\bno,?\s+thank(?:s|\s+you)\b"), False),
    ("leave me alone", re.compile(r"\bleave\s+(?:me|us)\s+alone\b"), False),
    ("don't need", re.compile(r"\b(?:we|i)\s+(?:really\s+)?(?:don'?t|do\s+not|dont)\s+(?:need|want)\s+(?:a\s+|any\s+|"
                              r"your\s+|the\s+)?(?:website|web\s*site|site|this|it|services?)\b"), False),
)
_STOP_HINGLISH = (
    ("band karo", re.compile(r"\bbandh?\s*(?:karo|kar\s*do|kardo|krdo|kro|kijiye|kijie|kariye|karein|kare|"
                             r"kar\s*dijiye|kar\s*dena)\b")),
    ("mat bhejo", re.compile(r"\b(?:mat|mt)\s+(?:bhejo|bhejiye|bhejna|bhejen|bhejein|bhejiyega|bheje)\b")),
    ("mail mat karo", re.compile(r"\b(?:e-?mails?|mails?|messages?|msgs?|contact|call|disturb|pareshaa?n|tang)\s+"
                                 r"(?:mat|mt|na)\s+(?:karo|kijiye|kariye|karna|karein|kare|bhejo|bhejiye|bhejna)\b")),
    ("dobara mat", re.compile(r"\b(?:dobara|dubara|phir\s+se|fir\s+se|firse|phirse|aage\s+se)\s+(?:mat|mt|na)\b")),
    ("nahi chahiye", re.compile(r"\b(?:nahi|nahin|nai|nhi|nahee|nahii)\s+(?:chahiye|chaiye|chahie|chaahiye|chiye|"
                                r"chaye)\b")),
    ("rehne do", re.compile(r"\b(?:rehne|rahne|rehene)\s+(?:do|dijiye|dena|de)\b")),
    ("zarurat nahi", re.compile(r"\b(?:zarurat|zaroorat|jarurat|jaroorat|jarur|zarur|jaroor)\s+(?:nahi|nahin|nhi|"
                                r"nai)\b")),
    ("interest nahi", re.compile(r"\b(?:interest|interested|intrest|intrested)\s+(?:nahi|nahin|nhi|nai)\b|"
                                 r"\b(?:nahi|nahin|nhi)\s+(?:hai\s+)?(?:interest|interested)\b")),
    # Gujarati romanised
    ("nathi joitu", re.compile(r"\bnathi\s+(?:joitu|joitun|joiti|joito|joita|joie|joiye|joiee|joituu|jotu)\b|"
                               r"\b(?:joitu|joiti|joito|joie|joiye)\s+nathi\b|\b(?:na|nai)\s+(?:joie|joiye|joiee)\b")),
    ("mokalsho nahi", re.compile(r"\b(?:mokalsho|mokalso|mokalta|moklsho|moklo)\s+(?:nahi|nai|nahin|na)\b|"
                                 r"\bna\s+(?:mokalsho|mokalso|moklo|mokalta)\b")),
    ("jarur nathi", re.compile(r"\b(?:jarur|jaroor|jarurat|zarur)\s+nathi\b|\bras\s+nathi\b")),
    ("rehva do", re.compile(r"\b(?:rehva|reva)\s+(?:do|dyo|dejo)\b")),
)
# Devanagari / Gujarati script: plain substrings (\b is unreliable around vowel signs).
_STOP_SCRIPT = (
    "बंद करो", "बंद कर दो", "बंद कीजिए", "बंद करें", "बन्द करो", "बन्द कर दो", "मत भेजो", "मत भेजिए", "मत भेजें",
    "मत भेजना", "ना भेजें", "नहीं चाहिए", "नही चाहिए", "नहीं चाहिये", "रहने दो", "रहने दीजिए", "ज़रूरत नहीं",
    "जरूरत नहीं", "ज़रुरत नहीं", "रुचि नहीं", "दिलचस्पी नहीं", "दोबारा मत", "फिर से मत", "परेशान मत",
    "નથી જોઈતું", "નથી જોઈતુ", "નથી જોઈતી", "નથી જોઈતો", "જોઈતું નથી", "જોઈતી નથી", "નથી જોઈએ", "જોઈએ નહીં", "બંધ કરો", "બંધ કરી દો", "મોકલશો નહીં",
    "મોકલશો નહિ", "ના મોકલશો", "મોકલવાનું બંધ", "જરૂર નથી", "જરૂરિયાત નથી", "રહેવા દો", "રસ નથી",
)
_STANDALONE_STOP = {"no", "nope", "remove", "unsubscribe", "stop", "nahi", "nahin", "nhi", "na", "nako", "nathi",
                    "नहीं", "ना", "ના", "નહીં", "નથી"}
_FILLERS = {"hi", "hello", "hey", "dear", "sir", "madam", "mam", "ma'am", "ji", "bhai", "team", "please", "pls", "plz",
            "thanks", "thank", "you", "regards", "sorry", "ok", "okay", "but", "and", "sirji"}
_GREETING_LINE = re.compile(r"^(?:hi|hello|hey|dear|namaste|namaskar|good\s+(?:morning|afternoon|evening))\b.{0,40}$",
                            re.IGNORECASE)


def _negated(text: str, start: int) -> bool:
    return bool(_NEGATOR_BEFORE.search(text[max(0, start - 30):start]))


def _footer_line(original: str, needle: str) -> bool:
    """True when every line that contains `needle` looks like a newsletter footer."""
    lines = [line for line in original.splitlines() if needle in line.lower().replace("-", "")]
    return bool(lines) and all(_FOOTER_LINE.search(line) for line in lines)


def _standalone(text: str) -> Optional[str]:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or _GREETING_LINE.match(stripped):
            continue
        tokens = [t for t in re.findall(r"[\w']+", stripped.lower()) if t not in _FILLERS]
        if 1 <= len(tokens) <= 2 and tokens[0] in _STANDALONE_STOP and (len(tokens) == 1
                                                                       or tokens[1] in _STANDALONE_STOP):
            return tokens[0]
        return None
    return None


def stop_matches(text: str) -> list[str]:
    """Names of the stop rules that match `text` (the sender's own words)."""
    found = []
    flat = normalise(text)
    for name, pattern, negatable in _STOP_EN:
        for match in pattern.finditer(flat):
            if negatable and _negated(flat, match.start()):
                continue
            if name == "stop" and (_STOP_EXCLUDED_BEFORE.search(flat[max(0, match.start() - 8):match.start()])
                                   or _STOP_EXCLUDED_AFTER.match(flat[match.end():match.end() + 20])):
                continue
            if name == "unsubscribe" and _footer_line(text, "unsub"):
                continue
            found.append(name)
            break
    for name, pattern in _STOP_HINGLISH:
        for match in pattern.finditer(flat):
            before = flat[max(0, match.start() - 12):match.start()]
            if name == "nahi chahiye" and re.search(r"\b(?:aur|aur\s+kuch|kuch\s+aur|sirf|bas)\s+$", before):
                continue
            found.append(name)
            break
    found += [f"script:{s}" for s in _STOP_SCRIPT if s in (text or "")]
    alone = _standalone(text or "")
    if alone:
        found.append(f"only:{alone}")
    return found


# ─── complaint / legal ──────────────────────────────────────────────────────

_BENIGN_SPAM = re.compile(r"\b(?:in|into|to|from|inside|under|check(?:ed)?|went\s+to|landed\s+in|found\s+in)\s+"
                          r"(?:my\s+|the\s+|your\s+|our\s+)?(?:spam|junk)(?:\s+(?:folder|box|mail|section|filter))?\b|"
                          r"\b(?:spam|junk)\s+(?:folder|box|filter)\b|\bno\s+complaints?\b")
_COMPLAINT_STRONG = (
    re.compile(r"\breport(?:ed|ing)?\s+(?:you|this|it|your\s+\w+|(?:this|the)\s+(?:e-?mail|mail|message))\b"),
    re.compile(r"\b(?:mark(?:ed|ing)?|flag(?:ged|ging)?)\s+(?:you\s+|this\s+|it\s+|your\s+\w+\s+)?(?:as\s+)?"
               r"(?:spam|junk)\b"),
    re.compile(r"\bthis\s+is\s+(?:pure\s+|just\s+|a\s+)?spam\b|\bspamm(?:ing|er|ers|ed)\b|\bstop\s+spam|"
               r"\bspam\s+(?:mail|email|message)s?\b"),
    re.compile(r"\blegal(?:ly)?\s+(?:action|notice|steps|proceedings|case)\b|\b(?:lawyers?|attorneys?|solicitors?)\b|"
               r"\bsue\b"),
    re.compile(r"\bconsumer\s+(?:court|forum|commission)\b|\bcourt\s+case\b|\b(?:take|drag|see)\s+you\s+(?:to|in)\s+"
               r"court\b|\bin\s+court\b|\bcourt\s+(?:me|mein)\b"),
    re.compile(r"\bpolice\s+(?:complaint|case|me|mein|ko)\b|\b(?:to|call|inform|tell)\s+(?:the\s+)?police\b|"
               r"\bcyber\s*(?:cell|crime|police)\b"),
    re.compile(r"\b(?:file|filing|lodge|register|raise)\s+(?:a\s+)?(?:formal\s+)?complaint\b|"
               r"\bcomplaint\s+(?:against|to|with)\b|\bcomplain(?:ing)?\s+(?:to|about\s+you|against)\b"),
    re.compile(r"\bharass(?:ing|ment|ed|es)?\b"),
    re.compile(r"\b(?:dpdp|dpdpa|gdpr)\b|\bdata\s+protection\b|\bit\s+act\b|\bprivacy\s+(?:law|violation|breach)\b|"
               r"\b(?:illegal|unlawful)\b"),
    re.compile(r"\bshikayat\b|\bcomplaint\s+(?:karunga|karungi|kar\s+dunga|kar\s+denge|karenge|kar\s+raha)\b|"
               r"\bcase\s+(?:karunga|kar\s+dunga|karenge|kar\s+denge)\b|\b(?:vakil|vakeel|kanooni|kanuni|qanooni)\b|"
               r"\bfariyad\b"),
)
_COMPLAINT_SCRIPT = ("शिकायत", "पुलिस", "वकील", "कानूनी", "अदालत", "स्पैम", "ફરિયાદ", "પોલીસ", "વકીલ", "કાનૂની",
                     "સ્પામ")
_COMPLAINT_WEAK = re.compile(r"\bspam\b|\bscam\b|\bfraud\b|\bis\s+(?:this|it)\s+legal\b")
_DELETION = re.compile(r"\b(?:delete|erase|remove)\s+(?:my|our|all\s+my)\s+(?:data|personal\s+data|details|"
                       r"information|info)\b")
_DATA_SOURCE = re.compile(r"\b(?:how|where)\s+did\s+you\s+get\s+(?:my|our|this)\s+(?:e-?mail|mail|address|id|number|"
                          r"contact|details)\b|\b(?:mera|hamara|meri)\s+(?:e-?mail|mail|number|id)\s+(?:kaha|kahan)\s+"
                          r"se\b")


@dataclass
class SafetyResult:
    labels: list[str] = field(default_factory=list)
    stop_rules: list[str] = field(default_factory=list)
    complaint_rules: list[str] = field(default_factory=list)
    complaint_credible: bool = False
    deletion_request: bool = False
    data_source_question: bool = False


def complaint_matches(text: str) -> tuple[list[str], bool]:
    flat = _BENIGN_SPAM.sub(" ", normalise(text))
    strong = [p.pattern[:40] for p in _COMPLAINT_STRONG if p.search(flat)]
    strong += [f"script:{s}" for s in _COMPLAINT_SCRIPT if s in (text or "")]
    if strong:
        return strong, True
    weak = _COMPLAINT_WEAK.findall(flat)
    return ([f"weak:{w}" for w in weak], False) if weak else ([], False)


def _strip_prefixes(subject: str) -> str:
    return re.sub(r"^\s*(?:(?:re|fwd?|aw|wg|sv)\s*(?:\[\d+\])?\s*:\s*)+", "", subject or "", flags=re.IGNORECASE)


def fallback_text(full_text: str) -> str:
    """The whole body without '>' lines and our own unsubscribe line (for a reply written under the quote)."""
    keep = [line for line in (full_text or "").splitlines()
            if not line.lstrip().startswith(">")
            and not re.match(r'^\s*Reply\s+"?stop"?\s+or\s+unsubscribe\s+here:', line, re.IGNORECASE)]
    return "\n".join(keep)


def safety_labels(new_text: str, subject: str = "", *, full_text: str = "", original_subject: Optional[str] = None
                  ) -> SafetyResult:
    """stop / complaint_legal from the sender's own words and a changed subject. (out_of_office and bounce come from
    the parser's kind.)"""
    scope = new_text if (new_text or "").strip() else fallback_text(full_text)
    own_subject = _strip_prefixes(subject)
    if original_subject is not None and own_subject.strip().lower() == _strip_prefixes(original_subject).strip().lower():
        own_subject = ""
    result = SafetyResult()
    result.stop_rules = stop_matches(scope) + [f"subject:{m}" for m in stop_matches(own_subject)]
    complaint, credible = complaint_matches(scope + "\n" + own_subject)
    result.complaint_rules, result.complaint_credible = complaint, credible
    result.deletion_request = bool(_DELETION.search(normalise(scope)))
    result.data_source_question = bool(_DATA_SOURCE.search(normalise(scope)))
    if result.stop_rules or result.deletion_request:
        result.labels.append(STOP)
    if complaint:
        result.labels.append(COMPLAINT_LEGAL)
    return result


# ─── commitments: what the sender asks for, and what a draft must never say ─────

_REQUEST_PATTERNS = {
    "discount": (re.compile(r"\bdiscount|\b(?:best|last|lowest|final|minimum|special)\s+(?:price|rate|offer)\b|"
                            r"\b(?:price|rate|cost|charges?)\s+(?:kam|kum|less|lower|reduce)|"
                            r"\b(?:thoda|thodu|kuch|thodi)\s+(?:kam|kum|ochhu|ochu|ocho)\b|"
                            r"\bkam\s+(?:ho\s+sakta|ho\s+sakte|kar\s+sakte|kijiye|kariye)\b|"
                            r"\b(?:cheaper|cheapest|concession|negotiat\w*|bargain)\b|"
                            r"\breduce\s+(?:the\s+)?(?:price|cost|rate)\b|\bfree\s+(?:of\s+cost|me|mein)\b|"
                            r"\bfor\s+free\b|\bmuft\b|\bochh?u\b"),
                 ("छूट", "डिस्काउंट", "ઓછું", "ડિસ્કાઉન્ટ")),
    "date": (re.compile(r"\bdeadline\b|\bkab\s+tak\b|\burgent(?:ly)?\b|\bjaldi\s+(?:chahiye|chaiye)\b|"
                        r"\b(?:need|want|ready|live|done|finish(?:ed)?|complete(?:d)?|deliver(?:ed)?)\s+(?:it\s+|this\s+|"
                        r"the\s+(?:site|website|page)\s+)?(?:by|before)\s+\w+|"
                        r"\b(?:by|before)\s+(?:diwali|navratri|holi|eid|christmas|new\s+year|dussehra|uttarayan|"
                        r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|next\s+week|this\s+week|"
                        r"month\s+end|end\s+of)\b"),
             ("तक चाहिए", "जल्दी चाहिए", "ક્યાં સુધી", "જલ્દી જોઈએ")),
    "guarantee": (re.compile(r"\bguarant\w*|\bgaurant\w*|\bguarent\w*|\bassur(?:e|ance)\b|\bwarrant(?:y|ee)\b|"
                             r"\bpakka\b|\b100\s*%"),
                  ("गारंटी", "ગેરંટી")),
    "refund": (re.compile(r"\brefund\w*|\bmoney\s*-?\s*back\b|\b(?:paise|paisa|paisay|pese)\s+(?:wapas|vapas|vaapas|"
                          r"pacha)\b"),
               ("रिफंड", "પૈસા પાછા", "રિફંડ")),
    "contract": (re.compile(r"\bcontract\b|\bagreement\b|\bterms\s+(?:and|&)\s+conditions\b|\bt\s*&\s*c\b|\bnda\b|"
                            r"\binvoice\b|\bgst\s+(?:bill|invoice|number)\b"),
                 ("अनुबंध", "કરાર")),
}


def commitment_requests(text: str) -> list[str]:
    """Which founder-only topics the sender asks about: discount, date, guarantee, refund, contract."""
    flat = normalise(text)
    return [name for name, (pattern, script) in _REQUEST_PATTERNS.items()
            if pattern.search(flat) or any(s in (text or "") for s in script)]


_WEEKDAYS = r"monday|tuesday|wednesday|thursday|friday|saturday|sunday"
_MONTH_NAMES = (r"january|february|march|april|june|july|august|september|october|november|december|"
                r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec")
_URL_IN_DRAFT = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_GUARANTEE_NEGATION = re.compile(r"(?:\bcannot|\bcan'?t|\bdon'?t|\bdo\s+not|\bno|\bnot|\bnever|\bwithout|\bnor)\s+"
                                 r"(?:\w+\s+){0,2}$")
_DRAFT_PATTERNS = {
    "discount": re.compile(r"\bdiscount|\d+\s*%|\bper\s*cent\b|\bspecial\s+(?:price|offer|rate|deal)\b|"
                           r"\breduced\s+(?:price|rate)\b|\b(?:lower|cheaper|best|last)\s+price\b|\bconcession\b|"
                           r"\bfor\s+free\b|\bfree\s+of\s+(?:cost|charge)\b|\bcomplimentary\b|\bwaive\w*|"
                           r"\bat\s+no\s+(?:extra\s+)?cost\b|छूट"),
    "date": re.compile(r"\b(?:" + _WEEKDAYS + r")\b|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:" + _MONTH_NAMES + r"|may)\b|"
                       r"\b(?:" + _MONTH_NAMES + r")\.?\s+\d{1,2}\b|\bmay\s+\d{1,2}\b|\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b|"
                       r"\b\d{4}-\d{2}-\d{2}\b|\b(?:tomorrow|tonight|today|next\s+week|this\s+week|next\s+month|"
                       r"end\s+of\s+(?:the\s+)?(?:week|month))\b|\b(?:kal|parso|parson|aaj)\b|"
                       r"\b(?:diwali|navratri|holi|eid|christmas|dussehra|uttarayan)\b"),
    "guarantee": re.compile(r"\bguarant\w*|\bpromis\w*|\bassur\w*|\b100\s*%|\bpakka\b"),
    "refund": re.compile(r"\brefund\w*|\bmoney\s*-?\s*back\b"),
    "contract": re.compile(r"\bcontract\b|\bagreement\b|\bterms\s+(?:and|&)\s+conditions\b|\bliabilit\w*|"
                           r"\bpenalt\w*|\bwarrant(?:y|ies|ee)\b|\bbinding\b|\bnda\b"),
}
_DURATION = re.compile(r"\b(?:within\s+)?\d+\s+(?:working\s+)?(?:hours?|days?|weeks?|months?)\b")


def draft_violations(model_text: str, facts_text: str) -> list[str]:
    """Reply rule (spec row 14 / RESULT row 19): a draft never offers a discount, names a date or deadline, gives a
    guarantee, a refund or contract terms. `model_text` = what the model wrote (body + sign-off), never the app's
    signature. A duration is allowed only when COMPANY_FACTS has the same words (e.g. "2 working days",
    "within 60 days"); "we cannot guarantee" is allowed."""
    flat = normalise(_URL_IN_DRAFT.sub(" ", model_text or ""))
    facts = normalise(facts_text)
    found = []
    for name, pattern in _DRAFT_PATTERNS.items():
        for match in pattern.finditer(flat):
            if name == "guarantee" and _GUARANTEE_NEGATION.search(flat[max(0, match.start() - 30):match.start()]):
                continue
            found.append(f"{name}: {match.group()!r}")
            break
    for match in _DURATION.finditer(flat):
        if match.group() not in facts:
            found.append(f"date: {match.group()!r} is not in the company facts")
    return found
