import xnat
import utils
import interface
import sys

colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'

with xnat.connect(server=colab) as connection:

    user = connection._logged_in_user
    print('Successfully connected to download server: ', connection._original_uri,
          ' as user: ', user)

    phase = utils.query_phase()
    project = connection.projects['MALIMAR_PHASE{}'.format(phase)]

    print('Project: ', project.name)

    mr_session, status = utils.select_mode(project)
    print(mr_session.label)
    Segmentations = interface.Segmenter(mr_session, status=status)  # status = False

    if utils.query_yes_no('Upload segmentation?'):
        if utils.query_yes_no('Segmentation Complete?'):
            Segmentations.status = 'complete'
            mr_session.fields['roi_done'] = 'Yes'
        else:
            Segmentations.status = 'in_progress'
            mr_session.fields['roi_done'] = 'In Progress'

        Segmentations.upload_segmentations()
