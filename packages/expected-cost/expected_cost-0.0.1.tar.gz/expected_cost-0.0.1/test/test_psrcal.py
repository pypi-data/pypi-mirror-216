import matplotlib.pyplot as plt
import numpy as np
from expected_cost import ec, utils
from expected_cost.data import create_scores_for_expts
from expected_cost.psrcal_wrappers import LogLoss

num_targets = 2
score_dict, targets = create_scores_for_expts(num_targets, calibrate=False, score_scale_mc2=0.2)

print("Cross-entropy on simulated scores")

scores = score_dict['cal']['Datap']
print("Cross-entropy score for calibrated posteriors: %.2f"% LogLoss(scores, targets))

scores = score_dict['cal']['Mismp']
print("Cross-entropy score for miscalibrated posteriors due to mismatched priors: %.2f"% LogLoss(scores, targets))

scores = score_dict['mc2']['Datap']
print("Cross-entropy score for miscalibrated posteriors due to simulated overfitting: %.2f"% LogLoss(scores, targets))
