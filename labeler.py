import xnat
import interface
import sys
import utils
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'
# going to need: /Applications/ITK-SNAP.app/Contents/bin/install_cmdl.sh my_directory - to be ran on bash to allow

DOWNLOAD_IMAGES = True
SOURCE = 'RMH'

with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to: ', connection._original_uri, ' as user: ', user)

    phase = utils.query_phase()
    project = connection.projects['MALIMAR_PHASE{}'.format(phase)]
    print('Project: ', project.name)

    disease_category = utils.query_disease()

    while True:
        mr_session = utils.find_session_to_label(project, disease_category, SOURCE)
        if mr_session:
            utils.print_session_vars(mr_session)

            if DOWNLOAD_IMAGES:
                print('---Downloading Images and Opening in ITK-SNAP---')
                status = 'verified' if mr_session.fields['roi_signed_off_andrea'] == 'Yes' else False
                Images = interface.Segmenter(mr_session, status=status)

            Labels = interface.Labeler(mr_session)
            Labels.open_crf_template()

            if utils.query_yes_no('Disease Labelling Completed?'):
                Labels.upload_crf(name=user)
                mr_session.fields['disease_labelled_andrea'] = 'Yes'

            mr_session.clearcache()
            print('\n\n')

        else:
            break
