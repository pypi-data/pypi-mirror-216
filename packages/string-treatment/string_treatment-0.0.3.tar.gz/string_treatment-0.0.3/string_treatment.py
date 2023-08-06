import operator
from jellyfish import jaro_winkler_similarity, damerau_levenshtein_distance, hamming_distance
import numpy as np
import pandas as pd

metrics_dict = {
  'jaro_winkler_similarity': jaro_winkler_similarity, 
  'damerau_levenshtein_distance': damerau_levenshtein_distance, 
  'hamming_distance': hamming_distance
}

def string_treatment(strings_compared, reference = None, metrics = 'all', threshold = 0.9) -> list:

    """
    Compare with a list of reference or creating the list within the strings 
    each other and returns the most similar string for each one.
    
    :param strings_compared: list of strings to be compared
    :param reference: list of reference strings or None if you want to build the list of reference within the 'strings_compared'
    :param metrics: metrics to be tested or used as similiraty measurement of distance between strings.
    :param threshold: threshold for the metrics similarity values
    :return: list of strings 'corrected'
    """
    
    if metrics == 'all':
      metrics_functions = list(metrics_dict.values())
      
    elif type(metrics) == list or type(metrics) == str:
      if type(metrics) == str: metrics = [metrics]
      
      try:
        metrics_functions = [metrics_dict[x] for x in metrics] 
      except:
        raise KeyError("Metrics must be a list or string with the following values: 'jaro_winkler_similarity', 'damerau_levenshtein_distance' or 'hamming_distance'")
      
    else:
      raise TypeError('Metrics must be a list or string')
      
      
    if 0 > threshold > 1:
      raise ValueError('Threshold must be between 0 and 1')
    
    
    if reference == None:         
      return _without_reference(metrics_functions, strings_compared, threshold)

    elif type(reference) == list:  
      return _with_reference(strings_compared, reference)

    else:
      raise TypeError('Reference must be a list or None')


def _without_reference(metrics_functions, strings_compared, threshold):
  metrics_results = dict()

  for metric in metrics_functions:
    already_corrected = list()
    strings = strings_compared.copy()
    metric_sum = [0, 0]
    
    for i in range(len(strings)):
      distances = dict()
      if strings[i] in already_corrected: 
        continue
      for j in range(i + 1, len(strings)):   
        if strings[j] in already_corrected: 
          continue      
        # Get all distances from strings[i] to strings[j]                     
        distances[strings[j]] = metric(strings[i].lower().strip(), strings[j].lower().strip())
          
      all_distances = pd.DataFrame(data = distances, index = [0]).unstack().reset_index().drop('level_1', axis = 1)
      
      if metric.__name__ != 'jaro_winkler_similarity':
        all_distances[0] = (all_distances[0] - all_distances[0].max()) / (all_distances[0].min() - all_distances[0].max())
          
      all_distances = all_distances[all_distances[0] >= threshold]
      
      if all_distances.empty: 
        continue
      
      metric_sum[0] += all_distances[0].sum()
      metric_sum[1] += all_distances[0].shape[0]
      
      all_distances_max_string = all_distances[all_distances[0] == max(all_distances[0])]['level_0'].values[0] ###
      
      already_corrected.append(all_distances_max_string) ### 
        
      strings = np.where(np.isin(strings, all_distances['level_0'].values) == True, all_distances_max_string, strings) ###
    
    metric_sum = metric_sum[0] / metric_sum[1]
          
    metrics_results[metric.__name__] = (metric_sum, strings)
  
  best_metric = max(metrics_results.items(), key = operator.itemgetter(1))

  print(f"Best metric '{best_metric[0]}' with mean {best_metric[1][0]}.")
  
  return best_metric[1][1]


def _with_reference(strings_compared, reference):
  strings_corrected = list()
  comparations = dict()

  for strings in strings_compared:
    for ref in reference:
      comparations[ref] = jaro_winkler_similarity(strings.lower().strip(), ref.lower().strip())

    strings_corrected.append(
        max(comparations.items(), key = operator.itemgetter(1))[0]
    )

    comparations.clear()

  return strings_corrected