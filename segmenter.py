import xnat
import utils
import interface
import sys
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'

with xnat.connect(server=colab) as connection:
    # todo: allow manual input of session for checkin
    user = connection._logged_in_user
    print('Successfully connected to download server: ', connection._original_uri,
          ' as user: ', user)

    project = connection.projects['MALIMAR_PHASE1']
    print('Project: ', project.name)

    user_name_dict = {'tbarfoot': 'theo', 'mhammeed': 'maira'}
    name = user_name_dict[user]

    mr_session = utils.manually_select_session(project)
    print(mr_session)
    Segmentations = interface.Segmenter(mr_session) # status = False
    # todo: get it to print what the file name should be.... maybe get it to create a blank file and the overwrite

    if utils.query_yes_no('Upload segmentation?'):
        if utils.query_yes_no('Segmentation Complete?'):
            Segmentations.status = 'complete'
            mr_session.fields['roi_done_' + name] = 'Yes'
        else:
            Segmentations.status = 'in_progress'
            mr_session.fields['roi_done_' + name] = 'In Progress'

        Segmentations.upload_segmentations()



    # todo: finish selection algorithm
    # if not mr_session:
    #     mr_session = utils.find_in_progress_segmenation(project, name)
    #     if not mr_session:




    # print('Starting new segmentation')
    # for e, experiment in enumerate(project.experiments):
    #     mr_session = project.experiments[experiment]
    #     if mr_session.fields['roi_done_theo'] == 'No' and mr_session.fields['roi_done_maira'] == 'No':
    #         pass  # to be continued

