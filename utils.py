import sys


def query_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def find_session_to_check(project):
    for mr_session in project.experiments.values():
        if ((mr_session.fields['roi_done_theo'] == 'Yes' and
             mr_session.fields['roi_signed_off_andrea'] == 'No') or
                (mr_session.fields['roi_done_maira'] == 'Yes' and
                 mr_session.fields['roi_signed_off_andrea'] == 'No')):
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session


def print_session_vars(mr_session):
    session_vars = ['disease_pattern', 'disease_category', 'dixon_orientation', 'cm_comments',
                    'mk_comments', 'tb_comments', 'response_mk_imwg']
    for var in session_vars:
        try:
            print(var, '=', mr_session.fields[var])
        except KeyError:
            continue

    print('Age =', mr_session.age)