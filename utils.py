import sys


def select_mode(project):
    print('Select Mode:')
    print('1. Continue in-progress segmentation')
    print('2. Manually enter session ID')
    print('3. Count completed segmentations')

    choice = input()

    if choice == '1':
        status = 'in_progress'
        return find_in_progress_segmenation(project), status

    elif choice == '2':
        print('Select Segmentation Status:')
        print('1. Unsegmented')
        print('2. In Progress')
        print('3. Complete')
        print('4. Verified')
        print('5. DeepMedic')
        choice = input()
        status = [False, 'in_progress', 'complete', 'verified', 'deep_medic']
        return manually_select_session(project), status[int(choice)-1]
    elif choice == '3':
        count_completed_segs(project)


def count_completed_crfs(project):
    crfs = {'F': {'complete': 0, 'total': 0}, 'D': {'complete': 0, 'total': 0},
            'I': {'complete': 0, 'total': 0}, 'H': {'complete': 0, 'total': 0}}
    for mr_session in project.experiments.values():
        crfs[mr_session.fields['disease_category']]['total'] += 1
        if mr_session.fields['disease_labelled'] == 'Yes':
            crfs[mr_session.fields['disease_category']]['complete'] += 1

    return crfs


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
            if mr_session.fields['roi_done'] == 'Yes':
                num_avanto_cor += 1
        elif mr_session.label.split('_')[-1] == "Avanto" and mr_session.fields['dixon_orientation'] == 'tra':
            total_avanto_tra += 1
            if mr_session.fields['roi_done'] == 'Yes':
                num_avanto_tra += 1
        elif mr_session.label.split('_')[-1] == "Aera" and mr_session.fields['dixon_orientation'] == 'tra':
            total_aera += 1
            if mr_session.fields['roi_done'] == 'Yes':
                num_aera += 1
        else:
            print('Unknown scan type found...')

    total = num_avanto_cor + num_avanto_tra + num_aera
    print('{}/{} scans segmented'.format(total, len(project.experiments)))
    print('{}/{} Avanto Cor'.format(num_avanto_cor, total_avanto_cor))
    print('{}/{} Avanto Tra'.format(num_avanto_tra, total_avanto_tra))
    print('{}/{} Aera'.format(num_aera, total_aera))


def query_yes_no(question):
    options = {'y': True, 'n': False}
    return query(question, options)


def query_phase():
    options = {'1': 1, '2': 2, '3': 3}
    return query('Enter Phase', options)


def query_disease():
    options = {'h': 'H', 'f': 'F', 'd': 'D', 'i': 'I'}
    return query('Enter Disease Category', options)


def query(question, options):
    while True:
        sys.stdout.write(question + ' [' + '/'.join(options) + ']:  ')
        choice = input().lower()
        if choice in options:
            return options[choice]
        else:
            sys.stdout.write('Please respond with: ' + ' or '.join(options) + '\n')


def find_session_to_check(project):
    print('Finding completed segmentations to check:')
    for mr_session in project.experiments.values():
        if mr_session.fields['roi_done'] == 'Yes' and mr_session.fields['roi_signed_off'] == 'No':
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No Segmentations to Check!')
    return False


def find_session_to_label(project, disease_category, source):
    print('Finding case to label with disease category {}'.format(disease_category))
    for mr_session in project.experiments.values():
        if (mr_session.fields['disease_labelled'] == 'No' and
                mr_session.fields['disease_category'] == disease_category):
            if mr_session.subject.label[:3] == source:
                print('---------------------{}-----------------------'.format(mr_session.label))
                return mr_session

    print('All CRFs complete for {}, with disease category {} from {}'.format(project.name, disease_category, source))


def print_session_vars(mr_session):
    print('--- Printing Session Variables ---')
    session_vars = ['disease_pattern', 'disease_category', 'dixon_orientation', 'cm_comments',
                    'mk_comments', 'tb_comments', 'response_mk_imwg']

    print('Age =', mr_session.age)
    print('Gender =', mr_session.subject.demographics.gender)
    print('Subject ID =', mr_session.subject.label)

    for var in session_vars:
        try:
            print(var, '=', mr_session.fields[var])
        except KeyError:
            continue


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


def find_in_progress_segmenation(project):
    print('Checking for segmentations currently in progress')
    for mr_session in project.experiments.values():
        if mr_session.fields['roi_done'] == 'In Progress':
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No Segmentations in progress by')
    return False


def find_unsegmented_session(project, scanner, dx_dir):
    print('Finding MR Session from', scanner, 'with', dx_dir, 'DIXON Orientation')
    for mr_session in project.experiments.values():
        # can also use mr_session.scanner.data['model'] to get scanner name rather than relying on session ID
        if (mr_session.fields['roi_done'] == 'No' and
           mr_session.label.split('_')[-1] == scanner and mr_session.fields['dixon_orientation'] == dx_dir):
            print('---------------------{}-----------------------'.format(mr_session.label))
            return mr_session

    print('No MR Session of this type left to segment')
    return False
