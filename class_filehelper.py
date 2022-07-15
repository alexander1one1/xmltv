from pathlib import Path
import wget
import os
import glob
import gzip
import settings as st

class FileHelper():
    def __init__(self, dl_link:str, force_clean:bool=False):
        '''
        class with works with files

        :param dl_link:
        link with arch

        :param force_clean:
        clear dir flag
        '''
        self.cur_dir = os.getcwd()
        self.temp_dir = self.cur_dir + os.sep + st.dirname_temp + os.sep
        self.dir_lists = self.cur_dir + os.sep + 'lists' + os.sep
        self.force_clean = force_clean
        self.dl_link = dl_link
        self.path_arch = self.temp_dir + self.dl_link.split('/')[-1]
        self.path_xml = self.temp_dir + st.filename_main_xml
        self.lists_files = {
            'bl_ch': self.dir_lists + 'blacklist_channels.txt',
            'bl_cat': self.dir_lists + 'blacklist_categories.txt',
            'bl_names': self.dir_lists + 'blacklist_names.txt',
            'tv_ch': self.dir_lists + 'tv_channels.txt',
        }

    def create_temp_folder(self):
        '''
        create temp folder if not exist

        :return:
        True if ok
        '''
        if not Path(self.temp_dir).is_dir():
            try:
                os.mkdir(self.temp_dir)
                return True
            except Exception as e:
                print("Temp dir was not create:", e)
                return False
        return True

    def check_arch_exist(self):
        '''
        check for exist file downloaded from link

        :param dl_link:
        download link

        :return:
        True if exist
        '''

        arch_exist = Path(self.path_arch).is_file()
        return arch_exist

    def check_xml_file_exist(self):
        '''
        check for exist file

        :return:
        True if exist
        '''
        file_exist = Path(self.path_xml).is_file()
        return file_exist

    def check_file_exist(self, filename:str):
        '''
        check for exist file

        :return:
        True if exist
        '''
        file_exist = Path(filename).is_file()
        return file_exist

    def download_arch(self):
        '''
        download file in temp dir

        :return:
        bool with status of download
        '''
        print("Downloading...")
        try:
            wget.download(self.dl_link, self.temp_dir)
            return True
        except Exception as e:
            print("Something went wrong with dl:", e)
            return False

    def extract_arch(self):
        '''
        extract archive

        :return:
        content or False
        '''
        with gzip.open(self.path_arch, 'rb') as f:
            file_content = f.read()
        with open(self.path_xml, 'wb') as f:
            try:
                f.write(file_content)
                return file_content
            except Exception as e:
                print("Write to xml file fail:", e)
                return False


    def remove_arch_and_xml(self):
        '''
        remove archive and xml file

        :return:
        True
        '''
        if os.path.exists(self.path_arch):
            os.remove(self.path_arch)
        if os.path.exists(self.path_xml):
            os.remove(self.path_xml)
        return True

    def remove_file(self, filename:str):
        os.remove(filename)


    def prepare_files(self):
        '''
        complex of defs for get files ready for parse

        :return:
        content of extracted xml
        '''
        self.create_temp_folder()
        if self.force_clean:
            self.remove_arch_and_xml()
        if not self.check_arch_exist():
            self.download_arch()
        xml_content = self.extract_arch()
        return xml_content

    def search_m3u(self):
        '''
        Search m3u files in main directory

        :return:
        Filename first m3u
        '''
        m3u_files = glob.glob("*.m3u")
        if len(m3u_files) > 0:
            with open(m3u_files[0]) as f:
                return f.read()
        else:
            return False

    def wrire_to_list(self, listname:str, content:str):
        '''
        Write content to list file

        :param listname:
        id list in FileHelper.lists_files

        :param content:
        Txt content

        :return: True
        '''
        with open(self.lists_files[listname], 'w') as f:
            f.write(content)
            return True

    def read_list(self, listname:str):
        '''
        Read content from list txt file

        :param listname:
        id list in FileHelper.lists_files

        :return:
        list from list txt
        '''
        with open(self.lists_files[listname], 'r') as f:
            return f.read().split('\n')


