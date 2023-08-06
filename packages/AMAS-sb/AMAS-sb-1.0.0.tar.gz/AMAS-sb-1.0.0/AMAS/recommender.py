# recommender.py
"""
Recomender for running annotation predictions.
This module is going to be directly used by the users.
"""

# import collections
import compress_pickle
import copy
import fnmatch
import itertools
import libsbml
import numpy as np
import os
import pandas as pd
import re

from AMAS import annotation_maker as am
from AMAS import constants as cn
from AMAS import iterator as it
from AMAS import tools
from AMAS import species_annotation as sa
from AMAS import reaction_annotation as ra

ELEMENT_TYPES = ['species', 'reaction']

class Recommender(object):

  def __init__(self,
               libsbml_cl=None, 
               libsbml_fpath=None,
               model_specs=None):
    """
    Parameters
    ----------
    libsbml_cl: libsbml.SBMLDocument
        A libsbml document class instance
    libsbml_fpath: str
        File path of an SBML model
    mdoel_specs: tuple/list
        Iterable object of two tuples including model specifications
    """
    # Document will be updated and saved if chosen. 
    self.sbml_document = None
    # First of all, collect model information from libsbml model
    # and send the informaton to create species/reaction annotations
    fname = None
    if libsbml_cl:
      spec_tuple, reac_tuple = self._parseSBML(libsbml_cl)
    elif libsbml_fpath:
      spec_tuple, reac_tuple = self._parseSBML(libsbml_fpath)
      # basically split fpath and use the last one
      fname = libsbml_fpath.split('/')[-1]
    elif model_specs:
      spec_tuple = model_specs[0]
      reac_tuple = model_specs[1]
    else:
      spec_tuple = None
      reac_tuple = None
    self.fname = fname
    self.species = sa.SpeciesAnnotation(inp_tuple=spec_tuple)
    self.reactions = ra.ReactionAnnotation(inp_tuple=reac_tuple)
    # Below are elements to interact with user
    self.current_type = None
    self.just_displayed = None
    self.selection = {val:dict() for val in ELEMENT_TYPES}


  def getDataFrameFromRecommendation(self,
                                     rec,
                                     show_url=False):
    """
    Get a pandas dataframe from 
    a single recommendation.

    Parameters
    ----------
    rec: cn.Recommendation

    show_url: bool
        If False, omit this column

    Returns
    -------
    :str
    """
    cands = [val[0] for val in rec.candidates]
    match_scores = [val[1] for val in rec.candidates]
    
    labels = rec.labels
    # index starts from 1;
    df = pd.DataFrame({'annotation':cands,
                       cn.DF_MATCH_SCORE_COL:match_scores,
                       'label':labels},
                       index=[1+val for val in list(range(len(cands)))])
    # df.index.name = '%s (cred. %.3f)' % (rec.id ,rec.credibility)
    df.index.name = rec.id
    if show_url:
      urls = rec.urls
      df['url'] = urls
    return df

  def getMarkdownFromRecommendation(self,
                                    rec,
                                    show_url=False):
    """
    Get a markdown using 
    a cn.Recommendation or pandas.DataFrame.

    Parameters
    ----------
    rec: cn.Recommendation/pandas.DataFrame

    show_url: bool
        If False, omit this column

    Returns
    -------
    :str
    """
    if isinstance(rec, pd.DataFrame):
      # to deepcopy so original data doesn't get changed
      # in line 156. 
      df = copy.deepcopy(rec)
      idx_name = df.index.name.split(' ')
      rec_id = idx_name[0]
    else:
      df = self.getDataFrameFromRecommendation(rec, show_url)
      rec_id = rec.id
      # rec_credibility = rec.credibility
    # In markdown, title is shown separately,
    # so index name with element ID is removed; 
    df.index.name=None
    df_str = df.to_markdown(tablefmt="grid", floatfmt=".03f", index=True)
    # Centering and adding the title 
    len_first_line = len(df_str.split('\n')[0])
    title_line = rec_id
    # title_line = "%s (credibility score: %.03f)" % (rec_id,  rec_credibility)
    title_line = title_line.center(len_first_line)
    df_str = title_line + '\n' + df_str
    return df_str

  def getSpeciesRecommendation(self,
                               pred_str=None,
                               pred_id=None,
                               method='cdist',
                               mssc='top',
                               cutoff=0.0,
                               update=True,
                               get_df=False):

    """
    Predict annotations of species using
    the provided string or ID.
    If pred_str is given, directly use the string;
    if pred_id is given, determine the appropriate
    name using the species ID. 
    Algorithmically, it is a special case of 
    self.getSpeciesListRecommendation.

    Parameters
    ----------
    pred_str: str
        Species name to predict annotation with
    pred_id: str
        ID of species (search for name using it)
    method: str
        One of ['cdist', 'edist']
        'cdist' represents Cosine Similarity
        'edist' represents Edit Distance.
        Default method id 'cdist'
    mssc: match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    update: bool
        If true, update existing species annotations
        (i.e., replace or create new entries)
        in self.species.candidates and self.species.formula
    get_df: bool
        If true, return a pandas.DataFrame.
        If False, return a cn.Recommendation

    Returns
    -------
    cn.Recommendation (namedtuple) / str
    """
    if pred_str:
      result = self.getSpeciesListRecommendation(pred_strs=[pred_str],
                                                 method=method,
                                                 mssc=mssc,
                                                 cutoff=cutoff,
                                                 update=update,
                                                 get_df=get_df)
    elif pred_id:
      result = self.getSpeciesListRecommendation(pred_ids=[pred_id],
                                                 method=method,
                                                 mssc=mssc,
                                                 cutoff=cutoff,
                                                 update=update,
                                                 get_df=get_df)  
    return result[0]    

  def getSpeciesIDs(self, pattern=None, regex=False):
    """
    Returns Species IDs that match the pattern.
    The pattern is given as glob
    If none is given, returns all available
    species that exist in the model.
  
    Parameters
    ---------
    pattern: str/None
      string pattern
    reges: bool
      if True, use regex
      if False, use glob

    Returns
    -------
    list-str/None
        None returned if no match was found
    """
    # list of species ids
    specs = list(self.species.names.keys())
    # returns a list of ids thta match pattern, if None, return all
    if pattern is None:
      return specs
    else:
      if regex:
        re_pattern = pattern
      else:
        re_pattern = fnmatch.translate(pattern)
      matched = [re.match(re_pattern, val) for val in specs]
      filt_matched = [val.group(0) for val in matched if val]
      if len(filt_matched)>0:
        return filt_matched
      else:
        return None

  def getSpeciesListRecommendation(self,
                                   pred_strs=None,
                                   pred_ids=None,
                                   method='cdist',
                                   mssc='top',
                                   cutoff=0.0,
                                   update=True,
                                   get_df=False):
    """
    Get annotation of multiple species,
    given as a list (or an iterable object).
    self.getSpeciesRecommendation is applied to
    each element. 

    Parameters
    ----------
    pred_strs: str-list
        :Species names to predict annotations with
    pred_ids: str-list
        :Species IDs to predict annotations with
         (model info should have been already loaded)
    method: str
        One of ['cdist', 'edist']
        'cdist' represents Cosine Similarity
        'edist' represents Edit Distance.
        Default method id 'cdist'
    mssc: match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    update: bool
        :If true, update the current annotations
        (i.e., replace or create new entries)
        in self.species.candidates and self.species.formula
    get_df: bool
        If True, return a list of pandas.DataFrame.
        If False, return a list of cn.Recommendation

    Returns
    -------
    list-Recommendation (list-namedtuple) / list-str
    """
    scoring_methods = {'edist': self.species.getEScores,
                       'cdist': self.species.getCScores} 
    if pred_strs: 
      ids_dict = {k:k for k in pred_strs}
      inp_strs = pred_strs
    elif pred_ids:
      ids_dict = {k:self.species.getNameToUse(inp_id=k) \
                  for k in pred_ids}
      inp_strs = [ids_dict[k] for k in ids_dict.keys()]
    pred_res = scoring_methods[method](inp_strs=inp_strs,
                                       mssc=mssc,
                                       cutoff=cutoff)
    result = []
    for spec in ids_dict.keys():
      urls = [cn.CHEBI_DEFAULT_URL + val[0][6:] for val in pred_res[ids_dict[spec]]]
      labels = [cn.REF_CHEBI2LABEL[val[0]] for val in pred_res[ids_dict[spec]]]
      one_recom = cn.Recommendation(spec,
                                    [(val[0], np.round(val[1], cn.ROUND_DIGITS)) \
                                     for val in pred_res[ids_dict[spec]]],
                                    urls,
                                    labels)
      result.append(one_recom)
      if update:
         _ = self.species.updateSpeciesWithRecommendation(one_recom)
    if get_df:
      return [self.getDataFrameFromRecommendation(rec=val) \
              for val in result]
    else:
      return result

  def getReactionRecommendation(self, pred_id,
                                use_exist_species_annotation=False,
                                spec_res=None,
                                spec_method='cdist',
                                mssc='top',
                                cutoff=0.0,                                
                                update=True,
                                get_df=False):
    """
    Predict annotations of reactions using
    the provided IDs (argument). 
    Can be either singular (string) or plural

    Parameters
    ----------
    pred_id: str
        A single ID of reaction to annotate
    use_exist_speices_annotation: bool
        If True, use existing species annotation
    spec_res: list-cn.Recommendation
        If provided, species will not be predicted
        for remaining species
    spec_method: str
        Method to use if to directly predict species annotation;
        if 'cdist' Cosine Similarity
        if 'edist' Edit distance
    mssc: match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    update: bool
        If true, update existing species annotations
        (i.e., replace or create new entries)
        in self.reactions.candidates
    get_df: bool
        If True, return a pandas DataFrame.
        If False, return a cn.Recommendation

    Returns
    -------
    Recommendation (namedtuple) / str
    """
    result = self.getReactionListRecommendation(pred_ids=[pred_id],
                                                use_exist_species_annotation=use_exist_species_annotation,
                                                spec_res=spec_res,
                                                spec_method=spec_method,
                                                mssc=mssc,
                                                cutoff=cutoff,
                                                update=update,
                                                get_df=get_df)
    return result[0]


  def getReactionIDs(self, pattern=None, by_species=False, regex=False):
    """
    Get IDs of reactions based on
    the pattern.
    
    If by_species is True, it retrieves
    all reaction with the species that match
    the pattern; 
    if False, it searches based on the ID of 
    reactions
    
    Parameters
    ---------
    pattern: str
        Pattern
        
    by_species: bool
      If True, find species with pattern
      If False, find reaction IDs
      
    regex: bool
      If True, use regex expression
      If False, convert it to regex.
    """
    reacts = list(self.reactions.reaction_components.keys())
    if pattern is None:
      return reacts
    # returns a list of ids thta match pattern, if None, return all
    if regex:
      re_pattern = pattern
    else:
      re_pattern = fnmatch.translate(pattern)
    if by_species:
      specs2use = self.getSpeciesIDs(pattern=re_pattern, regex=True)
      if any(specs2use):
        comp_items = list(self.reactions.reaction_components.items())
        result = [val[0] for val in comp_items \
                  if any(set(val[1]).intersection(specs2use))]
      # if no species match was found
      else:
        return None
    else:
      matched = [re.match(re_pattern, val) for val in reacts]
      result = [val.group(0) for val in matched if val]
    return result

  def getReactionListRecommendation(self, pred_ids,
                                    use_exist_species_annotation=False,
                                    spec_res=None,
                                    spec_method='cdist',
                                    mssc='top',
                                    cutoff=0.0,
                                    update=True,
                                    get_df=False):
    """
    Get annotation of multiple reactions.
    Instead of applying getReactionRecommendation 
    for each reaction,
    it'll predict all component species first
    and proceed (this will reduce computational cost).

    Parameters
    ----------
    pred_ids: str-list
        For now, it only accommodates calling by reaction IDs.
    use_exist_species_annotation: tool
        If True, search existing annotation for species
        and predict the remaining species
    spec_res: list-cn.Recommendation
        If provided, species will not be predicted
        for remaining species
    spec_method: str
        Method to use if to directly predict species annotation;
        if 'cdist' Cosine Similarity
        if 'edist' Edit distance
    mssc: match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    update: bool
        If true, update existing species annotations
        (i.e., replace or create new entries)
        in self.reactions.candidates
    get_df: bool
        If True, return a list of pandas DataFrames.
        If False, return a list of cn.Recommendation

    Returns
    -------
    list-Reccommendation (list-namedtuple) / list-str
    """
    # First, collect all species IDs to annotate
    specs_to_annotate = list(set(itertools.chain(*[self.reactions.reaction_components[val] \
                                                   for val in pred_ids])))
    if use_exist_species_annotation:
      pred_formulas = {val:self.species.exist_annotation_formula[val] \
                       for val in specs_to_annotate \
                       if val in self.species.exist_annotation_formula.keys()}
    else:
      pred_formulas = {}
    remaining_species = [val for val in specs_to_annotate if val not in pred_formulas.keys()]
    # Get annotation of collected species
    if len(remaining_species) > 0:
      if spec_res:
        spec_results = [val for val in spec_res if val.id in remaining_species]
      else:
        # No updates; use MSSC Top, cutoff 0.0. 
        spec_results = self.getSpeciesListRecommendation(pred_ids=remaining_species,
                                                         update=False,
                                                         method=spec_method)
      for one_recom in spec_results:
        chebis = [val[0] for val in one_recom.candidates]
        forms = list(set([cn.REF_CHEBI2FORMULA[k] \
                 for k in chebis if k in cn.REF_CHEBI2FORMULA.keys()]))
        pred_formulas[one_recom.id] = forms
    # Predict reaction annotations. 
    pred_res = self.reactions.getRScores(spec_dict=pred_formulas,
                                         reacs=pred_ids,
                                         mssc=mssc,
                                         cutoff=cutoff)
    result = []
    for reac in pred_res.keys():
      urls = [cn.RHEA_DEFAULT_URL + val[0][5:] for val in pred_res[reac]]
      labels = [cn.REF_RHEA2LABEL[val[0]] for val in pred_res[reac]]
      one_recom = cn.Recommendation(reac,
                                    [(val[0], np.round(val[1], cn.ROUND_DIGITS)) \
                                     for val in pred_res[reac]],
                                    urls,
                                    labels)
      result.append(one_recom)
    if update:
      self.reactions.candidates = pred_res
    if get_df:
      return [self.getDataFrameFromRecommendation(rec=val) \
              for val in result]
    else:
      return result

  def _parseSBML(self, sbml):
    """
    Parse SBML file and return 
    two tuples, for species and reactions 
    respecitvely,
    equivalent to model_specs.
    Can use either libsbml.Document class
    or a file path.

    Parameters
    ----------
    sbml: str(filepath)/libsbml.Document

    Returns
    -------
    (tuple, tuple): 
        Two tuples to create species/reaction annotation classes
        (species_tuple, reaction_tuple)
    """
    if isinstance(sbml, str):
      reader = libsbml.SBMLReader()
      # Reading the model string file
      with open(sbml, 'r') as f:
        model_str = f.read()
      self.sbml_document = reader.readSBMLFromString(model_str)
      # self.sbml_document = reader.readSBML(sbml)
    elif isinstance(sbml, libsbml.SBMLDocument):
      self.sbml_document = sbml
    model = self.sbml_document.getModel()
    exist_spec_annotation = tools.extractExistingSpeciesAnnotation(model)
    species_names = {val.getId():val.name for val in model.getListOfSpecies()}
    species_tuple = (species_names, exist_spec_annotation)
    #
    reac_exist_annotation = tools.extractExistingReactionAnnotation(inp_model=model)
    # Next, reaction components for each reaction
    reac_components = {val.getId():list(set([k.species for k in val.getListOfReactants()]+\
                                            [k.species for k in val.getListOfProducts()])) \
                       for val in model.getListOfReactions()}
    reaction_tuple = (reac_components, reac_exist_annotation)
    return species_tuple, reaction_tuple


  def getSpeciesStatistics(self,
                           mssc='top',
                           cutoff=0.0,
                           model_mean=True):
    """
    Get recall and precision 
    of species in a model, for both species and
    reactions.
    This method works only if there exists
    annotation in  model; otherwise
    None will be returned. 
    In the result, values will be 
    returned after rounding to the two decimal places. 

    Parameters
    ----------
    mssc: str
        match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    model_mean: bool
      If True, get single float values for recall/precision.
      If False, get a dictionary for recall/precision. 

    Returns
    -------
    None/dict
        Return None if there is nothing to evaluate
        (i.e., if there is no existing model annotation)
    """
    # get dictionary of formulas if they exist
    refs = {val:self.species.exist_annotation_formula[val] \
            for val in self.species.exist_annotation_formula.keys() \
            if self.species.exist_annotation_formula[val]}
    specs2eval = list(refs.keys())
    if len(specs2eval) == 0:
      return None
    preds_comb = self.getSpeciesListRecommendation(pred_ids=specs2eval,
                                                   mssc=mssc,
                                                   cutoff=cutoff)
    chebi_preds = {val.id:[k[0] for k in val.candidates] \
                   for val in preds_comb}
    preds = {k:[cn.REF_CHEBI2FORMULA[val] for val in chebi_preds[k] \
                if val in cn.REF_CHEBI2FORMULA.keys()] \
             for k in chebi_preds.keys()}
    recall = tools.getRecall(ref=refs, pred=preds, mean=model_mean)
    precision = tools.getPrecision(ref=refs, pred=preds, mean=model_mean)
    return {cn.RECALL: recall, cn.PRECISION: precision}


  def getReactionStatistics(self,
                            model_mean=True,
                            mssc='top',
                            cutoff=0.0):
    """
    Get recall and precision 
    of reactions in a model, for both species and
    reactions.
    This method works only if there exists
    annotation in  model; otherwise
    None will be returned. 
    In the result, values will be 
    returned after rounding to the two decimal places. 

    Parameters
    ----------
    mssc: str
        match score selection criteria
        'top' will recommend candidates with
        the highest match score above cutoff
        'above' will recommend all candidates with
        match scores above cutoff
    cutoff: float
        Cutoff value; only candidates with match score
        at or above the cutoff will be recommended.
    model_mean: bool
      If True, get single float values for recall/precision.
      If False, get a dictionary for recall/precision. 

    Returns
    -------
    None/dict
        Return None if there is nothing to evaluate
        (i.e., if there is no existing model annotation)
    """
    # For reactions, component species should be
    # predicted first. 
    refs = self.reactions.exist_annotation
    if len(refs) == 0:
      return None
    specs2pred = list(set(itertools.chain(*([self.reactions.reaction_components[val] for val in refs.keys()]))))
    ## Use mssc top, cutoff 0.0. 
    preds_comb = self.getSpeciesListRecommendation(pred_ids=specs2pred,
                                                   mssc='top',
                                                   cutoff=0.0)
    chebi_preds = {val.id:[k[0] for k in val.candidates] \
                   for val in preds_comb}
    specs_predicted = {k:[cn.REF_CHEBI2FORMULA[val] for val in chebi_preds[k] \
                       if val in cn.REF_CHEBI2FORMULA.keys()] \
                       for k in chebi_preds.keys()}
    reac_preds = self.reactions.getRScores(spec_dict=specs_predicted,
                                           reacs=refs.keys(),
                                           mssc='top',
                                           cutoff=0.0)
    preds = {k:[val[0] for val in reac_preds[k]] for k in reac_preds.keys()}
    recall = tools.getRecall(ref=refs, pred=preds, mean=model_mean)
    precision = tools.getPrecision(ref=refs, pred=preds, mean=model_mean)
    return {cn.RECALL: recall, cn.PRECISION: precision}

  def filterDataFrameByThreshold(self, df, min_score):
    """
    Filter dataframe by min_score (threshold),
    and returns the result;
  
    Note that if no item meets the threshold,
    it'll still return an empty dataframe. 

    Paramters
    ---------
    df: pd.DataFrame
  
    min_score: float (0.0-1.0)
  
    Returns
    -------
    pd.DataFrame  
    """
    scores = df[cn.DF_MATCH_SCORE_COL]
    filt_idx = scores[scores>=min_score].index
    filt_df = df.loc[filt_idx, :]
    return filt_df


  def autoSelectAnnotation(self,
                           df,
                           cutoff=0.0,
                           mssc='top'):
    """
    Choose annotations based on 
    the set threshold; 
    (1) if None meets the threshold, return an empty frame
    (2) if multiple meet the threshold,
        (a) if method is 'best':
            (i) find the highest match score among them
            (ii) return all above match score == highest_match_score
        (b) if method is 'all':
            (i) return all that is at or above min_score
      
    Parameters
    ----------
    df: pandas.DataFrame
  
    cutoff: float (0.0-1.0)
        Match score cutoff

    mssc: str
        Match score selection criteria;
        either 'top' or 'above'.

    Returns
    -------
    pandas.DataFrame
      if nothing matched,
      an empty dataframe is returned
    """ 
    scores = df[cn.DF_MATCH_SCORE_COL]
    # max_score: highest match score that exists
    # min_score: cutoff
    max_score = np.max(scores)
    if max_score < cutoff:
      # this will create an empty dataframe
      filt_idx = scores[scores>=cutoff].index
    elif mssc=='top':
      filt_idx = scores[scores==max_score].index
    else:
      filt_idx = scores[scores>=cutoff].index
    filt_df = df.loc[filt_idx, :]  
    return filt_df

  def recommendReaction(self,
                        ids=None,
                        mssc='top',
                        cutoff=0.0):
    """
    Recommend one or more ids of species
    and returns a single dataframe or
    a list of dataframes.
  
    Parameters
    ----------
    ids: str/list-str
        If None, recommend all reactionos.

    mssc: str
        match score selection criteria.
        'top' or 'above'

    cutoff: float
        MSSC cutoff

    Returns
    -------
    None
    """
    self.updateCurrentElementType('reaction')
    if isinstance(ids, str):
      reaction_list = [ids]
    elif ids is None:
      reaction_list = self.getReactionIDs()
    else:
      reaction_list = ids
    res = self.getReactionListRecommendation(pred_ids=reaction_list,
                                             mssc=mssc,
                                             cutoff=cutoff,
                                             get_df=True)
    res_dict = {val:res[idx] for idx, val in enumerate(reaction_list)}
    for k in res_dict.keys():
      filt_df = self.filterDataFrameByThreshold(res_dict[k], cutoff)
      print(self.getMarkdownFromRecommendation(filt_df)+"\n")
    self.updateJustDisplayed(res_dict)
    return None

  def recommendSpecies(self, ids=None, min_score=0.0):
    """
    Recommend one or more ids of species
    and returns a single dataframe or
    a list of dataframes.
  
    Parameters
    ----------
    ids: str/list-str
        If None, will predict all
  
    min_score: threshold for cutoff
        If None given, returns all values; 

    Returns
    -------
    None
    """
    self.updateCurrentElementType('species')
  
    if isinstance(ids, str):
      species_list = [ids]
    elif ids is None:
      species_list = self.getSpeciesIDs()
    else:
      species_list = ids
    res = self.getSpeciesListRecommendation(pred_ids=species_list,
                                            get_df=True)
    res_dict = {val:res[idx] for idx, val in enumerate(species_list)}
    for k in res_dict.keys():
      filt_df = self.filterDataFrameByThreshold(res_dict[k], min_score)
      print(self.getMarkdownFromRecommendation(filt_df)+'\n')
    self.updateJustDisplayed(res_dict)
    return None

  def updateCurrentElementType(self, element_type):
    """
    Updating self.current_type
    indicator; updated when
    recommendSpecies or recommendReaction 
    is called; 
  
    Parameters
    ----------
    element_type: str
        Either 'species' or 'reaction'
    """
    self.current_type = element_type

  def updateJustDisplayed(self, df_dict):
    """
    Used it every time
    result is shown to user.
    called by 
    /recommendSpecies/recommendReaction/
    /selectAnnotation/
    For now, always in the format as
    pandas.DataFrame. 

    Parameters
    ----------
    df_dict: dict()
        Dictionary of pandas.DataFrame
  
    Returns
    -------
    None
    """
    self.just_displayed = df_dict

  def selectAnnotation(self, choice=None):
    """
    Based on the previous recommendation,
    determine the annotations to store.
    If 'all' given in choice[1],
    select all.
  
    Parameters
    ----------
    choice: tuple/list-tuple (str, int)
        [(element ID, choice number)]
    """
    # assumes self.just_displayced is {id: pd.dataframe}
    sel_id = choice[0]
    sel_idx = choice[1]
    df = self.just_displayed[choice[0]]
    if sel_idx == 'all':
      result = df
    else:
      if isinstance(sel_idx, int):
        chosen = [sel_idx]
      else:
        chosen = sel_idx
      result = df.loc[chosen, :]
    # Now, update the selected annotation
    self.updateSelection(sel_id, result)
    print("Selection updated.")
    return None

  def updateSelection(self, sel_id, sel_df):
    """
    Direct result of selectAnnotation;
    filtered or non-filtered
    dictionary of dataframes.
  
    By calling SaveFile,
    All selected annotations will be
    saved as an .xml file. 
  
    Parameters
    ----------
    sel_id: str
  
    sel_df: pandas.DataFrame
    """
    self.selection[self.current_type].update({sel_id: sel_df})

  def displaySelection(self):
    """
    To assist user, 
    display all selected
    annotations from
    self.selection.
    """
    for one_type in ELEMENT_TYPES:
      type_selection = self.selection[one_type]
      for k in type_selection.keys():
        print(self.getMarkdownFromRecommendation(type_selection[k])+"\n")

  def saveToCSV(self, fpath="recommendation.csv"):
    """
    Save self.selection to csv.

    Parameters
    ----------
    fpath: str
        Path of the csv file to be saved. 
    """
    model = self.sbml_document.getModel()
    TYPE_EXISTING_ATTR = {'species': self.species.exist_annotation,
                          'reaction': self.reactions.exist_annotation}
    ELEMENT_FUNC = {'species': model.getSpecies,
                    'reaction': model.getReaction}
    TYPE_LABEL = {'species': cn.REF_CHEBI2LABEL,
                  'reaction': cn.REF_RHEA2LABEL}
    pd.set_option('display.max_colwidth', 255)
    # edf: element_df
    edfs = []    
    for one_type in self.selection.keys():
      type_selection = self.selection[one_type]
      for k in list(type_selection.keys()):   
        one_edf = type_selection[k]
        if one_edf.shape[0] == 0:
          continue
        annotations = list(one_edf['annotation'])
        match_scores = list(one_edf[cn.DF_MATCH_SCORE_COL])
        labels = list(one_edf['label'])
        # if there is existing annotation among predicted candidates;
        if k in TYPE_EXISTING_ATTR[one_type].keys():
          existings = [1 if val in TYPE_EXISTING_ATTR[one_type][k] else 0 \
                       for idx, val in enumerate(one_edf['annotation'])]
          upd_annotation = ['keep' if val in TYPE_EXISTING_ATTR[one_type][k] else 'ignore' \
                            for idx, val in enumerate(one_edf['annotation'])]
          annotation2add_raw = [val for val in TYPE_EXISTING_ATTR[one_type][k] \
                                if val not in list(one_edf['annotation'])]
          # only use existing annotation that exists in the label dictionaries
          annotation2add = [val for val in annotation2add_raw \
                            if val in TYPE_LABEL[one_type].keys()]

        # if there doesn't exist existing annotation among predicted candidates;
        else:
          existings = [0] * len(annotations)
          upd_annotation = ['ignore'] * len(annotations)
          annotation2add = []
        # handling existing annotations that were not predicted
        for new_anot in annotation2add:
          annotations.append(new_anot)
          if one_type=='reaction':
            match_scores.append(self.getMatchScoreOfRHEA(k, new_anot))
            labels.append(cn.REF_RHEA2LABEL[new_anot])
          elif one_type=='species':
            match_scores.append(self.getMatchScoreOfCHEBI(k, new_anot))
            labels.append(cn.REF_CHEBI2LABEL[new_anot])
          existings.append(1)
          upd_annotation.append('keep')
        new_edf = pd.DataFrame({'type': [one_type]*len(annotations),
                                'id': [k]*len(annotations),
                                'display name': [ELEMENT_FUNC[one_type](k).name]*len(annotations),
                                'meta id': [ELEMENT_FUNC[one_type](k).meta_id]*len(annotations),
                                'annotation': annotations,
                                'annotation label': labels,
                                cn.DF_MATCH_SCORE_COL: match_scores,
                                'existing': existings,
                                cn.DF_UPDATE_ANNOTATION_COL: upd_annotation})
        edfs.append(new_edf)
    res = pd.concat(edfs)
    res.insert(0, 'file', self.fname)
    # Write result to csv
    res.to_csv(fpath, index=False) 
    # print summary; 
    # Summary message
    for one_type in ELEMENT_TYPES:
      saved_elements = list(np.unique(res[res['type']==one_type]['id']))
      self.printSummary(saved_elements, one_type)

  def saveToSBML(self,
                 fpath='model_amas_annotations.xml',
                 option='augment'):
    """
    Update and save model;
    How to distinguish species vs. reactions? 
    by using self.current_element_type.

    If option is 'augment',
    it'll add candidate annotations to 
    existing annotation string.
    If option is 'replace',
    create a new annotation string and
    replace whatevers exists.
    Default to 'augment'.  
  
    Call annotation maker;
  
    Parameters
    ----------
    fpath: str
        Path to save file

    option: str
        Either 'augment' or 'replace'
    """
    model = self.sbml_document.getModel()
    ELEMENT_FUNC = {'species': model.getSpecies,
                    'reaction': model.getReaction}
    # dictionary with empty lists; 
    saved_elements = {k:[] for k in ELEMENT_TYPES}
    for one_type in ELEMENT_TYPES:
      type_selection = self.selection[one_type]
      maker = am.AnnotationMaker(one_type)
      sel2save = type_selection
      for one_k in sel2save.keys():
        one_element = ELEMENT_FUNC[one_type](one_k)
        meta_id = one_element.meta_id
        df = sel2save[one_k]
        cands2save = list(df['annotation'])
        if cands2save:
          if option == 'augment':
            orig_annotation = one_element.getAnnotationString()
            annotation_str = maker.addAnnotation(cands2save,
                                                 orig_annotation,
                                                 meta_id)
          elif option == 'replace':
            annotation_str = maker.getAnnotationString(cands2save, meta_id)
          one_element.setAnnotation(annotation_str)
          saved_elements[one_type].append(one_k)
        else:
          continue
    # finally, write the sbml document 
    libsbml.writeSBMLToFile(self.sbml_document, fpath)

    # Summary message
    for one_type in ELEMENT_TYPES:
      self.printSummary(saved_elements[one_type], one_type)

  def printSummary(self, saved, element_type):
    """
    Print out a summary of 
    saved element IDs and numbers. 
  
    Parameters
    ----------
    saved: list-str
        List of elements saved. 

    element_type: str
        'species' or 'reaction'
    """
    plural_str = {'species': '',
                  'reaction': '(s)'}
    num_saved = len(saved)
    if num_saved == 0:
      return None
    print("Annotation recommended for %d %s%s:\n[%s]\n" %\
          (num_saved,
           element_type,
           plural_str[element_type],
           ', '.join(saved))) 
    
  def getMatchScoreOfCHEBI(self, inp_id, inp_chebi):
    """
    Calculate match score of a species (by ID)
    with a ChEBI term. 
    This is to inform user of how well it matches with
    a specific ChEBI term.
    If the ChEBI term somehow 
    doesn't exist in the dictionary,
    0.0 will be returned. 

    Parameters
    ----------
    inp_id: str
        ID of a species

    inp_chebi: str
        A ChEBI term. 

    Returns
    -------
    res: float
    """
    inp_str = self.species.getNameToUse(inp_id)
    scores = self.species.getCScores(inp_strs=[inp_str],
                                     mssc='above',
                                     cutoff=0.0)[inp_str]
    # searching for the match score
    res = next((np.round(v[1], cn.ROUND_DIGITS) \
               for v in scores if v[0] == inp_chebi), 0.0)
    return res

  def getMatchScoreOfRHEA(self, inp_id, inp_rhea):
    """
    Calculate match score of a reaction (by ID)
    with a Rhea term. 
    This is to inform user of how well it matches with
    a specific Rhea term. 

    Parameters
    ----------
    inp_id: str
        ID of a species

    inp_rhea: str
        A Rhea term. 

    Returns
    -------
    res_match_score: float
    """
    specs2predict = self.reactions.reaction_components[inp_id] 
    spec_results = self.getSpeciesListRecommendation(pred_ids=specs2predict,
                                                     update=False,
                                                     method='cdist',
                                                     mssc='top',
                                                     cutoff=0.0)
    pred_formulas = dict()
    for one_spec_res in spec_results:
      chebis = [val[0] for val in one_spec_res.candidates]
      forms = list(set([cn.REF_CHEBI2FORMULA[k] \
             for k in chebis if k in cn.REF_CHEBI2FORMULA.keys()]))
      pred_formulas[one_spec_res.id] = forms
    scores = self.reactions.getRScores(spec_dict=pred_formulas,
                                       reacs=[inp_id],
                                       mssc='above',
                                       cutoff=0.0)[inp_id]
    # searching for the match score
    res = next((np.round(v[1], cn.ROUND_DIGITS) \
               for v in scores if v[0] == inp_rhea), 0.0)
    return res   
