"""Top-level package for clld-document-plugin."""
import re
from clld.db.models import Sentence
from clld.db.models import common
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld_corpus_plugin.util import rendered_sentence
from markdown.extensions.toc import TocExtension
from clld_document_plugin import datatables
from clld_document_plugin import interfaces
from clld_document_plugin import models
from clld_markdown_plugin import link_entity


__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.5"

glossing_delimiters = [
    "-",
    "–",
    ".",
    "=",
    ";",
    ":",
    "*",
    "~",
    "<",
    ">",
    r"\[",
    r"\]",
    "(",
    ")",
    "/",
    r"\\",
]


def split_word(word):
    parts = re.split(r"([" + "|".join(glossing_delimiters) + "])", word)
    parts = [x for x in parts if x != ""]
    return parts


def resolve_glossing_combination(input_string):
    output = []
    temp_text = ""
    for i, char in enumerate(list(input_string)):
        if re.match(r"[1-3]+", char):
            if i < len(input_string) - 1 and input_string[i + 1] == "+":
                temp_text += char
            elif input_string[i - 1] == "+":
                temp_text += char
                output.append(temp_text)
                temp_text = ""
            else:
                if temp_text != "":
                    output.append(temp_text)
                output.append(char)
                temp_text = ""
        else:
            temp_text += char
    if temp_text != "":
        output.append(temp_text)
    return output


def is_gloss_abbr_candidate(part, parts, j):
    return (
        part == part.upper()  # needs to be uppercase
        and part not in glossing_delimiters + ["[", "]", "\\"]  # and not a delimiter
        and part != "?"  # question marks may be used for unknown or ambiguous analyses
        and not (
            len(parts) > j + 2
            and parts[j + 2] in glossing_delimiters
            and parts[j + 1] not in [">", "-"]
        )
    )


def decorate_gloss_string(input_string, decoration=lambda x: f"\\gl{{{x}}}"):
    words_list = input_string.split(" ")
    for i, word in enumerate(words_list):  # pylint: disable=too-many-nested-blocks
        output = " "
        # take proper nouns into account
        if len(word) == 2 and word[0] == word[0].upper() and word[1] == ".":
            output += word
        else:
            parts = split_word(word)
            for j, part in enumerate(parts):
                if is_gloss_abbr_candidate(part, parts, j):
                    # take care of numbered genders
                    if part[0] == "G" and re.match(r"\d", part[1:]):
                        output += f"\\gl{{{part.lower()}}}"
                    else:
                        for gloss in resolve_glossing_combination(part):
                            output += decoration(gloss.lower())
                else:
                    output += part
        words_list[i] = output[1:]
    gloss_text_upcased = " ".join(words_list)
    return gloss_text_upcased

def render_sources(req, objid, table, session, ids=None, **kwargs):
    if "full" in kwargs:
        source = session.query(common.Source).filter(common.Source.id == objid)[0]
        return link(req, source, label=source.bibtex().text())
    return link_entity(
                        req,
                        objid,
                        "source",
                        common.Source,
                        session,
                    )


def render_ex(
    req, objid, table, session, ids=None, subexample=False, **kwargs
):  # pylint: disable=too-many-arguments
    if "subexample" in kwargs.get("format", []):
        subexample = True
    example_id = kwargs.get("example_id", [None])[0]
    title = kwargs.get("title", [None])[0]
    if objid == "__all__":
        if ids:
            ex_strs = [
                render_ex(req, mid, table, session, subexample=True)
                for mid in ids[0].split(",")
            ]
            return HTML.ol(
                HTML.li(
                    title,
                    HTML.ol(*ex_strs, class_="subexample"),
                    class_="example",
                    id_=example_id,
                ),
                class_="example",
            )
    sentence = session.query(Sentence).filter(Sentence.id == objid).first()
    if subexample:
        return rendered_sentence(
            req,
            sentence,
            sentence_link=True,
            counter_class="subexample",
            in_context=True,
        )
    return HTML.ol(
        rendered_sentence(
            req,
            sentence,
            sentence_link=True,
            in_context=True,
            example_id=example_id,
            counter_class="example",
            title=title,
        ),
        class_="example",
    )


def render_abbrev_list(req, objid, table, session, ids=None, **kwargs):
    abbrev_items = []
    for abbrev in session.query(common.GlossAbbreviation).all():
        abbrev_items.append(HTML.tr(HTML.td(abbrev.id), HTML.td(abbrev.name)))
    return HTML.table(HTML.tbody(*abbrev_items), **{"class": "table table-nonfluid"})

def includeme(config):

    config.registry.settings["mako.directories"].insert(
        1, "clld_document_plugin:templates"
    )
    config.registry.settings["clld_markdown_plugin"]["extensions"].extend(
        [
            TocExtension(permalink=False),
            "markdown.extensions.md_in_html",
            "markdown.extensions.attr_list",
            "markdown.extensions.footnotes",
            "pymdownx.tilde",
        ]
    )
    config.registry.settings["clld_markdown_plugin"]["renderer_map"][
        "ExampleTable"
    ] = render_ex
    config.registry.settings["clld_markdown_plugin"]["model_map"]["ChapterTable"] = {
        "route": "document",
        "model": models.Document,
    }

    config.registry.settings["clld_markdown_plugin"]["renderer_map"]["abbreviations.csv"] = render_abbrev_list

    config.registry.settings["clld_markdown_plugin"]["renderer_map"]["sources.bib"] = render_sources
    config.registry.settings["clld_markdown_plugin"]["renderer_map"]["Source"] = render_sources

    config.add_static_view("clld-document-plugin-static", "clld_document_plugin:static")

    config.register_resource(
        "document", models.Document, interfaces.IDocument, with_index=True
    )
    config.register_resource("topic", models.Topic, interfaces.ITopic, with_index=True)

    config.register_datatable("topics", datatables.Topics)
    config.register_datatable("documents", datatables.Documents)
