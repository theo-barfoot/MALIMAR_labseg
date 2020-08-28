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

    while True:
        mr_session = utils.find_session_to_check(project)
        if mr_session:
            utils.print_session_vars(mr_session)
            print('Downloading images and segmentations')
            Segmentations = interface.Segmenter(mr_session, verify=True)

            if utils.query_yes_no('Segmentation Checked?'):
                Segmentations.status = 'verified'
                Segmentations.upload_segmentations()
                mr_session.fields['roi_signed_off'] = 'Yes'

            sys.stdout.write('AR Comment: ')
            comment = input()
            mr_session.fields['ar_comments'] = comment
            mr_session.clearcache()
        else:
            break