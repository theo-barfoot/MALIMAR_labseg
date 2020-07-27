import xnat
import interface
import sys
import utils
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'
# going to need: /Applications/ITK-SNAP.app/Contents/bin/install_cmdl.sh my_directory - to be ran on bash to allow

with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to: ', connection._original_uri, ' as user: ', user)

    while True:
        sys.stdout.write('MR Session ID: ')
        mr_id = input()

        mr_session = connection.experiments[mr_id]
        utils.print_session_vars(mr_session)

        Labels = interface.Labeler(mr_session)

        if utils.query_yes_no('Upload edited CRF?'):
            Labels.upload_crf()

            mr_session.clearcache()
            print('\n\n')
        else:
            continue
