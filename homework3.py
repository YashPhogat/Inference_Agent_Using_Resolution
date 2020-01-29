import re
import sys
# sys.setrecursionlimit(999)
file = open("input.txt" , "r")
query_length = int(file.readline())
query = []
for i in range(query_length) :
    query.append(file.readline().rstrip())

kb_length = int(file.readline())
kb = []
for i in range(kb_length) :
    kb.append(file.readline().rstrip())
# print(query,kb)

file.close()
cnf_kb = []
for item in kb :
    if "=>" in item :
        temp = item.split("=>")
        predicate = temp[0]
        con = temp[1].replace(' ', '')
        cnf = ""
        for p in predicate.strip().split() :
            p = p.replace(" ", "")
            if p[0] == "~" :
                cnf += p[1:]
            elif p[0] == "&" :
                cnf += "|"
            else :
                cnf += "~" + p
        cnf_kb.append(cnf.replace(" ", '') + "|" + con.replace(" ",''))
    else :
        cnf_kb.append(item.replace(' ',''))


def create_kb_dictionaries(cnf_kb) :
    positive_kb = {}
    negative_kb = {}
    for sentence in cnf_kb :

        predicates = sentence.split("|")
        for pred in predicates :
            pred = pred.replace(' ', '')
            if pred[0] == "~" :
                key = pred[1 :].partition("(")[0]
                if key in negative_kb :
                    negative_kb[key] += [sentence]
                else :
                    negative_kb[key] = [sentence]
            else :
                key = pred.partition("(")[0]
                if key in positive_kb :
                    positive_kb[key] += [sentence]
                else :
                    positive_kb[key] = [sentence]

    return positive_kb, negative_kb


def constant_predicates(cnf_kb) :
    resolvable = list()
    for pred in cnf_kb :

        if "|" not in pred :
            # print("hjbhh:", pred)
            inner_params = re.search("\(.*?\)", pred).group(0)[1 :-1]
            list_const = inner_params.split(",")
            # print(list_const)
            # list_const =
            #
            #
            #
            # list_const.replace(' ', '')
            if all(ch[0].isupper() for ch in list_const) :
                # print(resolvable)
                resolvable.append(pred)

    return resolvable



# print("CNF-KB: ", cnf_kb)
# print("Positive KB: ", positive_knowledge_base)
# print("Negative KB: ", negative_knowledge_base)

def replace1(variable, string, constant):
    replacements1 = {}
    # print(replacements)
    #   https://stackoverflow.com/questions/17730788/search-and-replace-with-whole-word-only-option
    replacements1 = {variable: constant}

    def ifmatch1(match):
        return replacements1[match.group(0)]

    # notice that the 'this' in 'thistle' is not matched
    return (re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements1),
                 ifmatch1, string))

replacement = dict()
def replace(variable, string, constant):
    global replacement
    # print(replacements)
    #   https://stackoverflow.com/questions/17730788/search-and-replace-with-whole-word-only-option

    if variable in replacement:
        replacement[replacement[variable]] = constant
    else:
        replacement[variable] = constant
    # for k, v in replacement.items():
    #     if str(k[0]).isupper() and str(v[0]).isupper() and k!=v:
    #         replacement[k] = k
    for k, v in replacement.items() :
        if str(k[0]).isupper():
            replacement[k] = k
    # print(replacement, string)

    def ifmatch(match):
        return replacement[match.group(0)]

    # notice that the 'this' in 'thistle' is not matched
    return (re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacement),
                 ifmatch, string))


def standardize_cnf(cnf_kb):
    standardized_cnf = []
    i = 0
    for clause in cnf_kb:
        i+=1
        clause_list = clause.split("|")
        standardized_clause = ""
        for predicate in clause_list:
            bracket_list = re.search("\(.*?\)", predicate).group(0)[1:-1]
            bracket_list = bracket_list.split(",")
            # print(predicate, bracket_list)
            predicate_list = ''
            for var in bracket_list:
                if var[0].islower():
                    # print(var+str(i))
                    predicate = replace1(var , predicate, var + str(i))
            standardized_clause += predicate + "|"
            # predicate
        standardized_cnf += [standardized_clause[:-1]]

    return standardized_cnf


cnf_kb = standardize_cnf(cnf_kb)

positive_knowledge_base, negative_knowledge_base = create_kb_dictionaries(cnf_kb)
resolvable_constants = constant_predicates(cnf_kb)
# print(cnf_kb)
print(resolvable_constants)

# print("Resolvable:", resolvable_constants, len(resolvable_constants))


def unify(long_sentence, one_query) :
    pred = one_query.partition("(")[0]
    global replacement
    # print("****************", one_query, long_sentence)
    query_params = re.search("\(.*?\)", one_query).group(0)[1:-1]
    # print(query_params)
    query_params_list = query_params.split(",")
    # print(query_params_list)

    f_bool = False
    inc = 0
    # print(long_sentence )
    composite_sentences = long_sentence.split('|')
    # print("Long Sent",long_sentence, len(long_sentence))
    # composite_sentences = list(set(composite_sentences))
    # print(type(composite_sentences[-1]))

    for com in composite_sentences:
        com = com.replace(' ', '')
        pred_com = com.partition("(")[0].replace(' ','')
        # print(pred_com)
        # print("COMPOSITE",composite_sentences,"==>", com, pred_com)
        # if "(" in com:
        #     pred_com_param_list = re.search("\(.*?\)", com).group(0)[1:-1].split(",")
        #     # print("Pred com param: ", pred_com_param_list)
        # else:
        #     f_bool == False
        #     break
        # print("List", pred_com_param_list)
        if pred == pred_com :
            # replacement = {}
            pred_com_param_list = re.search("\(.*?\)", com).group(0)[1 :-1].split(",")
            for val in pred_com_param_list :
                val = val.replace(' ', '')
                if inc < len(query_params_list) and val[0].islower() and \
                        query_params_list[inc][0].islower():
                    f_bool = True
                    long_sentence = replace(val, long_sentence, query_params_list[inc])
                    one_query = replace(val, one_query, query_params_list[inc])
                    inc += 1
                elif inc < len(query_params_list) and val[0].isupper() and \
                        query_params_list[inc][0].isupper():
                    # print("ttttt", val, query_params_list[inc])
                    if val != query_params_list[inc]:
                        f_bool = False
                        break
                    else:
                        f_bool = True
                    inc += 1
                elif inc < len(query_params_list) and val[0].isupper() and \
                        query_params_list[inc][0].islower():
                    f_bool = True
                    one_query = replace(query_params_list[inc], one_query, val)
                    inc += 1
                elif inc < len(query_params_list) and val[0].islower() and \
                        query_params_list[inc][0].isupper():
                    f_bool = True
                    long_sentence = replace(val, long_sentence, query_params_list[inc])
                    inc += 1
                # else:
                #     f_bool = False
            if f_bool:
                break
    return f_bool, one_query, long_sentence


def cancel_out(str1, str2) :
    resolvable_bool, unified_query, unified_sentence = unify(str1, str2)
    # print("This is unified:", unified_sentence)
    if resolvable_bool :
        if unified_query in unified_sentence :
            unified_sentence_resolved = unified_sentence.replace(unified_query, '')
        else :
            start = unified_sentence.find(str2.partition("(")[0])
            end = unified_sentence.find(")", start)
            # print(unified_sentence)
            unified_sentence_resolved = unified_sentence[0 :start] + unified_sentence[end+1:]
            # print("Yeh hai maha galti")

        unified_sentence_resolved = unified_sentence_resolved.replace(" ", '')
        if '||' in unified_sentence_resolved :
            # print("Galti 1:", unified_sentence_resolved)
            return unified_sentence_resolved.replace('||', '|').replace(' ', ''), True
        elif unified_sentence_resolved[-1 :] == '|':
            # print("Galti2:")
            return unified_sentence_resolved[:-1].replace(' ', ''), True
        elif unified_sentence_resolved[:1] == '|':
            # print("Galti3:")
            return unified_sentence_resolved[1:].replace(' ', ''), True
        else:
            # print("Galti4:", unified_sentence_resolved)
            return unified_sentence_resolved.replace(' ', ''), True
    else:
        return unified_sentence.replace(' ', ''), False

parent_dict = dict()
def resolution(query_to_resolve, new_query, depth) :
    # print(depth)
    if depth > 1000:
        # print(query_to_resolve)
        return False
    global resolvable_constants
    global parent_dict
    global positive_knowledge_base, negative_knowledge_base
    # if query_to_resolve == '' or query_to_resolve == '~':
    #     # print("Le", query_to_resolve, "Sentence: ", query_to_resolve)
    #     return False
    # print(query_to_resolve, len(query_to_resolve))
    if query_to_resolve[0] == "~":

        # if query_to_resolve[1:] in resolvable_constants:
        #     # print("Yeh negative main resolvable main tha", query_to_resolve, resolvable_constants)
        #     return True
        resolve_key = query_to_resolve.partition("(")[0][1:]
        # print("Key: ", resolve_key)
        if resolve_key in positive_knowledge_base:
            resolvable_sentence_list = positive_knowledge_base[resolve_key]
            # print(query_to_resolve, "==>", resolvable_sentence_list)
        else:
            # print("Positive knowledge base main nahin hai", resolve_key)
            return False

        for sentence in resolvable_sentence_list:
            #  If Condition for reaching non recursion depth
            try:
                #  Assign input params to auxiliary variables
                query_to_resolve_aux = query_to_resolve
                new_query_aux = new_query
                # print("QUERY: ", new_query)
                # new_query_list = new_query.split('|')
                # new_query_list = list(set(new_query_list))
                # new_query_aux = '|'.join(new_query_list)
                # print("NEW QUERY: ", new_query_aux)

                if sentence in resolvable_constants:
                    rest_string, resolvable_bool = cancel_out(new_query_aux, "~" + sentence)
                    rest_string2 = ""
                    resolvable_bool2 = True
                else:
                    rest_string, resolvable_bool = cancel_out(new_query_aux, query_to_resolve_aux)
                    rest_string2, resolvable_bool2 = cancel_out(sentence, query_to_resolve_aux[1 :])

                if resolvable_bool == False or resolvable_bool2 == False :
                    continue
                else :
                    # print("Rest String", rest_string, "Rest String2",rest_string2 )
                    if rest_string2 != '' and rest_string != '':
                        new_query_aux = rest_string2 + '|' + rest_string
                        new_query_aux = new_query_aux.replace(' ', '')
                    else:
                        new_query_aux = (rest_string2 + rest_string).replace(" ", '')

                    # print("*******************", rest_string, "00000", rest_string2)
                    new_query_aux = new_query_aux.replace(" ", "")

                    # print("New Query Empty:", new_query_aux)
                    if new_query_aux == '' or new_query_aux == ' ':
                        return True
                    else:
                        if new_query_aux in parent_dict:
                            continue
                        parent_dict[new_query_aux] = True
                        # print(new_query_aux)
                        # new_query_list = new_query_aux.split('|')
                        # new_query_list = list(set(new_query_list))
                        # # print(new_query_list)
                        # new_query_aux = '|'.join(new_query_list)
                        if "|" in new_query_aux:
                            simplify_list = new_query_aux.split('|')
                            # simplify_list = list(set(simplify_list))
                            # print("Yeh simplify hai", simplify_list)
                            for q in simplify_list :
                                if q != ' ' and q != '':
                                    # print("Q:", q)
                                    q = q.replace(' ', '')

                                    if resolution(q, new_query_aux, depth+1):
                                        # print("Query vs Sentence se true aaya -ve",q , new_query_aux)
                                        return True
                                    else:
                                        break
                        else:
                            if resolution(new_query_aux, new_query_aux, depth+1):
                                # print("Sentence vs Sentence se true aaya: -ve")
                                return True
                            else:
                                continue
            except RecursionError as run_error:
                if run_error.args[0] == 'maximum recursion depth exceeded':
                    # print("Recursion depth nikal gayi - Negative query")
                    return False
        # print("Neg query ka pura chala but kuch output nahin aaya", query_to_resolve, new_query)
        return False
    else:
        # positive query
        # if '~'+query_to_resolve in resolvable_constants:
        #     # print(resolvable_constants, '~'+query_to_resolve)
        #     return True
        resolve_key = query_to_resolve.partition("(")[0]
        # print("Key: ", resolve_key)
        if resolve_key in negative_knowledge_base:
            resolvable_sentence_list = negative_knowledge_base[resolve_key]
            # print(query_to_resolve, "==>", resolvable_sentence_list)
        else:
            # print(query_to_resolve, "::::::::Negative KB main nahin tha::::::", resolve_key)
            return False

        for sentence in resolvable_sentence_list:
            #  If Condition for reaching non recursion depth
            try:
                #  Assign input params to auxiliary variables
                query_to_resolve_aux = query_to_resolve
                new_query_aux = new_query
                # print("QUERY: ", new_query)
                # new_query_list = new_query.split('|')
                # new_query_list = list(set(new_query_list))
                # new_query_aux = '|'.join(new_query_list)
                # print("NEW QUERY: ", new_query_aux)

                if sentence in resolvable_constants:
                    rest_string, resolvable_bool = cancel_out(new_query_aux, sentence[1:])
                    rest_string2 = ""
                    resolvable_bool2 = True
                else:
                    rest_string, resolvable_bool = cancel_out(new_query_aux, query_to_resolve_aux)
                    rest_string2, resolvable_bool2 = cancel_out(sentence, '~' + query_to_resolve_aux)
                    # print("Yahaan negative kiya:", '~' + query_to_resolve)
                if resolvable_bool == False or resolvable_bool2 == False:
                    continue
                else:
                    if rest_string2 != '' and rest_string != '':
                        new_query_aux = rest_string2 + '|' + rest_string
                        new_query_aux = new_query_aux.replace(' ', '')
                    # elif rest_string == '' and rest_string2 != '':
                    #     new_query_aux = rest_string2
                    # elif rest_string2 == '' and rest_string != '':
                    #     new_query_aux = rest_string
                    # else:
                    #     new_query_aux = ''
                    else :
                        new_query_aux = (rest_string2 + rest_string).replace(" ", '')

                    new_query_aux = new_query_aux.replace(" ", "")
                    # if "||" in new_query_aux:
                    #     new_query_aux = new_query_aux.replace("||", "|")
                    # if new_query_aux[0] == "|":
                    #     new_query_aux = new_query_aux[1:]
                    # if new_query_aux[-1] == "|":
                    #     new_query_aux = new_query_aux[:-1]

                    # print("New Query Empty:", new_query_aux)
                    if new_query_aux == '' or new_query_aux == ' ':
                        return True
                    else:
                        if new_query_aux in parent_dict:
                            continue
                        parent_dict[new_query_aux] = True
                        # print(new_query_aux)
                        # new_query_list = new_query_aux.split('|')
                        # new_query_list = list(set(new_query_list))
                        # # print(new_query_list)
                        # new_query_aux = '|'.join(new_query_list)
                        if "|" in new_query_aux:
                            simplify_list = new_query_aux.split('|')
                            # print(simplify_list)
                            # simplify_list = list(set(simplify_list))
                            for q in simplify_list :
                                if q != ' ' and q != '':
                                    q = q.replace(' ', '')
                                    if resolution(q, new_query_aux, depth+1) :
                                        # print("Query vs Sentence se true aaya")
                                        return True
                                    else:
                                        break
                        else:
                            if resolution(new_query_aux, new_query_aux, depth+1):
                                # print("SENTENCE vs Sentence se true aaya")
                                return True
                            else:
                                continue

            except RecursionError as run_error:
                if run_error.args[0] == 'maximum recursion depth exceeded':
                    # print("Recursion end hui - Positive Query")
                    return False
        # print("Pos query ka pura chala but kuch output nahin aaya")
        return False


final_result = ''
# print(query)
for q in query :
    # print(q)
    parent_dict = {}
    replacement = {}
    if q[0] == "~":

        use_query = q[1:]
        resolvable_constants += [use_query]
        # print(resolvable_constants)
        final_result += str(resolution(use_query, use_query, 1)) + "\n"
        resolvable_constants.remove(use_query)
        # print(resolvable_constants)
    else:
        use_query = "~" + q
        resolvable_constants += [use_query]
        # print(resolvable_constants)
        final_result += str(resolution(use_query, use_query, 1)) + "\n"
        resolvable_constants.remove(use_query)
        # print(resolvable_constants)
    # print("Result:" , final_result)
final_result = final_result.upper()
write_stream = open("output.txt", 'w')
write_stream.write(final_result.rstrip())
write_stream.close()

