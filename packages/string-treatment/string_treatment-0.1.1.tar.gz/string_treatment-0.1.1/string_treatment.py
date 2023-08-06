import operator
import typing
from jellyfish import jaro_winkler_similarity, damerau_levenshtein_distance, hamming_distance
import numpy as np
import pandas as pd

METRICS_DICT = {
  'jaro_winkler_similarity': jaro_winkler_similarity, 
  'damerau_levenshtein_distance': damerau_levenshtein_distance, 
  'hamming_distance': hamming_distance
}

def treat_unreferenced(strings_compared: list, 
                        metrics: typing.Union[list[str], str] = 'all', 
                        threshold: float = 0.9):
  '''    
  :param: strings_compared: list of strings to be compared.
  :param: metrics: metrics to be tested as similiraty measurement of distance between strings.
  :param: threshold: threshold for the metrics similarity values.
  
  :return: list of strings 'corrected'.
  '''

  if metrics == 'all':
    metrics = list(METRICS_DICT.keys())
  elif type(metrics) == list or type(metrics) == str:
    if type(metrics) == str: metrics = [metrics]
  else:
    raise TypeError('Metrics must be a list or string')
  
  if 0 > threshold > 1:
    raise ValueError('Threshold must be between 0 and 1')
  
  try:
    metrics_functions = [METRICS_DICT[x] for x in metrics] 
  except:
    raise KeyError("Metrics must be a list or string with the following values: 'jaro_winkler_similarity', 'damerau_levenshtein_distance', 'hamming_distance'.")
  
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
        distances[strings[j]] = metric(strings[i].lower().strip(), strings[j].lower().strip())
          
      all_distances = pd.DataFrame(data = distances, index = [0]).unstack().reset_index().drop('level_1', axis = 1)
      
      if metric.__name__ != 'jaro_winkler_similarity':
        all_distances[0] = (all_distances[0] - all_distances[0].max()) / (all_distances[0].min() - all_distances[0].max())
          
      all_distances = all_distances[all_distances[0] >= threshold]
      
      if all_distances.empty: 
        continue
      
      metric_sum[0] += all_distances[0].sum()
      metric_sum[1] += all_distances[0].shape[0]
      
      all_distances_max_string = all_distances[all_distances[0] == max(all_distances[0])]['level_0'].values[0] 
      
      already_corrected.append(all_distances_max_string)  
        
      strings = np.where(np.isin(strings, all_distances['level_0'].values) == True, all_distances_max_string, strings) 
    
    metric_sum = metric_sum[0] / metric_sum[1]
          
    metrics_results[metric.__name__] = (metric_sum, strings)
  
  best_metric = max(metrics_results.items(), key = operator.itemgetter(1))

  print(f"Best metric '{best_metric[0]}' with mean {best_metric[1][0]}.")
  
  return best_metric[1][1]


def treat_referenced(strings_compared: list[str], 
                      reference: list[str],
                      metric: str = 'jaro_winkler_similarity'):
  '''    
  :param strings_compared: list of strings to be compared.
  :param reference: list of reference strings.
  :param metric: metric to be used as similiraty measurement of distance between strings.
  
  :return: list of strings 'corrected'.
  '''
  
  try:
    metric = METRICS_DICT[metric]
  except:
    raise KeyError("metric must be a string with one of the following values: 'jaro_winkler_similarity' OR 'damerau_levenshtein_distance' OR 'hamming_distance'.")
  
  strings_corrected = list()
  comparations = dict()

  for strings in strings_compared:
    for ref in reference:
      comparations[ref] = metric(strings.lower().strip(), ref.lower().strip())

    strings_corrected.append(
        max(comparations.items(), key = operator.itemgetter(1))[0]
    )

    comparations.clear()

  return strings_corrected