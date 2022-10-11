#!/usr/bin/python3
# vim: set fileencoding=utf-8 :
#
# Copyright (C) 2014 Mattia Rizzolo <mattia@mapreri.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# On Debian systems, the complete text of the GNU General
# Public License can be found in `/usr/share/common-licenses/GPL-3'.


import os
import sys
import json
from re import search
from string import Template

json_list = 'list.json'

# note that both blacklisted_packages and languages listed at extra_pkg won't
# be auto-added, and thus need to be manually added to extra_pkg to be built

# binaries already in other sources, don't take them over (please sort!)
blacklisted_packages = [
 #   package        #    source
 "hunspell-an",     # hunspell-an
 "hunspell-ar",     # hunspell-ar
 "hunspell-be",     # hunspell-be
 "hunspell-bo",     # hunspell-bo
 "hunspell-br",     # hunspell-br
 "hunspell-ca",     # hunspell-ca
 "hunspell-en-au",  # scowl
 "hunspell-en-ca",  # scowl
 "hunspell-en-us",  # scowl
 "hunspell-et",     # ispell-et (bin:myspell-et provides it)
 "hunspell-fr",     # hunspell-fr
 "hunspell-lv",     # myspell-lv (myspell-lv binary)
 "hunspell-nl",     # dutch
 "hyphen-et",       # ispell-et (bin:myspell-et provides it)
 "hyphen-lv",       # myspell-lv (myspell-lv binary)
 "hyphen-pl",       # openoffice.org-hyphenation-pl
 "hyphen-ru",       # hyphen-ru
 "hyphen-te",       # hyphen-te
 "hunspell-sq",     # myspell-sq
 "mythes-de",       # openthesaurus
 "mythes-de-ch",    # openthesaurus
 "mythes-pl",       # openoffice.org-thesaurus-pl
]

provides = {
 "hyphen-en-gb": "hyphen-en-au, hyphen-en-za",
 "hunspell-kmr": "hunspell-ku",
}

breaks_replaces = {
 "hunspell-af": ("myspell-af", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-bg": ("myspell-bg", '<<', '4.1-5'),
 "hunspell-en-gb": ("myspell-en-gb", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-en-za": ("myspell-en-za", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-hr": ('myspell-hr', '<<', '1:6.0.3-2'),
 "hunspell-it": ("myspell-it", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-kmr": ('myspell-ku', '<<', '1:5.1.3-2'),
 "hunspell-lt": ('myspell-lt', '<<', '1.2.1-6'),
 "hunspell-pl": ('myspell-pl', '<<', '1:6.1.0~beta1-2'),
 "hunspell-pt-br": ('myspell-pt-br', '<=', '20131030-10'),
 "hunspell-pt-pt": ('myspell-pt-pt', '<=', '20091013-12'),
 "hunspell-ru": ("myspell-ru", '<=', "0.99g5-21"),
 "hunspell-sv": ("hunspell-sv-se",   '<<', "1:6.1.0~rc2-3"),
 "hunspell-sw": ("myspell-sw", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-th": ("myspell-th", '<<', "1:5.0.1+dfsg-1"),
 "hunspell-sl": ("myspell-sl", '<=', "1.0-5"),
 "hyphen-lt": ('openoffice.org-hyphenation-lt', '<<', '1.2.1-6'),
}

conflicts = {
 "hunspell-cs": "myspell-cs",
 "hunspell-da": "myspell-da",
 "hunspell-el": "myspell-el-gr",
 "hunspell-en-au": "myspell-en-au",
 "hunspell-es": "myspell-es",
 "hunspell-et": "myspell-et",
 "hunspell-gd": "myspell-gd",
 "hunspell-he": "myspell-he",
 "hunspell-hu": "myspell-hu",
 "hunspell-nl": "myspell-nl",
 "hunspell-no": "myspell-nb, myspell-nn",
 "hunspell-sk": "myspell-sk",
 "hunspell-uk": "myspell-uk",
 "hyphen-et": "myspell-et",
 "hyphen-no": "myspell-nb, myspell-nn",
}

# special packages, that do not follow the common logic
extra_pkg = [
 {"639-1": "de", "code": "de-at-frami",
  "name": "German (Austria)",
  "hunspell": ["de_AT_frami.aff", "de_AT_frami.dic"],
  "special": """Conflicts: myspell-de-at, hunspell-de-at
Description: German (Austria) dictionary for hunspell ("frami" version)
 This is the German (Austria) dictionary for use with the hunspell
 spellchecker.
 .
 This package contains a enhanced version by Franz Michael Baumann with
 some words missing in the base dictionary or not (yet) belonging to the
 "core" German words.
 .
 Hunspell is a spell checker and morphological analyzer library and program
 designed for languages with rich morphology and complex word compounding or
 character encoding. It is based on MySpell and features an Ispell-like
 terminal interface using Curses library, an Ispell pipe interface and a
 LibreOffice UNO module.
"""},
 {"639-1": "de", "code": "de-ch-frami",
  "name": "German (Switzerland)",
  "hunspell": ["de_CH_frami.aff", "de_CH_frami.dic"],
  "special": """Conflicts: myspell-de-ch, hunspell-de-ch
Description: German (Switzerland) dictionary for hunspell ("frami" version)
 This is the German (Switzerland) dictionary for use with the hunspell
 spellchecker.
 .
 This package contains a enhanced version by Franz Michael Baumann with
 some words missing in the base dictionary or not (yet) belonging to the
 "core" German words.
 .
 Hunspell is a spell checker and morphological analyzer library and program
 designed for languages with rich morphology and complex word compounding or
 character encoding. It is based on MySpell and features an Ispell-like
 terminal interface using Curses library, an Ispell pipe interface and a
 LibreOffice UNO module.
"""},
 {"639-1": "de", "code": "de-de-frami",
  "hunspell": ["de_DE_frami.aff", "de_DE_frami.dic"], "name": "German",
  "special": """Conflicts: myspell-de-de, hunspell-de-de
Description: German dictionary for hunspell ("frami" version)
 This is the German (Belgium, Germany, Luxemburg) dictionary for use with the
 hunspell spellchecker.
 .
 This package contains a enhanced version by Franz Michael Baumann with
 some words missing in the base dictionary or not (yet) belonging to the
 "core" German words.
 .
 Hunspell is a spell checker and morphological analyzer library and program
 designed for languages with rich morphology and complex word compounding or
 character encoding. It is based on MySpell and features an Ispell-like
 terminal interface using Curses library, an Ispell pipe interface and a
 LibreOffice UNO module.
"""},
 {"639-1": "de", "code": "de", "name": "German",
  "hyphen": ["hyph_de_DE.dic"]},
 {"639-1": "en", "code": "en-za", "name": "English (South Africa)",
  "hunspell": ["en_ZA.aff", "en_ZA.dic"]},
 {"639-1": "en", "code": "en-us", "name": "English (USA)",
  "mythes": ["th_en_US_v2.dat", "th_en_US_v2.idx"]},
 {"639-1": "en", "code": "en-gb", "name": "English (GB)",
  "hunspell": ["en_GB.aff", "en_GB.dic"], "hyphen": ['hyph_en_GB.dic']},
 {"639-1": "cs_CZ", "code": "cs", "name": "Czech",
  "mythes": ["thes_cs_CZ.dat", "thes_cs_CZ.idx"]},
]

# Code lookup: https://en.wikipedia.org/wiki/ISO_639:$code

# link the pseudo-RFC639-1 used by upstream (the key) to an actual RFC639-1 or RFC638-2
ass_639_code = {"af_ZA": "af", "an_ES": "an", "ar": "ar", "be_BY": "be", "bg_BG": "bg", "bn_BD": "bn", "bo": "bo", "br_FR": "br", "bs_BA": "bs", "ca": "ca", "cs_CZ": "cs", "da_DK": "da", "de": "de", "el_GR": "el", "en": "en", "es": "es", "et_EE": "et", "fr_FR": "fr", "gd_GB": "gd", "gl": "gl", "gu_IN": "gu", "gug": "gug", "he_IL": "he", "hi_IN": "hi", "hr_HR": "hr", "hu_HU": "hu", "id": "id", "is": "is", "it_IT": "it", "kmr_Latn": "kmr", "lo_LA": "lo", "lt_LT": "lt", "lv_LV": "lv", "mn_MN": "mn", "ne_NP": "ne", "nl_NL": "nl", "no": "no", "oc_FR": "oc", "pl_PL": "pl", "pt_BR": "pt-br", "pt_PT": "pt-pt", "ro": "ro", "ru_RU": "ru", "si_LK": "si", "sk_SK": "sk", "sl_SI": "sl", "sq_AL": "sq", "sr": "sr", "sv_SE": "sv", "sw_TZ": "sw", "te_IN": "te", "th_TH": "th", "tr_TR": "tr", "uk_UA": "uk", "vi": "vi", "zu_ZA": "zu"}

# link the pseudo-RFC639-1 used by upstream (the key) to a language name
ass_639_name = {"af_ZA": "Afrikaans", "an_ES": "Aragonese", "ar": "Arabic", "be_BY": "Belarusian", "bg_BG": "Bulgarian", "bn_BD": "Bengali", "bo": "Classic Tibetan", "br_FR": "Breton", "bs_BA": "Bosnian", "ca": "Catalan", "cs_CZ": "Czech", "da_DK": "Danish", "de": "German", "el_GR": "Modern Greek", "en": "English", "es": "Spanish", "et_EE": "Estonian", "fr_FR": "French", "gd_GB": "Scottish Gaelic", "gl": "Galician", "gu_IN": "Gujarati", "gug": "Guarani", "he_IL": "Hebrew", "hi_IN": "Hindi", "hr_HR": "Croatian", "hu_HU": "Hungarian", "id": "Indonesian", "is": "Icelandic", "it_IT": "Italian", "kmr_Latn": "Kurmanji", "lo_LA": "Laotian", "lt_LT": "Lithuanian", "lv_LV": "Latvian", "mn_MN": "Mongolian", "ne_NP": "Nepalese", "nl_NL": "Dutch", "no": "Norwegian", "oc_FR": "Occitan", "pl_PL": "Polish", "pt_BR": "Brazilian Portuguese", "pt_PT": "Portuguese", "ro": "Romanian", "ru_RU": "Russian", "si_LK": "Sinhala", "sk_SK": "Slovak", "sl_SI": "Slovene", "sq_AL": "Albanian", "sr": "Serbian", "sv_SE": "Swedish", "sw_TZ": "Swahili", "te_IN": "Telugu", "th_TH": "Thai", "tr_TR": "Turkish", "uk_UA": "Ukrainian", "vi": "Vietnamese", "zu_ZA": "Zulu"}

hyphen_tpl = Template("""
Package: hyphen-$language_639
Architecture: all
Multi-Arch: foreign
Depends: dictionaries-common, $${misc:Depends}
Suggests: libreoffice-writer
Provides: hyphen-hyphenation-patterns, hyphen-hyphenation-patterns-${language_639}${more_provides}
${breaks}${conflicts}Description: $language_name hyphenation patterns
 This package contains the $language_name hyphenation patterns.
 .
 You can use these patterns with programs which take advantage of libhyphen,
 like LibreOffice.
""")
hunspell_tpl = Template("""
Package: hunspell-$language_639
Architecture: all
Multi-Arch: foreign
Depends: dictionaries-common, $${misc:Depends}, $${hunspell:Depends}
Suggests: hunspell, libreoffice-writer
Provides: hunspell-dictionary, hunspell-dictionary-$language_639${more_provides}
${breaks}${conflicts}""")
hunspell_desc_tpl = Template(
 """Description: $language_name dictionary for hunspell
 This is the $language_name dictionary for use with the hunspell
 spellchecker.
 .
 Hunspell is a spell checker and morphological analyzer library and program
 designed for languages with rich morphology and complex word compounding or
 character encoding. It is based on MySpell and features an Ispell-like
 terminal interface using Curses library, an Ispell pipe interface and a
 LibreOffice UNO module.
""")
mythes_tpl = Template("""
Package: mythes-$language_639
Architecture: all
Multi-Arch: foreign
Depends: dictionaries-common, $${misc:Depends}
Suggests: libreoffice-writer
Provides: mythes-thesaurus, mythes-thesaurus-${language_639}
Description: $language_name Thesaurus for LibreOffice
 Libreoffice is a full-featured office productivity suite that provides a
 near drop-in replacement for Microsoft(R) Office.
 .
 This package contains the $language_name thesaurus for LibreOffice.
""")


def _add_list_to_dict(a_dict, index, item):
    try:
        a_list = a_dict[index]
    except KeyError:
        a_list = []
    a_list.append(item)
    a_dict[index] = sorted(a_list)
    return a_dict


def _read_list():
    try:
        with open(json_list, "r") as fd:
            return json.load(fd)
    except FileNotFoundError:
        print('%s not found, please run this script from inside the debian '
              'directory or compile a %s file if you already are.' %
              (json_list, json_list))
        sys.exit(1)


def generate_json():
    basepath = '../dictionaries'
    lsdir = []
    dictionaries = []
    try:
        ls = os.listdir(basepath)
    except FileNotFoundError:
        print('Please run this script from inside the debian directory.')
        sys.exit(1)
    for item in ls:
        if os.path.isdir(basepath + '/' + item):
            lsdir.append(item)
    for item in lsdir:
        if item in ['util', 'de', 'en']:  # the de and en are in extra_pkg
            continue
        itemd = {}
        itemd['639-1'] = item
        itemd['code'] = ass_639_code[item]
        itemd['name'] = ass_639_name[item]
        lslang = os.listdir(basepath + '/' + item)
        for i in lslang:
            if i == "dictionaries" and \
                    os.path.isdir(basepath + '/' + item + '/' + i):
                lslang += os.listdir(basepath + '/' + item + '/' + i)
        for i in lslang:
            if itemd['code'] == 'ca':
                filename = 'dictionaries/' + i
            else:
                filename = i
            if search(r'hyph_.*\.dic', i):
                _add_list_to_dict(itemd, 'hyphen', filename)
            if search(r'.*\.dic', i) and not search('hyph.*', i) \
                    and not search('.*frami.*', i):
                _add_list_to_dict(itemd, 'hunspell', filename)
            if search(r'.*\.aff', i) and not search('.*frami.*', i):
                _add_list_to_dict(itemd, 'hunspell', filename)
            if search(r'.*\.dat', i):
                if itemd['639-1'] == 'cs_CZ':
                    continue
                _add_list_to_dict(itemd, 'mythes', filename)
                idxfile = os.path.splitext(filename)[0] + '.idx'
                _add_list_to_dict(itemd, 'mythes', idxfile)
        dictionaries.append(itemd)
    dictionaries += extra_pkg
    dictionaries = sorted(dictionaries, key=lambda k: k['639-1'])
    with open(json_list, 'w') as fd:
        json.dump(dictionaries, fd, sort_keys=True,  indent=4)
        fd.write('\n')
    print("json file written to " + json_list)


def generate_control():
    control = """# Automatically generated.  DO NOT EDIT!
# Edit debian/control.in and debian/helper.py instead.
# Run `./helper.py control` to regenerate this.
"""
    try:
        with open('control.in', 'r') as fd:
            control += fd.read()
    except FileNotFoundError:
        print('control.in not found.  Please run this script from inside the '
              'debian directory.')
        sys.exit(1)
    lang_list = _read_list()
    for item in lang_list:
        if 'hyphen' in item:
            pkg_name = 'hyphen-' + item['code']
            if pkg_name in blacklisted_packages:
                pass
            else:
                co = ''
                pro = ''
                br = ''
                if pkg_name in breaks_replaces:
                    br = 'Breaks: {0} ({1} {2})\nReplaces: {0} ({1} {2})\n'
                    br = br.format(*breaks_replaces[pkg_name])
                if pkg_name in conflicts:
                    co = 'Conflicts: {}\n'.format(conflicts[pkg_name])
                if pkg_name in provides:
                    pro = ', %s' % provides[pkg_name]
                control += hyphen_tpl.substitute(language_639=item['code'],
                                                 language_name=item['name'],
                                                 more_provides=pro,
                                                 breaks=br,
                                                 conflicts=co)
        if 'hunspell' in item:
            pkg_name = 'hunspell-' + item['code']
            if pkg_name in blacklisted_packages:
                pass
            else:
                br = ''
                if pkg_name in breaks_replaces:
                    br = 'Breaks: {0} ({1} {2})\nReplaces: {0} ({1} {2})\n'
                    br = br.format(*breaks_replaces[pkg_name])
                co = ''
                if pkg_name in conflicts:
                    co = 'Conflicts: {}\n'.format(conflicts[pkg_name])
                pro = ''
                if pkg_name in provides:
                    pro = ', %s' % provides[pkg_name]
                control += hunspell_tpl.substitute(language_639=item['code'],
                                                   more_provides=pro,
                                                   breaks=br, conflicts=co)
                if 'special' in item:
                    control += item['special']
                else:
                    control += hunspell_desc_tpl.substitute(language_name=item['name'])
        if 'mythes' in item:
            if 'mythes-' + item['code'] in blacklisted_packages:
                pass
            else:
                control += mythes_tpl.substitute(language_639=item['code'],
                                                 language_name=item['name'])
    with open('control', 'w') as fd:
        fd.write(control)
    print("debian/control file created")


def generate_installs():
    lang_list = _read_list()
    rows = []
    for item in lang_list:
        langcode = item['code']
        for key in ['hunspell', 'hyphen', 'mythes']:
            package = '{}-{}'.format(key, langcode)
            if package in blacklisted_packages:
                continue
            try:
                for i in item[key]:
                    f = 'dictionaries/' + item['639-1'] + '/' + i + ' '
                    rows.append((
                        'dh_install',
                        '-p{}'.format(package),
                        f,
                        'usr/share/{}'.format(key),
                    ))
            except KeyError:
                pass
            text = [
                '# vi: ft=make\n',
                '#\n',
                '# AUTOGENERATED FILE, DO NOT EDIT HERE!\n',
                '\n',
                'install_files:\n',
            ]
            for row in rows:
                text.append('\t{}\n'.format(' '.join(row)))
            with open('rules.install', 'w') as fd:
                fd.writelines(text)
    print("rules.install file created.")


try:
    if sys.argv[1] == "json":
        generate_json()
    elif sys.argv[1] == "control":
        generate_control()
    elif sys.argv[1] == "install":
        generate_installs()
except IndexError:
    generate_control()
    generate_installs()
