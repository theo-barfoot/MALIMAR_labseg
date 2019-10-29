import xnat
import sys
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'

# todo: need to think about whether it makes sense for this segmenter to run for multiple sessions....

with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to download server: ', connection._original_uri,
          ' as user: ', user)

    user_name_dict = {'tbarfoot': 'theo', 'mhammeed': 'maira'}

    name = user_name_dict[user]
    print(name)

    project = connection.projects['MALIMAR_PHASE1']
    print('Project: ', project.name)

    print('Checking for segmentations currently in progress by', name)
    for e, experiment in enumerate(project.experiments):
        mr_session = project.experiments[experiment]
        if mr_session.fields['roi_done_' + name] == 'In Progress':
            # mr_session_select = mr_session
            print('Loading', mr_session.label)
            # run download sessions etc....
            break
        else:
            continue

    print('Starting new segmentation')
    for e, experiment in enumerate(project.experiments):
        mr_session = project.experiments[experiment]
        if mr_session.fields['roi_done_theo'] == 'No' and mr_session.fields['roi_done_maira'] == 'No':
            pass  # to be continued

