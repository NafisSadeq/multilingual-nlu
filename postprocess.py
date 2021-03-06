import re
import torch
import json

def calculateF1(predict_golden,type):
    TP, FP, FN = 0, 0, 0
    for item in predict_golden:
        predicts = item['predict']
        labels = item['golden']
        if(type=="tag"):
            predicts = [[x[0], x[1], x[2].lower()] for x in predicts]
            labels = [[x[0], x[1], x[2].lower()] for x in labels]
        for ele in predicts:
            if ele in labels:
                TP += 1
            else:
                FP += 1
        for ele in labels:
            if ele not in predicts:
                FN += 1
    precision = 1.0 * TP / (TP + FP) if TP + FP else 0.
    recall = 1.0 * TP / (TP + FN) if TP + FN else 0.
    F1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.
    return precision, recall, F1

def calculateF1perIntent(predict_golden):
    TP={}
    FP={}
    FN={}
    precision={}
    recall={}
    F1={}
    item_set={}
    for item in predict_golden:
        predicts = item['predict']
        labels = item['golden']
        for ele in predicts:
            item_set[ele]=1
            if ele in labels:
                if ele not in TP:
                    TP[ele]=1
                else:
                    TP[ele]+=1
            else:
                if ele not in FP:
                    FP[ele]=1
                else:
                    FP[ele]+=1
        for ele in labels:
            item_set[ele]=1
            if ele not in predicts:
                if ele not in FN:
                    FN[ele]=1
                else:
                    FN[ele]+=1
    for key,value in item_set.items():
        if(key not in TP):
            TP[key]=0
        if(key not in FP):
            FP[key]=0
        if(key not in FN):
            FN[key]=0      
        precision[key] = 1.0 * TP[key] / (TP[key] + FP[key]) if (TP[key]+ FP[key]) else 0.
        recall[key] = 1.0 * TP[key] / (TP[key] + FN[key]) if ((TP[key]+ FN[key])) else 0.
        F1[key] = 2.0 * precision[key] * recall[key] / (precision[key] + recall[key]) if precision[key] + recall[key] else 0.
    
    return precision, recall, F1

def calculateF1perSlotCLS(predict_golden):
    TP={}
    FP={}
    FN={}
    precision={}
    recall={}
    F1={}
    item_set={}
    for item in predict_golden:
        predicts = item['predict']
        labels = item['golden']
        for ele in predicts:
            item_set[ele]=1
            if ele in labels:
                if ele not in TP:
                    TP[ele]=1
                else:
                    TP[ele]+=1
            else:
                if ele not in FP:
                    FP[ele]=1
                else:
                    FP[ele]+=1
        for ele in labels:
            item_set[ele]=1
            if ele not in predicts:
                if ele not in FN:
                    FN[ele]=1
                else:
                    FN[ele]+=1
    for key,value in item_set.items():
        if(key not in TP):
            TP[key]=0
        if(key not in FP):
            FP[key]=0
        if(key not in FN):
            FN[key]=0      
        precision[key] = 1.0 * TP[key] / (TP[key] + FP[key]) if (TP[key]+ FP[key]) else 0.
        recall[key] = 1.0 * TP[key] / (TP[key] + FN[key]) if ((TP[key]+ FN[key])) else 0.
        F1[key] = 2.0 * precision[key] * recall[key] / (precision[key] + recall[key]) if precision[key] + recall[key] else 0.
    # precision, recall, F1=filter_dict(precision, recall, F1)
    return precision, recall, F1

def calculateF1perSlot(predict_golden):
    TP={}
    FP={}
    FN={}
    precision={}
    recall={}
    F1={}
    item_set={}
    for item in predict_golden:
        predicts = item['predict']
        predicts = [[x[0], x[1], x[2].lower()] for x in predicts]
        labels = item['golden']
        labels = [[x[0], x[1], x[2].lower()] for x in labels]
        for ele in predicts:
            ele_str=ele[0].split('+')[0]+"+"+ele[1]
            item_set[ele_str]=1
            if ele in labels:
                if ele_str not in TP:
                    TP[ele_str]=1
                else:
                    TP[ele_str]+=1
            else:
                if ele_str not in FP:
                    FP[ele_str]=1
                else:
                    FP[ele_str]+=1
        for ele in labels:
            ele_str=ele[0].split('+')[0]+"+"+ele[1]
            item_set[ele_str]=1
            if ele not in predicts:
                if ele_str not in FN:
                    FN[ele_str]=1
                else:
                    FN[ele_str]+=1
    for key,value in item_set.items():
        if(key not in TP):
            TP[key]=0
        if(key not in FP):
            FP[key]=0
        if(key not in FN):
            FN[key]=0      
        precision[key] = 1.0 * TP[key] / (TP[key] + FP[key]) if (TP[key]+ FP[key]) else 0.
        recall[key] = 1.0 * TP[key] / (TP[key] + FN[key]) if ((TP[key]+ FN[key])) else 0.
        F1[key] = 2.0 * precision[key] * recall[key] / (precision[key] + recall[key]) if precision[key] + recall[key] else 0.
    # precision, recall, F1=filter_dict(precision, recall, F1)
    return precision, recall, F1

def tag2triples(word_seq, tag_seq):
    word_seq = word_seq[:len(tag_seq)]
    assert len(word_seq)==len(tag_seq)
    triples = []
    i = 0
    while i < len(tag_seq):
        tag = tag_seq[i]
        if tag.startswith('B'):
            intent, slot = tag[2:].split('+')
            value = word_seq[i]
            j = i + 1
            while j < len(tag_seq):
                if tag_seq[j].startswith('I') and tag_seq[j][2:] == tag[2:]:
                    value += ' ' + word_seq[j]
                    i += 1
                    j += 1
                else:
                    break
            triples.append([intent, slot, value])
        i += 1
    return triples


def intent2triples(intent_seq):
    triples = []
    for intent in intent_seq:
        intent, slot, value = re.split('[+*]', intent)
        triples.append([intent, slot, value])
    return triples


def recover_intent(dataloader, intent_logits):
    intents = []
    for j in range(dataloader.intent_dim):
        if intent_logits[j] > 0:
            intent= dataloader.id2intent[j]
            intents.append(intent)
    return intents

def recover_slot(dataloader, slot_logits):
    slots = []
    for j in range(dataloader.slot_dim):
        if slot_logits[j] > 0:
            slot= dataloader.id2slot[j]
            slots.append(slot)
    return slots

def recover_tag(dataloader, intent_logits, tag_logits, tag_mask_tensor, ori_word_seq, new2ori):
    # tag_logits = [sequence_length, tag_dim]
    # intent_logits = [intent_dim]
    # tag_mask_tensor = [sequence_length]
    # new2ori = {(new_idx:old_idx),...} (after removing [CLS] and [SEP]
    max_seq_len = tag_logits.size(0)
    tags = []
    for j in range(1, max_seq_len-1):
        if tag_mask_tensor[j] == 1:
            value, tag_id = torch.max(tag_logits[j], dim=-1)
            tags.append(dataloader.id2tag[tag_id.item()])
    
    tag_intent = tag2triples(ori_word_seq, tags)

    return tag_intent
