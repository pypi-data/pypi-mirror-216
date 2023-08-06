import argparse
from lib_compare_packages.lib_compare_packages import package_dict, compare_packages, get_package_list


def main():
    parser = argparse.ArgumentParser(description='Compare package lists of two branches.')
    parser.add_argument('branch1', type=str, help='Name of the first branch')
    parser.add_argument('branch2', type=str, help='Name of the second branch')
    args = parser.parse_args()

    package_list_1 = get_package_list(args.branch1)
    package_list_2 = get_package_list(args.branch2)

    package_dict_1, package_dict_2 = compare_packages(package_list_1, package_list_2)

    result = package_dict(package_dict_1, package_dict_2)

    if result:
        print(result)
    else:
        print('Error occurred while getting package lists.')


if __name__ == '__main__':
    main()