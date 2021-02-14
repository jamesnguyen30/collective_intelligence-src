from math import log

class DecisionNode:

    def __init__(self, column = None, value = None, results = None, true_branch = None, false_branch = None):
        self.column = column
        self.results = results
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.value = value

class TreeBuilder:

    def __init__(self):
        pass
    
    def divide_set(self, data, column, value):
        ''' returns a tuple contains true_set and false_set''' 
        if isinstance(value, int) or isinstance(value, float):
            split_func = lambda row: row[column] >= value
        else:
            split_func = lambda row: row[column] == value

        true_set = []
        false_set = []

        for row in data:
            if split_func(row):
                true_set.append(row)
            else:
                false_set.append(row)
        return (true_set, false_set)

    def membership_counts(self, data):
        ''' returns a dictionary, ex: results = {'value_type' : 3, .... }'''
        results = {}
        
        if len(data)==0:
            return results

        last_index = len(data[0])-1

        for row in data:
            try:
                value = row[last_index]
            except IndexError as e:
                print(str(e))
                print(str(row) + ", " + str(last_index))

            results.setdefault(value, 0)
            results[value] += 1

        return results

    def entropy(self, data):
        entropy = 0
        log2 = lambda x: log(x) / log(2)
        memberships = self.membership_counts(data)
        for feature in memberships.keys():
            p_i = memberships[feature] / len(data)
            entropy -= p_i * log2(p_i)
        return entropy

    def recursive_build_tree(self, data, scoref = entropy):
        #check if the recursive data is None,
        #assign it to the data of the class
        #this happens when user calls this method
        #but since it's a recursive function
        #we need to have recursive_data parameter 

        
        if len(data) == 0:
            return DecisionNode()
        
        current_score = scoref(self, data)

        #track best criterias
        best_gain = 0
        best_column_and_value = None
        best_sets = None

        #get all the columns but exclude the final column
        #because we want the tree to come to that decision
        number_of_columns = len(data[0])-1
        
        for col_index in range(number_of_columns):
            #get all the values in this column
            col_values = {}
            for row in data:
                col_values.setdefault(row[col_index],0)
                col_values[row[col_index]] = 1

            for value in col_values.keys():
                (true_set, false_set) = self.divide_set(data, col_index, value)

                #calculate information gain
                #and choose the one with highest information gain
                p = float(len(true_set)/ len(data))
                gain = current_score - p*scoref(self, true_set) - (1-p)*scoref(self, false_set)

                if gain>best_gain and len(true_set)>0 and len(false_set)>0:
                    best_gain = gain
                    best_column_and_value = (col_index, value)
                    best_sets = (true_set, false_set)
        
        if best_gain>0:
            true_set = self.recursive_build_tree(best_sets[0])
            false_set = self.recursive_build_tree(best_sets[1])
            return DecisionNode(column= best_column_and_value[0], value = best_column_and_value[1], true_branch= true_set, false_branch= false_set)
        else:
            return DecisionNode(results= self.membership_counts(data))
    
    def print_tree(self, tree,indent = ''):
        # is this a leaf node?
        if tree.results!=None:
            print(str(tree.results))
        # this is not a leaf node, 
        # recursively call print_tree function 
        else:
            print("{} : {} ?".format(tree.column, tree.value))
            print(indent + 'T ->', end = '')
            self.print_tree( tree.true_branch, indent + ' ')
            print(indent + 'F ->', end = '')
            self.print_tree(tree.false_branch, indent + ' ')

class TreeClassifer:
    def __init__(self):
        pass
    
    def classify(self, data_point, tree):
        if tree.results!=None:
            return tree.results
        else:
            value = data_point[tree.column]
            branch = None
            if isinstance(value, int) or isinstance(value, float):
                if value>tree.value:
                    branch = tree.true_branch
                else:
                    branch = tree.false_branch
            else:
                if value == tree.value:
                    branch = tree.true_branch
                else:
                    branch = tree.false_branch
            return self.classify(data_point, branch)


        
        






        


