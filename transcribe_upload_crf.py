import xnat
import interface
import sys
import utils
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'
# going to need: /Applications/ITK-SNAP.app/Contents/bin/install_cmdl.sh my_directory - to be ran on bash to allow

with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to: ', connection._original_uri, ' as user: ', user)

    phase = utils.query_phase()
    project = connection.projects['MALIMAR_PHASE{}'.format(phase)]
    print('Project: ', project.name)

    sys.stdout.write('CRFs completed by: ')
    name = input()

    sys.stdout.write('Date Time Stamp (YYYYMMDD_hhmmss):')
    dt = input()

    while True:
        sys.stdout.write('MR Session ID: ')
        mr_id = input()

        mr_session = project.experiments[mr_id]
        utils.print_session_vars(mr_session)

        Labels = interface.Labeler(mr_session)
        Labels.open_crf_template()

        if utils.query_yes_no('Disease Labelling Completed?'):
            Labels.upload_crf(name=name, dt=dt)
            mr_session.fields['disease_labelled'] = 'Yes'

            mr_session.clearcache()
            print('\n\n')
        else:
            print('\n\n')
            continue
