import subprocess
import os
import shutil
import datetime


class Segmenter:
    def __init__(self, mr_session, status=False, verify=False):

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        self.mr_session = mr_session
        self.status = status
        self.verify = verify
        self.seg = False
        self.image_paths = {'dixon': {}, 'diffusion': {}}
        self.seg_paths = {'dixon': None, 'diffusion': None}

        shutil.rmtree('temp', ignore_errors=True)
        os.mkdir('temp')
        os.mkdir('temp/imgs')
        os.mkdir('temp/segs')

        self.download_images()

        if self.verify:
            self.status = 'complete'

        if self.status:
            self.seg = True
            self.download_segmentations()

        self.launch_itk_snap(self.seg)

    def download_images(self):
        scans = self.mr_session.scans
        for i, scan in scans.items():
            nifti_volume = scan.resources['NIFTI'].files[scan.series_description + '.nii.gz']
            filepath = 'temp/imgs/' + scan.series_description + '_' + self.mr_session.label + '.nii.gz'
            print('Downloading', scan.series_description, 'volume')
            nifti_volume.download(filepath, verbose=False)
            # print(scan.series_description + '.nii.gz', 'downloaded')
            if int(i) < 5:
                self.image_paths['dixon'][scan.series_description] = filepath
            else:
                self.image_paths['diffusion'][scan.series_description] = filepath

    def download_segmentations(self):
        res = self.mr_session.resources['segmentations_' + self.status]
        for name, seg in res.files.items():
            print('Downloading', name, 'segmentation')
            sequence = name.split('_')[0]
            extension = '.' + '.'.join(name.split('.')[-2:])
            filename = sequence + '_seg_' + extension
            filepath = 'temp/segs/' + filename
            seg.download(filepath, verbose=False)
            self.seg_paths[sequence] = filepath

    def launch_itk_snap(self, seg=False):
        FNULL = open(os.devnull, 'w')
        if seg:
            for sequence in self.image_paths:
                main_image = list(self.image_paths[sequence].values())[0]
                additional_images = list(self.image_paths[sequence].values())[1:]
                retcode = subprocess.run(["itksnap", "-g", main_image,
                                  "-o", *additional_images,
                                  "-s", self.seg_paths[sequence],
                                  "-l",  "segs.label"], stdout=FNULL, stderr=subprocess.STDOUT)

        else:
            for sequence in self.image_paths:
                main_image = list(self.image_paths[sequence].values())[0]
                additional_images = list(self.image_paths[sequence].values())[1:]
                retcode = subprocess.run(["itksnap", "-g", main_image,
                                  "-o", *additional_images,
                                  "-l",  "segs.label"], stdout=FNULL, stderr=subprocess.STDOUT)

    def upload_segmentations(self):
        print('Uploading Segmentations')
        for sequence in self.seg_paths:
            name = sequence + '_seg'
            dt = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')
            remotepath = name + dt + '.nii.gz'
            localpath = self.seg_paths[sequence]
            label = 'segmentations_' + self.status  # folder name
            mr_session = self.mr_session.xnat_session.experiments[self.mr_session.label]  # this shouldn't be necessary
            uri = '{}/resources/{}'.format(mr_session.uri, label)
            if label not in self.mr_session.resources:
                self.mr_session.xnat_session.put(uri, format='NIFTI')
                self.mr_session.clearcache()

            if sequence in [key.split('_')[0] for key in self.mr_session.resources[label].files]:
                print('Archiving old segmentation', name)
                self.archive_segmentation(sequence)  # todo: little confusing having both name and sequence defined

            self.mr_session.resources[label].upload(data=localpath, remotepath=remotepath)
            self.mr_session.clearcache()
            print(self.status, name, 'uploaded to:', self.mr_session.label)

    def archive_segmentation(self, sequence):
        format = 'NIFTI'
        mr_session = self.mr_session.xnat_session.experiments[self.mr_session.label]  # this shouldn't be necessary
        uri = '{}/resources/{}'.format(mr_session.uri, 'segmentations_old')
        if 'segmentations_old' not in self.mr_session.resources:
            self.mr_session.xnat_session.put(uri, format=format)
            self.mr_session.clearcache()
        label = 'segmentations_' + self.status
        full_name = [key for key in self.mr_session.resources[label].files if key.split('_')[0] == sequence][0]
        path = 'temp/' + full_name
        self.mr_session.resources[label].files[full_name].download(path, verbose=False)
        self.mr_session.resources[label].files[full_name].delete()
        self.mr_session.resources['segmentations_old'].upload(data=path, remotepath=full_name)
        self.mr_session.clearcache()


class Labeler:
    def __init__(self, mr_session):
        self.mr_session = mr_session
        self.open_crf_template()

    def open_crf_template(self):
        filename = 'temp/crf_' + self.mr_session.label + '.xlsx'
        shutil.copyfile('crf_template.xlsx', filename)
        FNULL = open(os.devnull, 'w')
        p = subprocess.run(["open", filename], stdout=FNULL, stderr=subprocess.STDOUT)

    def upload_crf(self):
        dt = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')
        format = 'EXCEL'
        remotepath = 'crf' + '_andrea' + dt + '.xlsx'
        localpath = 'temp/crf_' + self.mr_session.label + '.xlsx'
        label = 'labels'  # folder name
        mr_session = self.mr_session.xnat_session.experiments[self.mr_session.label]
        uri = '{}/resources/{}'.format(mr_session.uri, label)
        self.mr_session.xnat_session.put(uri, format=format)
        self.mr_session.clearcache()
        self.mr_session.resources[label].upload(data=localpath, remotepath=remotepath)
        self.mr_session.clearcache()
        print('CRF uploaded to:', self.mr_session.label)