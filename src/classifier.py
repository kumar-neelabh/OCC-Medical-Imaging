import numpy as np
import torch
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix

class Classifier:
  '''
  An extension to the original Deep SVDD to enable classification of test cases.
  
  optim_thresh(): get the threshold at which your metric is maximized
  classifier(): get y_pred based on optimum threshold
  wrong_answers(): get the list of test examples the classifier() wrongly classified in order to optimize the metric
  '''
  
  def __init__(self, X, y_true, probs, objective):
    self.X = X
    self.y_true = y_true
    self.probs = probs
    self.objective = objective
    
    self.y_pred = None
    self.acc_thresh = None
    self.max_acc = None
    self.confusion_matrix = None
  
  def optim_thresh(self, score='acc'):
    if score == 'acc':
      fpr, tpr, thresholds = roc_curve(self.y_true, self.probs)
      accuracy_scores = []
      for thresh in thresholds:
          accuracy_scores.append(accuracy_score(self.y_true, 
                                               [1 if m > thresh else 0 for m in self.probs]))

      accuracies = np.array(accuracy_scores)
      
      self.max_acc = accuracies.max()
      self.acc_thresh = thresholds[accuracies.argmax()]
      return self.acc_thresh

    return 'metric not defined'
  
  def classify(self, score='acc'):
    if self.objective == 'one-class':
      if score == 'acc':
        thresh = self.optim_thresh(score='acc')
        self.y_pred = [1 if m > thresh else 0 for m in self.probs]
        return self.y_pred
    
    if self.objective == 'soft-boundary':
      self.y_pred = [1 if m > 0 else 0 for m in self.probs]
      self.max_acc = accuracy_score(self.y_true, self.y_pred)
      return self.y_pred
      
    return 'metric not defined'
  
  def wrong_answers(self):
    if self.y_pred is None:
      _ = self.classify()
      
    wrong_idx = np.array([i for i, pred in enumerate(self.y_pred) if pred != self.y_true[i]]).flatten()
    wrong_imgs = [self.X[index] for index in wrong_idx]
    
    return wrong_imgs
  
  def conf_matrix(self):
    if self.y_pred is None:
      _ = self.classify()
      
    conf_mat = confusion_matrix(self.y_true, self.y_pred)
    return conf_mat
 
