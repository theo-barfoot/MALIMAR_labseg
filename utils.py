import sys


def select_mode(project, name):
    print('Select Mode:')
    print('1. Continue in-progress segmentation')
    print('2. Start new segmentation (Aera)')
    print('3. Start new segmentation (Avanto cor)')
    print('4. Start new segmentation (Avanto tra)')
    print('5. Manually enter session ID')
    print('6. Count completed segmentations')

    # todo: load completed example option

    choice = input()
    # todo: need to add some checks on the input

    if choice == '1':
        status = 'in_progress'
        return find_in_progress_segmenation(project, name), status
    elif choice == '2':
        status = False
        return find_unsegmented_session(project, scanner='Aera', dx_dir='tra'), status
    elif choice == '3':
        status = False
        return find_unsegmented_session(project, scanner='Avanto', dx_dir='cor'), status
    elif choice == '4':
        status = False
        return find_unsegmented_session(project, scanner='Avanto', dx_dir='tra'), status
    elif choice == '5':
        print('Select Segmentation Status:')
        print('1. Unsegmented')
        print('2. In Progress')
        print('3. Complete')
        print('4. Verified')
        choice = input()
        status = [False, 'in_progress', 'complete', 'verified']
        return manually_select_session(project), status[int(choice)-1]
    elif choice == '6':
        count_completed_segs(project)


def count_completed_segs(project):
    num_avanto_cor = 0
    total_avanto_cor = 0
    num_avanto_tra = 0
    total_avanto_tra = 0
    num_aera = 0
    total_aera = 0
    for mr_session in project.experiments.values():
        if mr_session.label.split('_')[-1] == "Avanto" and mr_session.fields['dixon_orientation'] == 'cor':
            total_avanto_cor += 1
            if (mr_session.fields['roi_done_theo'] == 'Yes') or (mr_session.fields['roi_done_maira'] == 'Yes'):
                num_avanto_cor += 1
        elif mr_session.label.split('_')[-1] == "Avanto" and mr_session.fields['dixon_orientation'] == 'tra':
            total_avanto_tra += 1
            if (mr_session.fields['roi_done_theo'] == 'Yes') or (mr_session.fields['roi_done_maira'] == 'Yes'):
                num_avanto_tra += 1
        elif mr_session.label.split('_')[-1] == "Aera" and mr_session.fields['dixon_orientation'] == 'tra':
            total_aera += 1
            if (mr_session.fields['roi_done_theo'] == 'Yes') or (mr_session.fields['roi_done_maira'] == 'Yes'):
                num_aera += 1
        else:
            print('Unknown scan type found...')

    total = num_avanto_cor + num_avanto_tra + num_aera
    print('{}/{} scans segmented'.format(total, len(project.experiments)))
    print('{}/{} Avanto Cor'.format(num_avanto_cor, total_avanto_cor))
    print('{}/{} Avanto Tra'.format(num_avanto_tra, total_avanto_tra))
    print('{}/{} Aera'.format(num_aera, total_aera))

    return False


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


def find_unsegmented_session(project, scanner, dx_dir):
    print('Finding MR Session from', scanner, 'with', dx_dir, 'DIXON Orientation')
    for mr_session in project.experiments.values():
        # todo: Can definitely improve this huge if statement. Should pass names in as argument
        # can also use mr_session.scanner.data['model'] to get scanner name rather than relying on session ID
        if (mr_session.fields['roi_done_theo'] == 'No' and mr_session.fields['roi_done_maira'] == 'No' and
           mr_session.label.split('_')[-1] == scanner and mr_session.fields['dixon_orientation'] == dx_dir):
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No MR Session of this type left to segment')
    return 0  # todo: need to improve this, more like actually write it properly
