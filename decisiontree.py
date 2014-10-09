#import dTree_ID3 as dt_id3
from __future__ import division
from math import log

import csv
import sys
import random
import copy
#from __future__ import division # enable integer division to create float
#pass commandline argument to decisiontree
def read_commandline():
    instance = {}
    instance_list = []
    if len(sys.argv) != 5:
        print "wrong usage"
        return
    else:
        inputFileName = sys.argv[1]
        #print inputFileName
        trainingSetSize = sys.argv[2]
        numberOfTrials = sys.argv[3]
        verbose = sys.argv[4]

    #read instance from example
    with open('%s' % inputFileName,'rb') as csvfile:
        #if 'IvyLeague.txt' in inputFileName:
        spamreader = csv.reader(csvfile,delimiter='\t')
        #create an attribute_list to store the attribute
        attribute_list = spamreader.next()
        #.next() returns a list of string
        # print attribute_list
        attribute_list = ','.join(attribute_list)
        attribute_list = attribute_list.replace(" ","")
        attribute_list = attribute_list.split(",")
        # print attribute_list

        #create dictionary_list to store all the instances
        for row in spamreader:
            #print row
            #could use join to create a string,then use split to create list
            if 'IvyLeague.txt' in inputFileName:
                rowData = ''.join(row).split(' ')
                # print rowData
            else:
                rowData = ' '.join(row).split(' ')
            #range could only go from 0 to len(rowData) - 1
            for i in range(0,len(rowData)):
                #print rowData
                if rowData[i] == "true":
                    #print i
                    instance[attribute_list[i]] = bool(1)

                    #print attribute_list[i]
                else:
                    instance[attribute_list[i]] = bool(0)
                #print instance
            instance_list.append(instance.copy())

        #randome generate training set and test set
        train = []
        test = []
        #python force the type to int;
        # print 'trainingsize'
        # print int(trainingSetSize)

        random.shuffle(instance_list)

        for i in range(0,int(trainingSetSize)):
            train.append(instance_list[i])
            #print idx[i]
        #print len(train)
        for i in range(int(trainingSetSize)+1,len(instance_list)):
            #print i
            test.append(instance_list[i])

            #print test
            #flag += 1
            #instance_list[idx[i]]
            #print 'removed'
            #print idx[i]

        #print "instancelist:",instance_list
        #print test

        #print test
        sum_decision = 0
        sum_res = 0
        for i in range(0,int(numberOfTrials)):
            print 'TRIAL NUMBER:%d' % i
            tree = build_Tree(train, attribute_list)
            decision_res = decision_classify(test,tree)
            prob_result = calculate_priorprob(train)
            prob_res = priorprob_classify(test, prob_result)
            sum_decision += decision_res
            sum_res += prob_res
        print sum_res,'sum_res',sum_decision,'sum_decision'
        mean_decision = round(sum_decision / int(numberOfTrials),1)
        mean_prob = round(sum_res / int(numberOfTrials) ,1)
        print mean_decision,'mean_decision',mean_prob,'mean_prob'
        if verbose == '1':
            print 'example file used = %s' %inputFileName
            print 'number of trials = %s' %numberOfTrials
            print 'train set size for each trial = %d' %len(train)
            print 'testing set size for each trial = %d' %len(test)
            lists = []
            lists.append("mean performance of decision tree over all trials = %d" % mean_decision)
            lists.append('% ')
            lists.append('correct classification')
            print ''.join(lists)
            prob_lists = []
            prob_lists.append("mean performance of using prior probability derived from the training set = %d" % mean_prob)
            prob_lists.append('% ')
            prob_lists.append('correct classification')
            print ''.join(prob_lists)






#calculate the priorprob
def calculate_priorprob(train):
    total_num = len(train)
    true_num = 0
    for ele in train:
        true_num += ele['CLASS']
    prob = true_num / total_num
    if prob >= 0.5:
        return bool(1)
    else:
        return bool(0)

#seperate the list
def seperate_list(total_list,attribute):
    sub_list_1 = []
    sub_list_2 = []
    for dic_list in total_list:
        if dic_list[attribute] == bool(1):
            sub_list_1.append(dic_list.copy())
        else:
            sub_list_2.append(dic_list.copy())
    return sub_list_1,sub_list_2

#calculate entropy
def calculate_entropy(lists,attribute):
    entropy = 0.0
    total = len(lists)
    p = 0
    #print 'attrL:',attribute
    for ele in lists:
        p = p + ele[attribute]

    #base case for decision_tree
    if p == 0 or p == total:
        return 0
    p_pos = p / total
    p_neg = 1 - p_pos
    #print p_pos,p_neg
    entropy = -p_pos*log(p_pos,2) - p_neg*log(p_neg,2)
    #print "entr:",entropy
    #print "lists:",lists,"attribute:",attribute
    return entropy

#calculate information gain
def calculate_infogain(total_list,list_attribute):
    info_gain = 0.0
    total = len(total_list)
    subset1,subset2 = seperate_list(total_list,list_attribute)
    info_gain = calculate_entropy(total_list,'CLASS') - len(subset1)/total * calculate_entropy(subset1,'CLASS') - len(subset2)/total * calculate_entropy(subset2,'CLASS')
    return info_gain

def getAttribute(rows,attribute_list):
    max_gain = 0
    best_attribute = 'none'
    for i in range(0,len(attribute_list)-1):
        gain = calculate_infogain(rows,attribute_list[i])
        if gain > max_gain:
            max_gain = gain
            best_attribute = attribute_list[i]
    #print "best_attrib",best_attribute
    return best_attribute

def build_Tree(train_set,attribute_list):
    tree_list = {}
    attribute = 'root'
    tree_list = buildTree(train_set,attribute_list,tree_list,attribute)
    #print tree_list
    print_tree(tree_list)
    return tree_list

def buildTree(train_set,attribute_list,tree_list,attribute):
    #print train_set
    #print "tree_first:",calculate_entropy(train_set,'CLASS')
    #base case: instances are all the same
    if calculate_entropy(train_set,'CLASS') == 0:
        #print "wrong",train_set,attribute
        tree_list['parent'] = attribute
        tree_list['attribute'] = 'leaf'
        tree_list['result'] = train_set[0]['CLASS']
        return tree_list
    else:
        #print calculate_entropy(train_set,'CLASS')
        #print attribute
        tree_list['parent'] = attribute
        #print tree_list['parent']
        #print "get_attribute:",getAttribute(train_set,attribute_list)
        attribute = getAttribute(train_set, attribute_list)
        tree_list['attribute'] = attribute
        #print tree_list['attribute']
        sub_list1,sub_list2 = seperate_list(train_set,attribute)
        #print attribute
        tree_list['trueChild'] = buildTree(sub_list1, attribute_list,{}, attribute)
        tree_list['falseChild'] = buildTree(sub_list2, attribute_list,{}, attribute)
        return tree_list

def print_tree(tree_list):
    #print tree_list
    if tree_list['attribute'] == 'leaf':
        #print 0
        print "parent:",tree_list['parent']
    else:
        print "parent:",tree_list['parent'],"attribute:",tree_list['attribute'],"trueChile:",tree_list['trueChild']['attribute'],"falseChild:",tree_list['falseChild']['attribute']
        print_tree(tree_list['trueChild'])
        print_tree(tree_list['falseChild'])

     
def decision_classify(train,tree):
    total = len(train)
    right = 0
    for instance in train:
        current = tree
        while current['attribute'] != 'leaf':
            if instance[current['attribute']] == False:
                current = current['falseChild']
            else:
                current = current['trueChild']
        #print tree
        if current['result'] == instance['CLASS']:
            right = right + 1
        #print right
    # print right
    # print total,'total'
    prob = round(right / total * 100,1)
    lists = []
    lists.append("Percent of test cases correctly classified by a decision tree build with = %d" % prob)
    lists.append('%')
    print ''.join(lists)
    return prob

def priorprob_classify(test,prob_result):
    correct_num = 0
    total_num = len(test)
    #print "prob_result:",prob_result
    #print total_num

    for t in test:
        #print t
        if t['CLASS'] == bool(1):
            correct_num = correct_num + 1
    #print "correct_num",correct_num
    result = correct_num / total_num * 100
    #print result
    result = round(result)
    #print result
    lists = []
    lists.append("Percent of test cases correctly classified by using prior probabilities from the training set = %d" % result)
    lists.append('%')
    print ''.join(lists)
    return result




def main():
    read_commandline()

if __name__ == '__main__':
    main()

