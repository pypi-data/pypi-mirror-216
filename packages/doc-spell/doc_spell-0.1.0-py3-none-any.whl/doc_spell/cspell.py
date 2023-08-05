"""
Retrieves human text from the code and pipes it via spell checker.

First, formatter collects all comments and doc strings. After that, it strips
tech text, and sends the rest to spell checker.

The tech text in comments could be:
 * code snippets
 * variable references, function names
 * technical comments, like `noqa`, `pylint`

"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments.formatter import Formatter
import subprocess as sp
import re
import sys
import os
import tempfile
from identify import identify
import logging
from pydevkit.log import prettify

log = logging.getLogger(__name__)


def repl(matchobj):
    txt = matchobj.group(0)
    return tr(txt)


def tr(txt):
    rc = ""
    for c in txt:
        if c.isspace():
            rc += c
        else:
            rc += " "
    return rc


class CodeFormatter(Formatter):
    """
    Retrieve human text from the code.

    The flow:
     1. collect all comments and doc strings
     2. strip tech text
         * fenced block - multi-line text between 3 back ticks, similar to
           `<pre>` tag
         * in-line code - text between back ticks, similar to `<code>`
         * special comment - e.g. `noqa`, `pylint`
         * custom regex - lines matching user-defined regex
    """

    # comment directive consists from 3 parts: header, command and value.
    # for example: `docspell: accept foo,bar`
    comment_prefix = "docspell"
    command_accept_len = 2

    def __init__(self, comment_delims, ignore_lines, **options):
        log.debug("%s init", self.__class__.__name__)
        log.debug("arg: comment_delims '%s'", comment_delims)
        log.debug("arg: ignore_lines '%s'", ignore_lines)
        log.debug("arg: options '%s'", options)
        Formatter.__init__(self, **options)
        self.comment_delims = comment_delims
        self.ignore_lines = ignore_lines
        self.spell_dict = []

    def format(self, tokensource, outfile):  # noqa: A003
        txt = self.tr_code(tokensource)
        txt = self.tr_comment_delims(txt)
        txt = self.tr_line(txt)
        txt = self.tr_directive(txt)
        txt = self.tr_md_code_block(txt)
        txt = self.tr_md_code(txt)
        outfile.write(txt)

    def tr_code(self, tokensource):
        tokens = []
        for ttype, value in tokensource:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug(
                    "token: type %s, value '%s'", ttype, value.replace("\n", "\\n")
                )
            if (
                ttype == Token.Comment
                or ttype == Token.Comment.Single
                or ttype == Token.Comment.Multiline
                or ttype == Token.Literal.String.Doc
            ):
                log.debug("token: accept")
                nv = value
            else:
                nv = tr(value)
            tokens.append(nv)
        return "".join(tokens)

    def tr_comment_delims(self, txt):
        if not self.comment_delims:
            return txt
        prefix_reg = [re.escape(i) for i in self.comment_delims]
        reg = "(?m)^[ \\t]*(" + "|".join(prefix_reg) + ")"
        return re.sub(reg, repl, txt)

    def tr_line(self, txt):
        if not self.ignore_lines:
            return txt
        line_reg = [re.escape(i) for i in self.ignore_lines]
        reg = "(?m)^[ \\t]*(" + "|".join(line_reg) + ")(\\W.*)?$"
        return re.sub(reg, repl, txt)

    def tr_directive(self, txt):
        line_reg = [re.escape(self.comment_prefix)]
        reg = "(?m)^[ \\t]*(" + "|".join(line_reg) + ")(\\W.*)?$"
        return re.sub(reg, self.mk_dict, txt)

    def mk_dict(self, matchobj):
        otxt = txt = matchobj.group(0)
        # rm leading '#'
        txt = txt.split(None, 1)[-1]
        txt = txt.split()
        log.debug("internal command: %s", txt)
        if len(txt) == self.command_accept_len and txt[0] == "accept":
            log.debug("accept words '%s'", txt[1])
            self.spell_dict += txt[1].split(",")
        return tr(otxt)

    def tr_md_code(self, txt):
        reg = "(?P<open>`+)[^`\\n]+?(?P=open)"
        return re.sub(reg, repl, txt)

    def tr_md_code_block(self, txt):
        reg_indent = "(?P<indent>^[ \\t]*)"
        reg = "(?m)" + reg_indent + "(?P<open>`{3,})[ \\t]*$\\n"
        reg += "((?P=indent).*$\\n)*?"
        reg += "(?P=indent)(?P=open)[ \\t]*$"
        return re.sub(reg, repl, txt)


def hunspell(code, path, conf, spell_dict):
    """
    Pipe code to `hunspell` and print errors in gcc format `file:line:column`.

    `spell_dict` is a personal dictionary. Is is loaded for the single run and
    not saved to disk.
    """
    tconf = conf.get("hunspell", {})
    log.debug("tconf: %s", prettify(tconf))

    # add personal word list
    dict_fp, dict_fname = tempfile.mkstemp(prefix="doc-spell-dict-")
    dict_fp = open(dict_fname, "w")

    def add_word_list(name, words):
        log.debug("add dictionary '%s'", name)
        for word in words:
            w = word.strip()
            if not w:
                continue
            log.debug("add word '%s'", w)
            dict_fp.write(w + "\n")

    add_word_list("inline", spell_dict)
    word_lists = tconf.get("wordlists", [])
    for wl in word_lists:
        try:
            words = open(wl, "r").readlines()
        except Exception as exp:
            log.error("%s", exp)
            continue
        add_word_list(wl, words)
    dict_fp.close()

    # save code for debugging
    code_fp, code_fname = tempfile.mkstemp(prefix="doc-spell-code-")
    code_fp = open(code_fname, "w")
    code_fp.write(code)
    code_fp.close()

    p = sp.Popen(
        ["hunspell", "-a", "-p", dict_fname],
        universal_newlines=True,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
    )

    # read one-line header
    p.stdout.readline()

    rc = True
    for no, line in enumerate(code.splitlines()):
        if line == "" or line.isspace():
            continue
        log.debug("line %d '%s'", no, line)
        for wm in re.finditer("\\b\\w+\\b", line):
            log.debug(">> %s", wm.group(0))
            # feed a line with one word
            p.stdin.write(wm.group(0) + "\n")
            p.stdin.flush()
            # read an answer for a word
            txt = p.stdout.readline().strip()
            # read an answer for a line
            p.stdout.readline()
            log.debug("<< '%s'", txt)
            if txt == "*":
                continue
            rc = False
            msg = "%s:%s:%s: %s" % (path, no + 1, wm.start(0), txt)
            print(msg, file=sys.stderr)

    if log.getEffectiveLevel() != logging.DEBUG:
        os.unlink(dict_fname)
        os.unlink(code_fname)
    else:
        log.debug("remove tmp code: %s", code_fname)
        log.debug("remove tmp dict: %s", dict_fname)
    return rc


# weights of lexer aliases, to find best match
aliases = {
    "shell": 1,
    "bash": 2,
    "c": 1,
    "c++": 2,
}


def get_lexer(tags, *, debug=False):
    log.debug("search for lexer")
    rc = (None, None)
    for tag in tags:
        try:
            lexer = get_lexer_by_name(tag, stripall=True)
        except Exception:
            lexer = None
        log.debug("tag %s, lexer %s", tag, lexer)
        if rc == (None, None):
            rc = (lexer, tag)
        if not debug:
            break
    return rc


def parse_rule(rule, comment_delims, ignore_lines):
    log.debug("matched rule %s", rule)
    err = "configuration error: rule '%s'" % rule["name"]

    def get_list(key, dst):
        tmp = rule.get(key, [])
        if tmp is None:
            return
        if not isinstance(tmp, list):
            log.error("%s: '%s' must be a list", err, key)
            sys.exit(1)
        dst += tmp

    get_list("comment-delims", comment_delims)
    get_list("ignore-lines", ignore_lines)


def get_formatter(conf, tags):
    comment_delims = []
    ignore_lines = []
    log.debug("search configuration for matching rules")
    for r in conf["rules"]:
        if r["tag"] in tags:
            parse_rule(r, comment_delims, ignore_lines)
    comment_delims = list(set(comment_delims))
    ignore_lines = list(set(ignore_lines))
    return CodeFormatter(comment_delims=comment_delims, ignore_lines=ignore_lines)


def spell_checker(path, conf):
    """
    Obtain human text from the code and pipe it via hunspell.

    In case of spelling errors, raises an exception.
    """
    log.info("check '%s'", path)
    tags = identify.tags_from_path(path)
    if "symlink" in tags:
        path = os.readlink(path)
        log.info("redirect to '%s'", path)
        tags = identify.tags_from_path(path)
    log.debug("identify %s", tags)
    accept = {"file", "text"}
    rc = accept - tags
    if len(rc):
        log.error("only text files are supported")
        msg = "%s: unsupported type %s" % (path, tags)
        raise Exception(msg)

    doc_types = {
        "html",
        "markdown",
        "xml",
        "qml",
        "rst",
        "xhtml",
        "pug",
        "jade",
        "scaml",
        "xslt",
    }
    rc = doc_types - tags
    if len(rc) != len(doc_types):
        log.error("only programming languages are supported, no markup")
        msg = "%s: unsupported type %s" % (path, tags)
        raise Exception(msg)

    tags = tags - accept
    tags = tags - {"executable", "non-executable", "plain-text"}
    tags = sorted(tags, key=lambda x: aliases.get(x, -1), reverse=True)
    log.debug("sorted tags %s", tags)
    lexer, tag = get_lexer(tags, debug=True)
    formatter = get_formatter(conf, tags)
    code = open(path, "r").read()
    code = highlight(code, lexer, formatter)
    if not hunspell(code, path, conf, formatter.spell_dict):
        msg = "spelling errors in '%s'" % path
        raise Exception(msg)
