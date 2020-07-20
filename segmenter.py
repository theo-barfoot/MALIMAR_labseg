import xnat
import utils
import interface
import sys

colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'

with xnat.connect(server=colab) as connection:

    user = connection._logged_in_user
    print('Successfully connected to download server: ', connection._original_uri,
          ' as user: ', user)

    project = connection.projects['MALIMAR_PHASE1']
    print('Project: ', project.name)

    user_name_dict = {'tbarfoot': 'theo', 'mhammeed': 'maira'}
    name = user_name_dict[user]

    mr_session, status = utils.select_mode(project, name)
    print(mr_session.label)
    Segmentations = interface.Segmenter(mr_session, status=status) # status = False

    if utils.query_yes_no('Upload segmentation?'):
        if utils.query_yes_no('Segmentation Complete?'):
            Segmentations.status = 'complete'
            mr_session.fields['roi_done_' + name] = 'Yes'
        else:
            Segmentations.status = 'in_progress'
            mr_session.fields['roi_done_' + name] = 'In Progress'

        Segmentations.upload_segmentations()

    sys.stdout.write('TB Comment: ')
    comment = input()
    mr_session.fields['tb_comments'] = comment

    sys.stdout.write('Artefacts?: ')
    comment = input()
    mr_session.fields['artefact'] = comment

