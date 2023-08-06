from b2bTools.singleSeq.DynaMine.Predictor import DynaMine
from b2bTools.singleSeq.EFoldMine.Predictor import EFoldMine
from b2bTools.singleSeq.DisoMine.Predictor import DisoMine
from b2bTools.singleSeq.Agmata.Predictor import Agmata
from b2bTools.singleSeq.PSPer.Predictor import PSPer
from b2bTools.singleSeq import constants
from b2bTools.general.Io import B2bIo

# TODO: Here access all predictions, or at least those asked for!

class MineSuite(B2bIo):

  scriptName = "b2bTools.singleSeq.Predictor"

  def __init__(self):
    self._dynaMine = None
    self._eFoldMine = None
    self._disoMine = None
    self._agmata = None
    self._psper = None

    # Additional info for writing files
    self._infoTexts = None
    self._references = None
    self._version = None
    self._informationPerPredictor = None

    #self.references = ['doi: 10.1038/ncomms3741 (2013)', 'doi: 10.1093/nar/gku270 (2014)', 'doi: 10.1038/s41598-017-08366-3 (2017)']

  @property
  def dynaMine(self):
    if not self._dynaMine:
      self._dynaMine = DynaMine()

    return self._dynaMine

  @property
  def eFoldMine(self):
    if not self._eFoldMine:
      self._eFoldMine = EFoldMine(dynaMine=self.dynaMine)
    return self._eFoldMine

  @property
  def disoMine(self):
    if not self._disoMine:
      self._disoMine = DisoMine()
    return self._disoMine

  @property
  def agmata(self):
    if not self._agmata:
      self._agmata = Agmata()
    return self._agmata

  @property
  def psper(self):
    if not self._psper:
      self._psper = PSPer()
    return self._psper

  @property
  def infoTexts(self):
    if not self._infoTexts:
      self._infoTexts = list(
        set(
          self.dynaMine.infoTexts +
          self.eFoldMine.infoTexts +
          self.disoMine.infoTexts +
          self.agmata.infoTexts +
          self.psper.infoTexts
        )
      )
      self._infoTexts.sort()

    return self._infoTexts

  @property
  def references(self):
    if not self._references:
      self._references = list(
        set(
          self.dynaMine.references +
          self.eFoldMine.references +
          self.disoMine.references +
          self.agmata.references +
          self.psper.references
        )
      )
      self._references.sort()

    return self._references

  @property
  def version(self):
    if not self._version:
      self._version = "DynaMine {}, EFoldMine {}, DisoMine {}, Agmata {}. PSPer {}".format(
        self.dynaMine.version,
        self.eFoldMine.version,
        self.disoMine.version,
        self.agmata.version,
        self.psper.version
      )

    return self._version

  @property
  def informationPerPredictor(self):
    if not self._informationPerPredictor:
      self._informationPerPredictor = self.dynaMine.informationPerPredictor.copy()
      self._informationPerPredictor.update(self.eFoldMine.informationPerPredictor)
      self._informationPerPredictor.update(self.disoMine.informationPerPredictor)
      self._informationPerPredictor.update(self.agmata.informationPerPredictor)
      self._informationPerPredictor.update(self.psper.informationPerPredictor)

    return self._informationPerPredictor

  def predictSeqs(self, seqs, predTypes = (constants.TOOL_EFOLDMINE, constants.TOOL_DISOMINE, constants.TOOL_AGMATA)):

    """
    :param seqs: A list of sequence ID and sequence pairs, e.g. ('mySeq', 'MYPEPTIDE')
    :param predTypes: DynaMine suite will be run default, then here can determine what else to run on top.
    :return: Nothing
    """

    self.seqs = seqs
    sanitized_pred_types = [tool.lower() for tool in predTypes]

    # DynaMine - always needs to be run
    self.dynaMine.predictSeqs(seqs)
    self.allPredictions = self.dynaMine.allPredictions

    if constants.TOOL_EFOLDMINE in sanitized_pred_types or constants.TOOL_DISOMINE in sanitized_pred_types:
      # EFoldMine
      self.eFoldMine.predictSeqs(seqs, dynaMinePreds=self.dynaMine.allPredictions)
      # This needs cleaning up!
      # TODO double-check that dynamine preds are not messed up!
      self.allPredictions = self.eFoldMine.allPredictions

    if constants.TOOL_DISOMINE in sanitized_pred_types:
      # DisoMine
      self.disoMine.allPredictions = self.allPredictions
      self.disoMine.predictSeqs(seqs)

      # TODO should also pull Psipred predictions if agmata requested, save time!

    if constants.TOOL_AGMATA in sanitized_pred_types:
      self.agmata.allPredictions = self.allPredictions
      self.agmata.predictSeqs(self.seqs)

    if constants.TOOL_PSP in sanitized_pred_types:
      seqs_dict = dict((key, value) for key, value in seqs)
      self.psper.predictSeqs(seqs_dict)

      for key, value in self.psper.allPredictions.items():

        for psper_key in ['viterbi', 'complexity', 'arg', 'tyr', 'RRM', 'disorder', 'psper_execution_time']:
              if psper_key in value:
                self.allPredictions[key][psper_key] = value[psper_key]
              else:
                self.allPredictions[key][psper_key] = [None] * len(value['seq'])
