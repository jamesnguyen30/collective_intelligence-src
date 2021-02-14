from tree_builder import TreeBuilder, DecisionNode, TreeClassifer

data=[
        ['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']
    ]

if __name__ == "__main__":
    tree_builder = TreeBuilder()
    tree = tree_builder.recursive_build_tree(data)  
    # tree_builder.print_tree(tree)

    tree_classifier = TreeClassifer()
    print(tree_classifier.classify( ['kiwitobes','France','yes',19,'Basic'], tree))
