import xnat
import interface
import sys
import utils
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'
# going to need: /Applications/ITK-SNAP.app/Contents/bin/install_cmdl.sh my_directory - to be ran on bash to allow


with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to: ', connection._original_uri, ' as user: ', user)

    project = connection.projects['MALIMAR_PHASE1']
    print('Project: ', project.name)

    while True:
        mr_session = utils.find_session_to_check(project)
        if mr_session:
            utils.print_session_vars(mr_session)
            print('Downloading images and segmentations')
            Segmentations = interface.Segmenter(mr_session, verify=True)
            Labels = interface.Labeler(mr_session)

            if utils.query_yes_no('Segmentation Checked?'):
                Segmentations.status = 'verified'
                Segmentations.upload_segmentations()
                mr_session.fields['roi_signed_off_andrea'] = 'Yes'

            if utils.query_yes_no('Disease Labelling Completed?'):
                Labels.upload_crf()
                mr_session.fields['disease_labelled_andrea'] = 'Yes'

            sys.stdout.write('AR Comment: ')
            comment = input()
            mr_session.fields['ar_comments'] = comment
            mr_session.clearcache()
        else:
            break
