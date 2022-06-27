from asyncio.windows_events import NULL
import pprint
from bide_alg import bide_alg
import pprint
CONTENT = ['css', 'js', 'jpg', 'jpeg', 'png', 'bmp', 'txt', 'ico', 'rss', "JPG", "gif"]

def pasre_string(s):
    try:
        ip = s[:s.find(' ')]
        s = s[s.find(' ')+5:]

        date_time = s[:28]
        s = s[29:]

        method = s[1:4]
        s = s[5:]

        url = s[:s.find(' ')]
        s = s[s.find(' ')+1:]
        s = s[s.find(' ')+1:]

        status = s[:s.find(' ')]
        s = s[s.find(' ')+1:]

        s = s[s.find(' ')+1:]
        reference_url = s[:s.find(' ')].replace('"', '')

        return ip, date_time, method, url, status, reference_url

    except Exception as e:
        print(e)
        return None

content = 0
get = 0
method200 = 0
reference = 0


def filter(ip, date_time, method, url, status, reference_url):
    global content, get, method200, reference
    if any(c in url for c in CONTENT):
        content += 1
        return False
    if not method == "GET":
        get += 1
        return False
    if not status == '200':
        method200 += 1
        return False
    if reference_url == '-':
        reference += 1
        return False
    return True


def load_data(path='bongbongtrangtri.log'):
    items = {}
    with open(path, 'r') as f:
        for line in f:
            ip, date_time, method, url, status, reference_url = pasre_string(line)
            if filter(ip, date_time, method, url, status, reference_url):
                if ip not in items:
                    items[ip] = [url]
                else:
                    items[ip].append(url)
    return [v for k,v in items.items()]

# Load items from file after filtered 
items = load_data()

# Get longest transaction
max = max([len(row) for row in items])

bide_obj = bide_alg(items, 2 , max)
bide_obj._mine()

# Store result
sorted_result = [[], [], [], [], []]
# Store minsup
rule_dic = {}

for rule in bide_obj._results:
    sorted_result[len(rule[0])].append(rule)
    rule_dic['#'.join(rule[0])] = rule[1]

def get_sup(items):
    global rule_dic
    
    if isinstance(items, list):
        key = '#'.join(items)
        return rule_dic[key]

    if isinstance(items, str):
        return rule_dic[items]

    print(f'can not find sup of {items}')

for i, itemset in enumerate(sorted_result[2:]):
    print(f"{i+2} item in sequence")
    for item in itemset:
        print('\n -------------------------- \n')
        if i == 0:
            try:
                conf = get_sup(item[0]) / get_sup(item[0][0]) * 100
                print(f"{item[0][0]} -> {item[0][1]}, conf = {conf}")
            except Exception as e: 
                pass

        elif i == 1: # 3 item in itemset : <A, B , C>
            try:
                # <A> -> <B, C>
                conf = get_sup(item[0]) / get_sup(item[0][0])  * 100
                print(f"{item[0][0]} -> {'#'.join(item[0][1:])}, conf = {conf}")

                # <A, B> -> <C>
                conf = get_sup(item[0]) / get_sup(item[0][:2])  * 100
                print(f"{'#'.join(item[0][:2])} -> {item[0][2]}, conf = {conf}")

            except Exception as e: 
                 pass

        elif i == 2:# 4 item in itemset : <A, B , C, D>
            try:
                # <A> -> <B, C, D>
                conf = get_sup(item[0]) / get_sup(item[0][0])  * 100
                print(f"{item[0][0]} -> {'#'.join(item[0][1:])}, conf = {conf}")
                # <A, B> -> <C, D>
                conf = get_sup(item[0]) / get_sup(item[0][:2])  * 100
                print(f"{item[0][:2]} -> {'#'.join(item[0][2:])}, conf = {conf}")
                # <A, B, C> -> <D>
                conf = get_sup(item[0]) / get_sup(item[0][:3])  * 100
                print(f"{'#'.join(item[0][:3])} -> {item[0][3]}, conf = {conf}")

            except Exception as e: 
                 pass
        else:
            pass 


# print(4961 - content - get - method200 - reference)