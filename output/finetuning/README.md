---
license: apache-2.0
tags:
- generated_from_trainer
model-index:
- name: finetuning
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# finetuning

This model is a fine-tuned version of [facebook/bart-base](https://huggingface.co/facebook/bart-base) on the SCITLDR dataset.
It achieves the following results on the evaluation set:
- Loss: 5.2490

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 4
- eval_batch_size: 4
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 3.0

### Training results



### Framework versions

- Transformers 4.18.0
- Pytorch 1.10.2
- Datasets 2.1.0
- Tokenizers 0.12.1
