import xnat
import interface
import sys
import utils
colab = 'https://xnatcruk.icr.ac.uk/XNAT_ICR_COLLABORATIONS'
# going to need: /Applications/ITK-SNAP.app/Contents/bin/install_cmdl.sh my_directory - to be ran on bash to allow


session_vars = ['disease_pattern', 'disease_category', 'dixon_orientation', 'cm_comments',
                        'mk_comments', 'tb_comments', 'response_mk_imwg']

with xnat.connect(server=colab) as connection:
    user = connection._logged_in_user
    print('Successfully connected to: ', connection._original_uri, ' as user: ', user)

    project = connection.projects['MALIMAR_PHASE1']
    print('Project: ', project.name)

    print('Checking for completed segmentations:')
    for mr_session in project.experiments.values():
        if ((mr_session.fields['roi_done_theo'] == 'Yes' and
                mr_session.fields['roi_signed_off_andrea'] == 'No') or
            (mr_session.fields['roi_done_maira'] == 'Yes' and
                mr_session.fields['roi_signed_off_andrea'] == 'No')):

            print('---------------------{}-----------------------'.format(mr_session.label))
            for var in session_vars:
                try:
                    print(var, '=', mr_session.fields[var])
                except KeyError:
                    continue

            print('Age =', mr_session.age)
            print('Downloading images and segmentations')
            Segmentations = interface.Segmenter(mr_session, verify=True)
            Labels = interface.Labeler(mr_session)

            checked = utils.query_yes_no('Segmentation Checked?')
            if checked:
                Segmentations.status = 'verified'
                Segmentations.upload_segmentations()
                mr_session.fields['roi_signed_off_andrea'] = 'Yes'

            labelled = utils.query_yes_no('Disease Labelling Completed?')
            if labelled:
                Labels.upload_crf()
                mr_session.fields['disease_labelled_andrea'] = 'Yes'

            sys.stdout.write('AR Comment: ')
            comment = input()
            mr_session.fields['ar_comments'] = comment

        mr_session.clearcache()

    print('No Segmentations to Check!')
