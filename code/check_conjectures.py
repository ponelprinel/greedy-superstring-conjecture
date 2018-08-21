import hierarchical_graph
import graph_drawer
import networkx as nx
from random import randint
from exact_solution import shortest_superstring


test_number = 1
separator = '--------'


def compare_graphs(g, h):
    return nx.difference(g, h).number_of_edges() == 0 and \
           nx.difference(h, g).number_of_edges() == 0


def log(input_strings, exact_sol, hier_sol):
    return "%s\nExact Solution has length %d:\n%s\nGreedy Hierarchical Solution has length %d:\n%s\n\n"\
           % (input_strings, len(exact_sol), exact_sol, len(hier_sol), hier_sol)


def log_counter_example(log_file, input_strings, exact_sol, hier_sol, description):
    with open(log_file, 'a+') as output_file:
        output_file.write(description+'\n')
        output_file.write(log(input_strings, exact_sol, hier_sol))


def log_counter_examples(log_file, input_strings, exact_sol, hier_sol, hier_graph, exact_graph, trivial_graph):
    counter_example = False
    if len(hier_sol) >= 2 * len(exact_sol):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution is twice longer than the optimal one')
        counter_example = True
    if not compare_graphs(hier_graph, exact_graph):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution does not equal the collapsed exact solution')
        counter_example = True
    if not compare_graphs(hier_graph, trivial_graph):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution does not equal the collapsed trivial solution')
        counter_example = True
    return counter_example


def check(log_file, strings):
    global test_number
    global separator
    print('Test # {}'.format(test_number))
    for string in strings:
        print(string)
    test_number += 1
    drawer = graph_drawer.GraphDrawer(strings, 'output', False, True)
    hier_sol, hier_graph = hierarchical_graph.construct_greedy_solution(strings, drawer)

    opt_permutation = shortest_superstring(strings)
    opt_strings = [strings[i] for i in opt_permutation]
    exact_sol, exact_graph = hierarchical_graph.collapse_for_permutation(opt_strings, drawer)

    trivial_sol, trivial_graph = hierarchical_graph.collapse_for_permutation(strings, drawer)

    if log_counter_examples(log_file, strings, exact_sol, hier_sol, hier_graph, exact_graph, trivial_graph):
        print('\nCounter-example found!\n{}'.format(separator))
        return True
    else:
        print('\nGood\n{}'.format(separator))


def check_dataset(log_file, dataset_file='../web/static/datasets.txt'):
    print('Checking dataset from file {}\n'.format(dataset_file))
    counter_example = False
    with open(dataset_file, 'r') as presets_file:
        presets = presets_file.readlines()
        presets = [x.strip() for x in presets]
        for preset in presets:
            counter_example = check(log_file, preset.split(' ')) and counter_example
    if counter_example:
        print('\nCounter-example found!')
    else:
        print('\nNo counter-examples found!')


def check_input(strings):
    n = len(strings)
    for i in range(n):
        for j in range(n):
            if (i != j) and (strings[i].find(strings[j]) >=0):
                return False
    return True


def random_input():
    alphabet_size = randint(2, 5)
    length = randint(10, 25)
    superstring = ''
    for _ in range(length):
        superstring += chr(ord('a') + randint(0, alphabet_size - 1))
    start = 0
    end = randint(3, 7)
    strings = []
    while end <= len(superstring):
        strings.append(superstring[start:end+1])
        start = randint(start + 1, end)
        end = end + randint(1, 3)
    if not check_input(strings):
        return random_input()
    return strings


def check_random(log_file, number_of_tests):
    print('Checking {} random inputs\n'.format(number_of_tests))
    counter_example = False
    for _ in range(number_of_tests):
        counter_example = check(log_file, random_input()) and counter_example
    if counter_example:
        print('\nCounter-example found!')
    else:
        print('\nNo counter-examples found!')


log_file = 'counter-examples.txt'
#check_dataset(log_file)
s = 'aaaaa'
check_random(log_file, 1)