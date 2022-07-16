import xmltodict
import time
import datetime
from class_filehelper import FileHelper
from class_dbhelper import DbHeblper
from class_outhelper import OutHelper


class XMLTV():
    def __init__(self, opts:dict):
        self.opts = opts
        self.fh = FileHelper(self.opts['xmltv_link_arch'], self.opts['force_download'])
        self.db = DbHeblper()
        self.out = OutHelper()
        self.time_now = int(time.time())
        self.m3u_only = self.opts['use_m3u']

    def start(self):
        if self.need_new_db():
            self.create_new_db()


    def need_new_db(self):
        '''
        check, need new db or not
        Temp depend only wit force flag

        :return: bool, True - create new. False - ok, no need new db
        '''
        if self.opts['force_download']:
            return True
        else:
            if not self.fh.check_file_exist('xmltv.db'):
                return True
            return False

    def create_new_db(self):
        '''
        create db complex - prepare files, get an pasrse content, create db

        :return:
        '''
        xml_content = self.fh.prepare_files()           # prepare files and get content
        xmltv_dict = xmltodict.parse(xml_content)       # get dict from xml content
        self.fh.remove_file(self.db.filename_db)
        self.db.create_table('channels')
        self.db.create_table('shows')
        self.parse_xmltv_dict(xmltv_dict)               #
        self.save_channels_from_m3u()


    def parse_xmltv_dict(self, xmltv_dict:dict):
        '''
        Parsing dict with xml data and post it to db

        :param xmltv_dict:
        dict via xml

        :return:
        bool, True if success
        '''
        channels = []
        channels_id_name = {}
        for channel in xmltv_dict['tv']['channel']:
            this_channel = {
                'cid': channel['@id'],
                'name': channel['display-name']['#text'],
                'logo': ''
            }
            channels_id_name.update({this_channel['cid']:this_channel['name']})
            channels.append(this_channel)

        shows = []
        for show in xmltv_dict['tv']['programme']:
            this_show = {
                'cid': show['@channel'],
                'chanel_name': channels_id_name[show['@channel']],
                'start': self.xmltvtime_to_timestamp(show['@start']),
                'stop': self.xmltvtime_to_timestamp(show['@stop']),
                'duration': self.xmltvtime_to_timestamp(show['@stop']) - self.xmltvtime_to_timestamp(show['@start']),
                'title': show['title']['#text'] if 'title' in show.keys() else '',
                'category': show['category']['#text'] if 'category' in show.keys() else '',
                'description': show['desc']['#text'] if 'desc' in show.keys() else '',
            }
            shows.append(this_show)
        print(f"Total shows: {len(shows)}")
        print(f"Total channels: {len(channels)}")
        self.db.add_new_data('shows', shows)

        self.db.add_new_data('channels', channels)
        return True

    def xmltvtime_to_timestamp(self, timex: str):
        '''
        Convert string with time in xmltv format to timestamp

        :param timex:
        String with time from xml

        :return:
        Unix timestamp
        '''
        offset_dirt = timex[-5:-2]
        offset = int(offset_dirt)
        year = int(timex[0:4])
        month = int(timex[4:6])
        day = int(timex[6:8])
        hours = int(timex[8:10])
        minutes = int(timex[10:12])
        seconds = int(timex[12:14])
        unix_time = datetime.datetime(year, month, day, hours, minutes, seconds) + datetime.timedelta(hours=offset)
        unix_time = int(time.mktime(unix_time.timetuple()))
        return unix_time

    def get_shows(self):
        '''
        Main function for route other function for get gata and out it

        :return:
        '''
        time_min = self.time_now - (self.opts['target_minutes_ending'] * 60)
        time_max = self.time_now + (self.opts['target_minutes_begining'] * 60)
        dirty_found_data = self.db.read_data_between('shows', (time_min, time_max))
        filtered_dirty_found_data = self.filter_shows(dirty_found_data)

        if self.opts['html_out']:
            found_data_html = self.pretty_filtered_list_for_html(filtered_dirty_found_data)
            self.out.out_html(found_data_html, False)
        else:
            found_data_console = self.pretty_filtered_list_for_console(filtered_dirty_found_data)
            self.out.out_console(found_data_console)

    def pretty_filtered_list_for_console(self, dirty_found_data:list):
        '''
        Get data with format for console out

        :param dirty_found_data:
        Data from database

        :return:
        Clean list to console out
        '''
        pfd = []
        for show in dirty_found_data:
            this_show = [show[1], self.ts_to_time(show[2]),
                         show[4] // 60, show[5]]
            pfd.append(this_show)
        return pfd

    def pretty_filtered_list_for_html(self, dirty_found_data:list):
        '''
        Get data with format for html out

        :param dirty_found_data:
        Data from database

        :return:
        Clean list to html out
        '''
        pfd = []
        for show in dirty_found_data:
            this_show = {
                'channel_logo': str(''),
                'channel_name': str(show[1]),
                'time_show_begin': str(self.ts_to_time(show[2])),
                'time_duration': str(show[4] // 60),
                'title': str(show[5]),
                'category': str(show[6]),
                'desc': str(show[7]),
            }
            pfd.append(this_show)
        return pfd


    def ts_to_time(self, ts:int):
        '''
        Convert timestamp for human-readable format

        :param ts:
        Unix timestamp

        :return:
        Time in %H:%M format
        '''
        return datetime.datetime.fromtimestamp(int(ts)).strftime('%H:%M')

    def get_list_m3u_channels(self):
        '''
        Get channels from m3u file if is exist

        :return:
        False if not exist or list of channels
        '''
        m3u_content = self.fh.search_m3u()
        if m3u_content:
            m3u_channels = []
            for line in m3u_content.split('\n'):
                if line.startswith("#EXTINF"):
                    m3u_channels.append(line.split(',')[-1])
            return m3u_channels
        else:
            print('m3u files was not found')
            return False

    def save_channels_from_m3u(self):
        '''
        Saves chanels list if it exist to file

        :return:

        '''
        channels = self.get_list_m3u_channels()
        if channels:
            self.fh.wrire_to_list('tv_ch', '\n'.join(channels))
            print('Channels was write')

    def filter_shows(self, shows:list):
        '''
        Filtering dirty data from database with blacklists and channels in m3u

        :param shows:
        Dirty data

        :return:
        Filtered data
        '''
        bl_channels = self.fh.read_list('bl_ch')
        bl_categories = self.fh.read_list('bl_cat')
        bl_names = self.fh.read_list('bl_names')
        tv_channels = self.fh.read_list('tv_ch')
        # fields: ['cid', 'chanel_name', 'start', 'stop', 'duration', 'title', 'category', 'description']
        remove_counts = {
            'bl_channels': 0,
            'bl_categories': 0,
            'bl_names': 0,
            'tv_channels': 0,
        }
        filtered_shows = []
        for show in shows:
            if (self.m3u_only and self.check_in_list(show[1], tv_channels)) or not self.m3u_only:
                this_show = []
                this_show.append(show[0])
                if not self.check_in_list(show[1], bl_channels):
                    this_show.append(show[1])
                else:
                    remove_counts['bl_channels'] += 1
                    continue
                this_show.append(show[2])
                this_show.append(show[3])
                this_show.append(show[4])
                if not self.check_in_list(show[5], bl_names):
                    this_show.append(show[5])
                else:
                    remove_counts['bl_names'] += 1
                    continue
                if not self.check_in_list(show[6], bl_categories):
                    this_show.append(show[6])
                else:
                    remove_counts['bl_categories'] += 1
                    continue
                this_show.append(show[7])
                filtered_shows.append(this_show)
            else:
                remove_counts['tv_channels'] += 1
        print('Filtered by:')
        print(f"TV channels: {remove_counts['tv_channels']}")
        print(f"BL channels: {remove_counts['bl_channels']}")
        print(f"BL categories: {remove_counts['bl_categories']}")
        print(f"BL names: {remove_counts['bl_names']}")
        print(f"Shows filtered: {len(filtered_shows)}/{len(shows)}")
        return filtered_shows

    def check_in_list(self, name:str, lst:list):
        '''
        Check for part of element exist list

        :param name:
        Element

        :param lst:
        List to search

        :return:
        Bool, True if found, False if not
        '''
        if name == '':
            return False
        for line in lst:
            if len(line) > 0:
                if name.lower() in line.lower():
                    return True
        return False

