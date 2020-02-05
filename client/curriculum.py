from random import random

def curriculum_learning(object):
    """Curriculum training for better generalization, currently implemented in
    an ad-hoc method. This only serves as proof of concept"""

    # These are the experiment/pose index pairs that the agent should be
    # trained on in sequence [experiment, pose]
    # The brackets are done as a hacky way to get the length of each sets
    # eg: curriculum_training_set[current_set][specific_example][element]
    # 1) current_set is eg: [[1, 1], [2, 5], [2, 9]],
    # 2) specific_example is eg: [2, 5] from (1), eq to 0 if only 1 element
    # 3) element is eg: 2 from (2)
    curriculum_training_set = [[[1, 1]],
                               [[2, 5]],
                               [[2, 9]],
                               [[1, 1], [2, 5], [2, 9]]]

    # The distance to goal the agent achieved last time. Success in the Carla
    # Reward is set to within 2.0 from the actual goal. In this case, if the
    # vehicle is able to reach within the   close_enough   range, it changes
    # experiment to train the agent on the next set of experiment.
    close_enough = 5.0
    if object.last_distance_to_goal is None:
        # Arbitrary number for initial
        current_distance_to_goal = 100.0
    else:
        current_distance_to_goal = object.last_distance_to_goal

    if (current_distance_to_goal < close_enough) and \
       (object.current_set != len(curriculum_training_set)-1):
        object.current_set += 1

    # This is the total number of possible experiments in the selected set.
    # This is used to randomize the experiments from a set with more than 1
    # possible experiment.
    total_diff_exp = len(curriculum_training_set[object.current_set])

    # No need to randomize
    if total_diff_exp == 1:
        exp_idx = curriculum_training_set[object.current_set][0][0]
        idx_pose = curriculum_training_set[object.current_set][0][1]
    # Pick one of the preselected ones at random
    else:
        exp_idx = curriculum_training_set[object.current_set][int(random()*total_diff_exp)][0]
        idx_pose = curriculum_training_set[object.current_set][int(random()*total_diff_exp)][1]

    return exp_idx, idx_pose
