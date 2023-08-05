import pandas as pd
import os
from few_shot_priming.config import *


def save_splits():
    """
    Save the splits of the experiments by sampling a validation set from the training set with exclusive topic sets
    :return:
    """
    path_source, path_training, path_validation, path_test = get_experiment_paths()
    df_arguments = pd.read_csv(path_source, sep=",", encoding="utf-8")
    df_training = df_arguments[df_arguments["split"] == "train"]
    df_test = df_arguments[df_arguments["split"] == "test"]
    training_topics = df_training["topicTarget"].sample(12).unique()
    training_topics = training_topics[:10]
    df_sampled_training = df_training[df_training["topicTarget"].isin(training_topics)]

    df_validation = df_training[~df_training["topicTarget"].isin(training_topics)]

    df_sampled_training.to_csv(path_training, sep=",", encoding="utf-8", index=False)
    df_validation.to_csv(path_validation, sep=",", encoding="utf-8", index=False)
    df_test.to_csv(path_test, sep=",", encoding="utf-8", index=False)


def oversample_dataset(df, experiment):
    if experiment == "ibmsc":
        pro_claims = df[df["claims.stance"]=="PRO"]
        con_claims = df[df["claims.stance"]=="CON"]
        count_of_con_to_sample = pro_claims.shape[0] - con_claims.shape[0]

        con_claims_to_add = con_claims.sample(count_of_con_to_sample)
        return pd.concat([df, con_claims_to_add])
    else:
        return df

def adapt_ibmsc(df):
    labels = {"PRO": 1, "CON":0}
    stances = [ labels[stance] for stance in df["claims.stance"].values]
    return zip(df["topicText"].values, df['claims.claimCorrectedText'].values, stances)

def adapt_vast(df):
    return zip(df["new_topic"], df["text_s"], df["label"])

def load_splits(experiment, oversample=True):
    """
    Load the splits of the experiments and return it in a dictionary of pandas dataframes
    :return: a dictionary containing the training, validation, and test splits
    """
    path_source, path_training, path_validation, path_test = get_experiment_paths(experiment)
    if experiment == "ibmsc" and not os.path.exists(path_validation):
        save_splits()
    df_training = pd.read_csv(path_training, sep=",", encoding="utf-8")
    df_validation = pd.read_csv(path_validation, sep=",", encoding="utf-8")
    df_test = pd.read_csv(path_test, sep=",", encoding="utf-8")
    dataset = {"training": df_training, "validation": df_validation, "test": df_test}
    if oversample:
        dataset["training"] = oversample_dataset(dataset["training"], experiment)
    for split in dataset:
        if experiment == "ibmsc":
            dataset[split] = adapt_ibmsc(dataset[split])
        else:
            dataset[split] = adapt_vast(dataset[split])
    return dataset


def sample_few_shots(df_training, size, filter = None, sort_criterion = None):
    """
    Sample few shots from the training dataframe. The few shots can be filtered by using a specific boolean functions and sorted
    :param df_training: a dataframe containing the whole training split
    :param size: the size of the few shots to use for training
    :param filter: a boolean function that takes a record of the trianing split and decided whether to include or not
    :param sort_criteria: a dicionary specifing the name of the column and the sorting order used to sort the few shot examples
    :return: a dataframe containing the sampled few shots
    """
    df_sample = df_training.sample(n=size)
    return df_sample


