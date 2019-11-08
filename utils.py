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
    print('Finding completed segmentations to check:')
    for mr_session in project.experiments.values():
        if ((mr_session.fields['roi_done_theo'] == 'Yes' and
             mr_session.fields['roi_signed_off_andrea'] == 'No') or
                (mr_session.fields['roi_done_maira'] == 'Yes' and
                 mr_session.fields['roi_signed_off_andrea'] == 'No')):
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No Segmentations to Check!')
    return False


def print_session_vars(mr_session):
    session_vars = ['disease_pattern', 'disease_category', 'dixon_orientation', 'cm_comments',
                    'mk_comments', 'tb_comments', 'response_mk_imwg']
    for var in session_vars:
        try:
            print(var, '=', mr_session.fields[var])
        except KeyError:
            continue

    print('Age =', mr_session.age)


def manually_select_session(project):
    sys.stdout.write('Enter MR Session ID: ')
    label = input()
    if label == '':
        return False
    else:
        try:
            mr_session = project.experiments[label]
            return mr_session
        except KeyError:
            print('uh oh')  # todo: get id reentry, maybe check form of ID eg XXXXXX_XXXXXX_.....


def find_in_progress_segmenation(project, name):
    print('Checking for segmentations currently in progress by', name)
    for mr_session in project.experiments.values():
        if mr_session.fields['roi_done_' + name] == 'In Progress':
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No Segmentations in progress by', name)
    return False


def find_unsegmented_session(project):
    pass
