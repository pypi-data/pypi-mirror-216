import matplotlib.pyplot as plt
import numpy as np
from expected_cost import ec, utils
from expected_cost.data import create_scores_for_expts

num_targets = 2
score_dict, targets = create_scores_for_expts(num_targets, calibrate=False, score_scale_mc2=0.2)

print("EC on simulated data using the 0-1 cost matrix")

scores = score_dict['cal']['Datap']
print("EC for Bayes decisions from calibrated posteriors: %.3f"%ec.average_cost_for_bayes_decisions(targets, scores)[0])

scores = score_dict['cal']['Mismp']
print("EC for Bayes decisions from miscalibrated posteriors due to a mismatch in priors: %.3f"%ec.average_cost_for_bayes_decisions(targets, scores)[0])

scores = score_dict['mc2']['Datap']
print("EC for Bayes decisions from miscalibrated posteriors due to simulated overfitting: %.3f"%ec.average_cost_for_bayes_decisions(targets, scores)[0])
