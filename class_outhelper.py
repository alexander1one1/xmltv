import os
import webbrowser
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
init(autoreset=True)

class OutHelper():
    def __init__(self):
        '''
        Some functions for return results

        '''

        self.console_table_max_sym = 70
        self.colors = [
            {'min':0,'max':10, 'color':Fore.LIGHTWHITE_EX},
            {'min':10,'max':30, 'color':Fore.LIGHTRED_EX},
            {'min':30,'max':60, 'color':Fore.YELLOW},
            {'min':60,'max':120, 'color':Fore.LIGHTGREEN_EX},
            {'min':120,'max':9999, 'color':Fore.LIGHTMAGENTA_EX},
        ]
        self.filename_html_template = 'html_template.html'
        self.filename_html_out = 'out.html'

    def out_html(self, data:list, enable_logo:bool):
        '''
        Set data for out via html file and open browser with it

        :param data:
        Shows data (special for html)

        :param enable_logo:
        bool, True: need out logo, False: dont need

        :return:
        Nothing. Just open default browser
        '''
        with open(self.filename_html_template, 'r') as f:
            template_content = f.read()

        out = ''
        for show in data:
            out += '<tr>'
            if enable_logo:
                out += '<td><img src="' + show['channel_logo'] + '" width=100 height=100 /></td>'
            else:
                out += '<td></td>'
            out += '<td>' + show['channel_name'] + '</td>'
            out += '<td>' + show['time_show_begin'] + '</td>'
            out += '<td>' + show['time_duration'] + '</td>'
            out += '<td>' + show['title'] + '</td>'
            out += '<td>' + show['category'] + '</td>'
            out += '<td>' + show['desc'] + '</td>'
            out += '</tr>'

        out_content = template_content.replace('---CONTENT---', out).encode(encoding='UTF-8')
        with open(self.filename_html_out, 'wb') as f:
            f.write(out_content)
        webbrowser.open(self.filename_html_out)

    def out_console(self, data:list):
        '''
        Set data for out via console

        :param data:
        Shows data (special for console)

        :return:
        Nothing, just stdout in console
        '''
        self.console_table = PrettyTable()
        self.console_table.set_style(15)
        self.console_table.align = "l"
        self.console_table.field_names = ['Channel', 'Start', 'Duration', 'Name']
        sorted_data = sorted(data, key = lambda x: int(x[1].split(':')[0]*60) + int(x[1].split(':')[1]))
        for count, show in enumerate(sorted_data):
            color = Fore.LIGHTWHITE_EX if count % 2 == 0 else Fore.LIGHTYELLOW_EX
            this_show = []
            this_show.append(color + show[0][:self.console_table_max_sym] + Fore.RESET)
            this_show.append(color + show[1] + Fore.RESET)
            this_show.append(self.get_colorama_color(int(show[2])) + str(show[2]) + Fore.RESET)
            this_show.append(color + show[3][:self.console_table_max_sym] + Fore.RESET)
            self.console_table.add_row(this_show)
        print(self.console_table)

    def get_colorama_color(self, duration:int):
        this_color = Fore.LIGHTWHITE_EX
        for color in self.colors:
            if color['min'] <= duration <= color['max']:
                this_color = color['color']
                break
        return str(this_color)
