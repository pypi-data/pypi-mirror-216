"""
======================COPYRIGHT/LICENSE START==========================

Util.py: Useful functions for scripts in this directory and its subdirectories

Copyright (C) 2005-2008 Wim Vranken (European Bioinformatics Institute)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../../license/LGPL.license

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


======================COPYRIGHT/LICENSE END============================

for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)
- PDBe website (http://www.ebi.ac.uk/pdbe/)

- contact Wim Vranken (wim@ebi.ac.uk)
=======================================================================

If you are using this software for academic purposes, we suggest
quoting the following references:

===========================REFERENCE START=============================
R. Fogh, J. Ionides, E. Ulrich, W. Boucher, W. Vranken, J.P. Linge, M.
Habeck, W. Rieping, T.N. Bhat, J. Westbrook, K. Henrick, G. Gilliland,
H. Berman, J. Thornton, M. Nilges, J. Markley and E. Laue (2002). The
CCPN project: An interim report on a data model for the NMR community
(Progress report). Nature Struct. Biol. 9, 416-418.

Wim F. Vranken, Wayne Boucher, Tim J. Stevens, Rasmus
H. Fogh, Anne Pajon, Miguel Llinas, Eldon L. Ulrich, John L. Markley, John
Ionides and Ernest D. Laue (2005). The CCPN Data Model for NMR Spectroscopy:
Development of a Software Pipeline. Proteins 59, 687 - 696.

===========================REFERENCE END===============================
"""

import re
from b2bTools.general.ccpn.format.general.Constants import defaultSeqInsertCode

# characters that can be used as a one-digit index
indexChars = '123456789'

#######################
# Regular expressions #
#######################

def getRegularExpressions(format = None):

  patt = {}

  patt['emptyline'] = re.compile(r"^\s*$")
  patt['hash'] = re.compile(r"^\s*\#")
  patt['exclamation'] = re.compile(r"^\s*\!")
  patt['underscore'] = re.compile(r"^\s*\_")
  patt['colon'] = re.compile(r":")
  patt['onlyDollar'] = re.compile(r"^\$$")
  patt['onlydigit'] = re.compile(r"^\d+$")
  patt['onlyFloat'] = re.compile(r"^\d+\.\d+$")
  patt['bracketEither'] = re.compile(r"\(|\)")
  patt['bracketOpen'] = re.compile(r"\s*\(")
  patt['bracketClose'] = re.compile(r"\)")
  patt['nucleusLetterDigit'] = re.compile(r"^([A-Za-z])(\d+)")
  patt['seqInsertCode'] = re.compile(r"^([A-Za-z]*)(\d+)([A-Za-z]*)")
  patt['anySpace'] = re.compile(r"\s")

  if format == 'amber':

    patt[format + 'RestraintStart'] = re.compile(r"(\&rst)")
    patt[format + 'RestraintEnd'] = re.compile(r"(\&end)")

  elif format == 'ansig':

    patt[format + 'CurlyBrace'] = re.compile(r"\{(.*)\}")

  elif format == 'auremol':

    patt[format + 'Section'] = re.compile(r"^\s*section_(.+)$")
    patt[format + 'SubSection'] = re.compile(r"^\s*([A-Z_]+)\:")

  elif format == 'autoAssign':
    patt[format + 'specPhase'] = re.compile(r"phase:\s*\{(.*)\}\s*\{\s*$")
    patt[format + 'onlyCurlyBraceEnd'] = re.compile(r"^\}$")
    patt[format + 'CurlyBrace'] = re.compile(r"\{\s*(.*)\s*\}")
    patt[format + 'seqCode1Or3LetterAndCode'] = re.compile(r"([A-Z][a-z]{0,2})(\d+)")
    patt[format + 'spinSystemInfo'] = re.compile(r".+(\(.+\))")

  elif format == 'aqua':
    patt[format + 'Count'] = re.compile(r"^count (\d+) type (.+)$")
    patt[format + 'UpperDistance'] = re.compile(r"^NOEUPP")
    patt[format + 'LowerDistance'] = re.compile(r"^NOELOW")
    patt[format + 'EndComment']    = re.compile(r"\#(.+)$")

  elif format == 'bruker':
    patt[format + 'StartDoubleHash'] = re.compile(r"^\#\#")
    patt[format + 'StartDoubleHashDollar'] = re.compile(r"^\#\#\$")
    patt[format + 'StartDoubleDollar'] = re.compile(r"^\$\$")
    patt[format + 'SharpBracketOpen'] = re.compile(r"^\<")
    patt[format + 'SharpBracketClose'] = re.compile(r"\>$")
    patt[format + 'SharpBracketEither'] = re.compile(r"\<|\>")
    patt[format + 'BracketsListIndicator'] = re.compile(r"\(\d+\.\.\d+\)")
    patt[format + 'Date'] = re.compile(r"2\d\d\d-\d\d-\d\d")
    patt[format + 'DigitDotDigit'] = re.compile(r"^\-?\d*\.?\d+$")
    patt[format + 'Dot'] = re.compile(r"\.")
    patt[format + 'BracketCloseNumber'] = re.compile(r"\)\s*\d")
    patt[format + 'FinalReturn'] = re.compile(r"\n$")
    patt[format + 'BracketMultiValue'] = re.compile(r"\((\d+)\-(\d+)\)")
    patt[format + 'InOrDecrement'] = re.compile(r"\s*(i|d)d(\d+)")
    patt[format + 'HashComment'] = re.compile(r"^\s*\#(.+)")
    patt[format + 'SemiColonComment'] = re.compile(r"^\s*\;(.*)")
    patt[format + 'PulseName'] = re.compile(r"\/([^\/]+)\"")
    patt[format + 'FnMode'] = re.compile(r"FnMode?\s*(.+)\s*", re.I)
    patt[format + 'EchoAntiEcho'] = re.compile(r"igrad|\*EA", re.I)
    patt[format + 'PathwayElements'] = re.compile(r"(F\d+)\s*\(([^\)]+)\)")
    patt[format + 'DimIncrement'] = re.compile(r"in(\d+)\s*\=\s*inf(\d+)\s*\\s*/\s*(\d+)")
    patt[format + 'phaseSensitive'] = re.compile(r"\;\s*phase sensitive")
    patt[format + 'constantTime'] = re.compile(r"constant time")
    patt[format + 'semiconstantTime'] = re.compile(r"semi-constant time")
    patt[format + 'tSearch'] = re.compile(r"(t\d)")
    patt[format + 'Version'] = re.compile(r"Version\s*(\d+\.*\d*)")

  elif format == 'charmm':

    patt[format + 'NumberAtoms'] = re.compile(r"^\s*(\d+)\s*$")
    patt[format + 'AtomLine'] = re.compile(r"^\s*\d+\s+\d+\s+[A-Za-z]+\s+")

  # This is for CNS/xplor
  elif format == 'cns':

    patt[format + 'DistancePeakInfoLine'] = re.compile(r"peak",re.IGNORECASE)
    patt[format + 'MultiSign'] = re.compile(r"[\%\#\*\+]")
    patt[format + 'RestrNum'] = re.compile(r"\{\s*(\-?\d+)\s*\}")
    patt[format + 'Assign'] = re.compile(r"assi",re.IGNORECASE)
    patt[format + 'AssignOr'] = re.compile(r"or",re.IGNORECASE)
    patt[format + 'ChemShiftFormat'] = re.compile(r"attr\s+store",re.IGNORECASE)
    patt[format + 'ChemShiftStore'] = re.compile(r"do.+store\d+\s*\=\s*(\-?\d*\.?\d*)\s*\)",re.IGNORECASE)
    patt[format + 'ChainCode'] = re.compile(r"segid\s+(\"([A-Za-z0-9 ]+)\"|([A-Za-z0-9]+))\s*",re.IGNORECASE)
    patt[format + 'Class'] = re.compile(r"class\s+",re.IGNORECASE)
    patt[format + 'SeqCode'] = re.compile(r"resid?u?e?\s+(\-?\d+[a-zA-Z]?)\s*",re.IGNORECASE)
    patt[format + 'AtomName'] = re.compile(r"name\s+([A-Z0-9\%\#\*\+]+\'?)",re.IGNORECASE)
    patt[format + 'RestrDistances'] = re.compile(r"([\d\.]+)\s+(-?[\d\.]+)\s+(-?[\d\.?]+)")
    patt[format + 'RestrAngles'] = re.compile(r"(\d+\.?\d*)\s+(-?\+?\d+\.?\d*)\s+(\+?\d+\.?\d*)\s+(\d)")
    patt[format + 'RestrCoupling'] = re.compile(r"(\d+\.?\d*)\s+(\d+\.?\d*)")
    patt[format + 'RestrCsa'] = re.compile(r"(-?\d+\.?\d*)\s+(\d+\.?\d*)\s*(\d+\.?\d*)?")
    patt[format + 'RestrRdc'] = re.compile(r"(-?\d+\.?\d*)\s+(\d+\.?\d*)\s*(\d+\.?\d*)?")
    patt[format + 'RestrInnerOr'] = re.compile(r"\s*or",re.IGNORECASE)
    patt[format + 'InnerElementPatt'] = re.compile(r"\(([^\)\(]+)\)",re.M)
    patt[format + 'LongCommentStart'] = re.compile(r"\{")
    patt[format + 'LongCommentEnd'] = re.compile(r"\}")

  elif format == 'csi':

    patt[format + 'Comment'] = re.compile(r"^\s*\>")

  elif format in ['dyana','cyana']:

    patt[format + 'CoordinateInfoLine'] = re.compile(r"\s*\d+\s+[A-Z0-9]+\s+\d+\s+")
    patt[format + 'CoordinateAtomLine'] = re.compile(r"^ATOM|^HETATM")
    patt[format + 'NewModel'] = re.compile(r"^MODEL\s+(\d+)")

  elif format == 'mars':

    patt[format + 'AtomNameHeader'] = re.compile(r"^\s*([\sNCHABO\-1])+\s*$")
    patt[format + 'AtomInfo'] = re.compile(r"([A-Z]+)(\-\d)?")

  elif format == 'mol':

    patt[format + 'Counts'] = re.compile(r"^([0-9 ][0-9 ][0-9]){6}")
    patt[format + 'Atoms'] = re.compile(r"^([0-9\- ][0-9\- ][0-9\- ][0-9\- ][0-9]\.[0-9][0-9 ][0-9 ][0-9 ]){3}")
    patt[format + 'Bonds'] = re.compile(r"^([0-9 ][0-9 ][0-9]){4}([0-9 ][0-9 ][0-9 ])([0-9 ][0-9 ][0-9])")

  elif format == 'mol2':

    patt[format + 'TriposTag'] = re.compile(r"\@\<TRIPOS\>(.+)")

  elif format == 'monte':

    patt[format + 'Comment'] = re.compile(r"^\s*(\#\#|\%\%)")
    patt[format + 'Assignment'] = re.compile(r"([A-Za-z]+)?([0-9]+|\?)?")
    patt[format + 'AtomInfo'] = re.compile(r"([A-Za-z0-9]+)(\(.+\)|\-1)?")

  elif format in ['nmrDraw','talos']:

    patt[format + 'Remark'] = re.compile(r"^REMARK")
    patt[format + 'Dataline'] = re.compile(r"^DATA")
    patt[format + 'Vars'] = re.compile(r"^VARS")
    patt[format + 'Format'] = re.compile(r"^FORMAT")

  elif format == 'nmrView':

    patt[format + 'DigitSpace'] = re.compile(r"^\d+\s+")
    patt[format + 'CurlyBrace'] = re.compile(r"\{([^{}]*)\}")
    patt[format + 'CurlyBraceStart'] = re.compile(r"\{")
    patt[format + 'CurlyBraceEnd'] = re.compile(r"\}\s+")
    patt[format + 'NumbersNoBrace'] = re.compile(r"^(\d+\.\d+\s*){2}")

  elif format == 'nmrStar':

    patt[format + 'EndSaveTag'] = re.compile(r"save_$")

  elif format == 'pdb':

    patt[format + 'NewModel'] = re.compile(r"^MODEL\s+(\d+)")
    patt[format + 'AllAtom'] = re.compile(r"^ATOM|^HETATM")
    patt[format + 'HetAtom'] = re.compile(r"^HETATM")
    patt[format + 'Header'] = re.compile(r"^HEADER")
    patt[format + 'Title'] = re.compile(r"^TITLE")
    patt[format + 'Remark4'] = re.compile(r"^REMARK   4 ([a-zA-Z0-9]{4}) COMPLIES WITH FORMAT V.\s*(\d+\.\d+)\s*\,")
    patt[format + 'Compound'] = re.compile(r"^COMPND\s+\d*\s+")
    patt[format + 'DbReference'] = re.compile(r"^DBREF")
    patt[format + 'SequenceChange'] = re.compile(r"^SEQADV")
    patt[format + 'Sequence'] = re.compile(r"^SEQRES")
    patt[format + 'Source'] = re.compile(r"^SOURCE\s+\d*\s+(.+)")
    patt[format + 'Keywds'] = re.compile(r"^KEYWDS\s+\d*\s+(.+)")
    patt[format + 'ExpData'] = re.compile(r"^EXPDATA\s+\d*\s+(.+)")
    patt[format + 'Authors'] = re.compile(r"^AUTHOR\s+\d*\s+(.+)")
    patt[format + 'Journal'] = re.compile(r"^JRNL\s+(AUTH|TITL|REF|REFN|PUBL|EDIT)\s+\d*\s+(.+)")
    patt[format + 'Reference'] = re.compile(r"^REFERENCE\s+(\d+)")
    patt[format + 'ReferenceJournal'] = re.compile(r"\s*(AUTH|TITL|REF|REFN|PUBL|EDIT)\s+\d*\s+(.+)")
    patt[format + 'Remarks'] = re.compile(r"^REMARK\s+(\d+)\s+(.+)")
    patt[format + 'HetGroup'] = re.compile(r"^HET\s+")
    patt[format + 'HetName'] = re.compile(r"^HETNAM")
    patt[format + 'HetSynonym'] = re.compile(r"^HETSYN")
    patt[format + 'HetFormula'] = re.compile(r"^FORMUL")
    patt[format + 'Bonds'] = re.compile(r"^CONECT")
    patt[format + 'SsBond'] = re.compile(r"^SSBOND")
    patt[format + 'Link'] = re.compile(r"^LINK")
    patt[format + 'SecStruc'] = re.compile(r"^(HELIX|TURN|SHEET)")
    patt[format + 'Termination'] = re.compile(r"^TER ")

  elif format == 'pipp':
    patt[format + '?_AXIS'] = re.compile(r"^(.+)_AXIS")
    patt[format + 'Shift'] = re.compile(r"^\s*(.+)\s+([0-9]*\.?[0-9]+)\s+\((.+)\)\s*$")
    patt[format + 'ShiftNoAss'] = re.compile(r"^\s*(.+)\s+([0-9]*\.?[0-9]+)\s*$")

  elif format == 'pistachio':
    patt[format + 'Comment'] = re.compile(r"^\s*\%.+")

  elif format == 'sparky':
    patt[format + 'SharpBracketBetween'] = re.compile(r"^\<(.+)\>$")
    patt[format + 'LabelCodeName'] = re.compile(r"([A-Z]?)((\d+\,?)+)(.+)")
    patt[format + 'BracketBetween'] = re.compile(r"\((.+)\)")

  # Addition Maxim Mayzel, Gothenburg
  elif format == 'targetedAcquisition':
    patt[format + 'seqCode1Or1LetterAndCode'] = re.compile(r"([A-Z])(\d+)")
    patt[format + 'figOfMerit'] = re.compile(r"([B|G|M])\s*(\d+\.*\d*)")

  elif format == 'xeasy':
    patt[format + 'IName'] = re.compile(r"^\#\s*INAME\s+(\d)\s*(.+)$")
    patt[format + 'CyanaFormat'] = re.compile(r"^\#\s*CYANAFORMAT\s+(.+)\s*$")
    patt[format + 'PeakInfo'] = re.compile(r"^\s*([^#]+)\s*\#?.*$")

  return patt

patt = getRegularExpressions()

def getSeqAndInsertCode(seqCode):

  seqInsertCode = defaultSeqInsertCode

  if seqCode != None:
    try:
      seqCode = int(seqCode)
    except:
      searchObj = patt['seqInsertCode'].search(str(seqCode))
      if searchObj:
        try:
          seqCode = int(searchObj.group(2))
          if searchObj.group(1) or searchObj.group(3):
            seqInsertCode = searchObj.group(1) + searchObj.group(3)

        except:
          seqCode = None
      else:
        seqCode = None

  return (seqCode,seqInsertCode)

def standardNucleusName(name):

  if (not name):
    name = '1H'
  elif ((name[0].upper() == 'H') or (name.upper() == '1H')):
    name = '1H'
  elif ((name[0].upper() == 'C') or (name.upper() == '13C')):
    name = '13C'
  elif ((name[0].upper() == 'N') or (name.upper() == '15N')):
    name = '15N'
  elif ((name[0].upper() == 'P') or (name.upper() == '31P')):
    name = '31P'
  else:
    name = '1H'

  return name

