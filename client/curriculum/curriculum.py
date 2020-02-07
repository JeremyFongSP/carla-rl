from random import random
import yaml


def curriculum_learning(obj, file):
    """Curriculum training for better generalization, currently implemented in
    an ad-hoc method. This only serves as proof of concept. The obj argument
    refers to the CarlaEnv itself, file refers to the curriculum_to_follow.yaml"""

    # Reads curriculum_to_follow.yaml and organizes it into an array
    with open(file, 'r') as curr_file:
        yaml_list = yaml.safe_load(curr_file)

    curriculum_training_set = yaml_list['curr_list']

    # The distance to goal the agent achieved last time. Success in the Carla
    # Reward is set to within 2.0 from the actual goal. In this case, if the
    # vehicle is able to reach within the   close_enough   range, it changes
    # experiment to train the agent on the next set of experiment.
    close_enough = 5.0
    if obj.last_distance_to_goal is None:
        # Arbitrary number for initial
        current_distance_to_goal = 100.0
    else:
        current_distance_to_goal = obj.last_distance_to_goal

    if (current_distance_to_goal < close_enough) and \
       (obj.current_set != len(curriculum_training_set)-1):
        obj.current_set += 1

    # This is the total number of possible experiments in the selected set.
    # This is used to randomize the experiments from a set with more than 1
    # possible experiment.
    total_diff_exp = len(curriculum_training_set[obj.current_set])

    # No need to randomize
    if total_diff_exp == 1:
        exp_idx = curriculum_training_set[obj.current_set][0][0]
        idx_pose = curriculum_training_set[obj.current_set][0][1]
    # Pick one of the preselected ones at random
    else:
        exp_idx = curriculum_training_set[obj.current_set][int(random()*total_diff_exp)][0]
        idx_pose = curriculum_training_set[obj.current_set][int(random()*total_diff_exp)][1]

    return exp_idx, idx_pose
