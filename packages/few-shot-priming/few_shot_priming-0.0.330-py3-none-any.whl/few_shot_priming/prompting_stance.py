import logging
import random

import pandas as pd
import openprompt
import os
import torch
import wandb

from argparse import ArgumentParser
from sklearn.metrics import accuracy_score
from openprompt.prompts import ManualTemplate, ManualVerbalizer
from openprompt import PromptForClassification, PromptDataLoader
from openprompt.plms import load_plm
from openprompt.data_utils import InputExample

from sklearn.metrics import accuracy_score, f1_score
from transformers import AdamW, get_linear_schedule_with_warmup, GPTJForCausalLM
from transformers import BertTokenizer, BertModel, T5Tokenizer, T5Model, AutoTokenizer, AutoModelForCausalLM
from transformers import DebertaModel, DebertaTokenizer, GPT2Tokenizer, GPT2Model, GPT2LMHeadModel, DebertaForSequenceClassification
from transformers import OPTConfig, OPTModel, BertForSequenceClassification, AutoModelWithLMHead, LlamaTokenizer
from torch.nn import CrossEntropyLoss

from few_shot_priming.config import *
from few_shot_priming.experiments import *
from few_shot_priming.mylogging import *
use_cuda = torch.cuda.is_available()


def convert_to_prompt_splits(dataset, config, sample=True):
    """
    Conver the pandas dataframes to splits as specified by the openprompt api
    :param dataset: a dictionary containing the trianing, validation, and test dataframes
    :return: a dictionary containing lists of input examples as specified by the openprompt api
    """
    prompt_splits = {}
    prompt_splits["test"] = []
    prompt_splits["training"] = []
    prompt_splits["validation"] = []
    for key in dataset.keys():
        if key == "training" and sample:
                dataset["training"] = sample_few_shots(dataset["training"], config["few-shot-size"])
        for i,record in dataset[key].iterrows():
            prompt_splits[key].append(InputExample(guid= i , text_a = record["text"], text_b = record["topic"], label = record["stance"]))
    return prompt_splits


def save_pre_trained_model():
    """
    Saving pretrained model to use huggingface transformers without internet
    """
    config = load_config()
    config = config["pre-trained-models"]
    path = Path(config["path"])
    bert_path = os.path.join(path,"bert-base-uncased")
    if not os.path.exists(bert_path):
        bert = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        berttokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        bert.save_pretrained(bert_path)
        berttokenizer.save_pretrained(bert_path)


    gpt_2_path = os.path.join(path, "gpt2-xl")
    if not os.path.exists(gpt_2_path):
        gpt_2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2-xl')
        gpt_2_model = GPT2Model.from_pretrained('gpt2-xl')
        gpt_2_model.save_pretrained(gpt_2_path)
        gpt_2_tokenizer.save_pretrained(gpt_2_path)

    deberta_path = os.path.join(path, "microsoft/deberta-base")
    if not os.path.exists(deberta_path):
        deberta_tokenizer = DebertaTokenizer.from_pretrained("microsoft/deberta-base")
        deberta_model = DebertaForSequenceClassification.from_pretrained("microsoft/deberta-base")
        deberta_tokenizer.save_pretrained(deberta_path)
        deberta_model.save_pretrained(deberta_path)
    alpaca_path  = os.path.join(path, "wxjiao/alpaca-7b")

    if not os.path.exists(alpaca_path):
        alpaca_tokenizer = LlamaTokenizer.from_pretrained("wxjiao/alpaca-7b")
        alpaca_model = AutoModelForCausalLM.from_pretrained("wxjiao/alpaca-7b")
        alpaca_tokenizer.save_pretrained(alpaca_path)
        alpaca_model.save_pretrained(alpaca_path)

def create_few_shot_model(config, experiment, offline=True):
    """
    Prepare an openprompt model based on the configuration
    :param config: a dictionary specifing the name and type of the model
    :return: an openprompt modle, a wrapper class, a tokenizer, and a template
    """
    model_name = config["model-name"]

    if offline:
        model_type = Path(config["model-path"])
    else:
        model_type = config["model-type"]
    if experiment == "vast":
        classes = [0, 1, 2]
        label_words = {0: ["con"], 1: ["pro"], 2 : ["neutral"]}
    else:
        classes = [0, 1]
        label_words = {0: ["con"], 1: ["pro"]}
    plm, tokenizer, model_config, WrapperClass = load_plm(model_name, model_type)

    promptTemplate = ManualTemplate(
        text = 'On the topic {"placeholder":"text_b"} the argument {"placeholder":"text_a"} has the stance {"mask"}.',
        tokenizer = tokenizer,
    )
    promptVerbalizer = ManualVerbalizer(
        classes = classes,
        label_words = label_words,
        tokenizer = tokenizer,
    )
    promptModel = PromptForClassification(template = promptTemplate, plm=plm, verbalizer=promptVerbalizer, freeze_plm=False)
    if use_cuda:
        promptModel = promptModel.cuda()
    return promptModel, WrapperClass, tokenizer, promptTemplate


def run_experiment_prompting(config=None, experiment="ibmsc", offline=False, validate=True, splits=None):
    save_pre_trained_model()
    few_shot_size = config["few-shot-size"]
    labels_text_map = {1: ["pro" ], 0: ["con"], 2: ["neutral"] }
    if offline:
        model_name = config["model-path"]
    else:
        model_name = config["model-name"]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    if not splits:
        splits = load_splits(experiment)
        training_dataset = splits["training"].sample(few_shot_size)
    else:
        training_dataset = splits["training"]
    if validate:
        test_dataset = splits["validation"]
    else:
        test_dataset = splits["test"]
    prompt = "Given are the following examples:\n"
    for i, record in training_dataset.iterrows():
        sentence = record["text"]
        if len(sentence) > 1000:
            sentence = sentence[:1000]
        topic = record["topic"]
        stance = record["stance"]
        label = labels_text_map[stance]
        idx = random.randint(0, len(label)-1)
        stance_text = label[idx]
        print(f"{stance} --> {stance_text}")
        template = f"On the topic {topic} the argument {sentence} has the stance {stance}\n"
        prompt = prompt + template
    predictions = []
    #test_dataset = test_dataset.sample(10)
    labels = []
    for i, record in test_dataset.iterrows():
        sentence = record["text"]
        topic = record["topic"]
        label = record["stance"]
        template_no_stance = f"On the topic {topic} the argument {sentence} has the stance"
        prompt_to_predict = prompt + template_no_stance
        seq = tokenizer.encode(prompt_to_predict, return_tensors="pt")
        generated = model.generate(seq, max_new_tokens=3)
        resulting_string = tokenizer.decode(generated.tolist()[0])
        if "pro" in resulting_string[-15:].lower() or "supports" in resulting_string[-15:].lower() or "positive" in resulting_string[-15:].lower():
            predictions.append(1)
        elif "con" in resulting_string[-15:].lower():
            predictions.append(0)
        else:
            predictions.append(2)
        labels.append(label)
    accuracy = accuracy_score(labels, predictions)
    if experiment == "vast":
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1, 2])
        neutral_f1 = f1s[2]
    else:
        f1s = f1_score(labels, predictions, average=None, labels=[0, 1])
        neutral_f1 = 0
    con_f1 = f1s[0]
    pro_f1 = f1s[1]

    macro_f1 = f1_score(labels, predictions, average="macro")

    return accuracy, pro_f1, con_f1, neutral_f1, macro_f1

def run_experiment_prompt_fine_tuning(config=None, experiment="ibmsc", params=None, offline=False, validate=True, splits=None, logger = None):
    """
    Run a validation experiment or a test experiment
    :param validate: a boolean flag specifying whether to run a validation or  test experiment
    :return:
    """
    if offline:
        save_pre_trained_model()
    batch_size = params["batch-size"]
    lr = params["learning-rate"]
    epochs_num = params["epochs"]
    if not splits:
        splits = load_splits(experiment)
        prompt_dataset = convert_to_prompt_splits(splits, config)
    else:
        prompt_dataset = convert_to_prompt_splits(splits, config, sample=False)
    promptModel, WrapperClass, tokenizer, promptTemplate = create_few_shot_model(config, experiment=experiment, offline=offline)
    train_data_loader = PromptDataLoader(dataset = prompt_dataset["training"], tokenizer=tokenizer, template=promptTemplate,
        tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
    if validate:
        experiment_type = "validate"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["validation"], tokenizer = tokenizer, template = promptTemplate,
            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)
    else:
        experiment_type = "test"
        test_data_loader = PromptDataLoader(dataset = prompt_dataset["test"], tokenizer = tokenizer, template = promptTemplate,
            tokenizer_wrapper_class=WrapperClass, batch_size=batch_size, truncate_method="head", max_seq_length=256, decoder_max_length=3)

    loss_func = CrossEntropyLoss()
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in promptModel.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in promptModel.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]

    optimizer = AdamW(optimizer_grouped_parameters, lr=float(lr))
    metrics = {}
    for epoch in range(epochs_num):
        tot_loss = 0
        for step, inputs in enumerate(train_data_loader):
            if use_cuda:
                inputs = inputs.cuda()
            promptModel.train()
            logits = promptModel(inputs)
            labels = inputs["label"]
            loss = loss_func(logits, labels)
            loss.backward()
            tot_loss += loss.item()
            optimizer.step()
            optimizer.zero_grad()
            if step % 100 == 1:
                log_message(logger, "Epoch {}, average loss: {}".format(epoch, tot_loss/(step+1)), level=logging.INFO)
            metrics["train/loss"] = tot_loss/(step+1)
            wandb.log(metrics)
        promptModel.eval()
        test_loss = 0
        all_test_labels = []
        all_test_preds = []
        for step, test_inputs in enumerate(test_data_loader):
            if use_cuda:
                test_inputs = test_inputs.cuda()
            test_logits = promptModel(test_inputs)
            test_labels = test_inputs["label"]
            all_test_labels.extend(test_labels.cpu().tolist())
            all_test_preds.extend(torch.argmax(test_logits, dim = -1).cpu().tolist())
            loss = loss_func(test_logits, test_labels)
            test_loss += loss.item()
            metrics[f"{experiment_type}/loss"] = test_loss/(step+1)
            wandb.log(metrics)
        metrics[f"{experiment_type}/accuracy"] = accuracy_score(all_test_labels, all_test_preds)
        if experiment == "vast":
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1, 2])
            neutral_f1 = f1s[2]
        else:
            f1s = f1_score(all_test_labels, all_test_preds, average=None, labels=[0, 1])
            neutral_f1 = 0
        con_f1 = f1s[0]
        pro_f1 = f1s[1]
        macro_f1 = f1_score(all_test_labels, all_test_preds, average="macro")
        metrics[f"{experiment_type}/pro-f1"] = pro_f1
        metrics[f"{experiment_type}/con-f1"] = con_f1
        metrics[f"{experiment_type}/neutral-f1"] = neutral_f1
        metrics[f"{experiment_type}/macro-f1"] = macro_f1
        wandb.log(metrics)
    log_metrics(logger, metrics, level=logging.WARNING)
    metrics["score"] = metrics[f"{experiment_type}/accuracy"]
    wandb.log(metrics)

    return metrics["score"]