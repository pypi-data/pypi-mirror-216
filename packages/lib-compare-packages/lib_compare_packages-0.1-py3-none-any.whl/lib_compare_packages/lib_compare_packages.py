import requests
import json
from requests import exceptions
from packaging.version import parse
import packaging.version
import re


def v_r(s):
    s = re.sub(r'(\.0*)*$', '', s)  
    a = re.split(r'(\d+)', s)
    a[1::2] = map(int, a[1::2])
    return a

def mycmp(a, b):
    a, b = v_r(a), v_r(b)
    return (a > b) - (a < b)  
    
def get_package_list(branch):
    
    try:
        url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"    

        response = requests.get(url)
        response.raise_for_status()
        package_list = response.json()["packages"]
        return package_list
 
    except KeyError:
        raise SystemExit(exceptions.RequestException)
    except Exception as e:
        print(f"An error occurred: {e}")


def compare_packages(package_list_1, package_list_2):    

    package_dict_1 = {}
    package_dict_2 = {}

    for package in package_list_1:
        package_dict_1.setdefault(package['arch'], {})[package['name']] = package
    for package in package_list_2:
        package_dict_2.setdefault(package['arch'], {})[package['name']] = package
        
    return package_dict_1, package_dict_2
        
        
def package_dict(package_dict_1,package_dict_2):
    
    # Находим все пакеты, которые есть только в первой ветке
    only_in_1 = {}
    for arch in package_dict_1:
        only_in_1[arch] = []
        for package_name in package_dict_1[arch]:
            if package_dict_2.get(arch, []).get(package_name) is None:
                only_in_1[arch].append(package_dict_1[arch][package_name])

    # Находим все пакеты, которые есть только во второй ветке
    only_in_2 = {}
    for arch in package_dict_2:
        only_in_2[arch] = []
        for package_name in package_dict_2[arch]:
            if package_dict_1.get(arch, []).get(package_name) is None:
                only_in_2[arch].append(package_dict_2[arch][package_name])


    # Находим все пакеты, version-release которых больше в первой ветке, чем во второй
    greater_in_1 = {}
    for arch in package_dict_1:
        greater_in_1[arch] = []
        for package_name in package_dict_1[arch]:
            if package_name in package_dict_2.get(arch, {}):
                version1 = package_dict_1[arch][package_name]['version']
                version2 = package_dict_2[arch][package_name]['version']
                release1 = package_dict_1[arch][package_name]['release']
                release2 = package_dict_2[arch][package_name]['release']
                
                try:
                    if parse(version1) > parse(version2) or (parse(version1) == parse(version2) and parse(release1) > parse(release2)):
                        greater_in_1[arch].append(package_dict_1[arch][package_name])
                except packaging.version.InvalidVersion:
                    if mycmp(version1, version2) == 1 or (mycmp(version1, version2)==0 and mycmp(release1, release2)==1):
                        greater_in_1[arch].append(package_dict_1[arch][package_name])
            else:
                continue


# Создаем словарь с результатами сравнения
    result = {
        "only_in_1": only_in_1,
        "only_in_2": only_in_2,
        "greater_in_1": greater_in_1
    }

    # Возвращаем результат
    
    return (json.dumps(result, indent=4))