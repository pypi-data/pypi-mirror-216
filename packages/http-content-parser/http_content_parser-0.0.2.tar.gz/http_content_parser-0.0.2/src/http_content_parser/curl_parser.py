# -*- coding: UTF-8 -*-
class CurlParser(object):
    def split_url(self, url: str, split_char: str):
        # TODO 考虑url中没有http字符的情况(只出现在Postman导出的curl)
        url_params = {}
        if '?' in url:
            ss = url.split('?')
            url = ss[0]
            url_params = ss[1]
            url_params = self.form_str_to_dict(url_params)
        urls = url.split('/')
        url_path = ''
        for i in range(3, len(urls)):
            url_path += urls[i] + split_char
        return {'url_path': url_path, 'url_params': url_params}

    def form_str_to_dict(self, form_data):
        """将form表单参数转成dict类型"""
        item_dict = {}
        if '&' in form_data:
            for item in form_data.split('&'):
                line = item.split('=')
                if len(line) == 2:
                    item_dict[line[0]] = line[1]
                if len(line) == 1:
                    item_dict[line[0]] = ''
        else:
            if '=' in form_data:
                line = form_data.split('=')
                item_dict[line[0]] = line[1]
        return item_dict

    # 处理curl中data部分的数据,把多行转换成一行数据
    def reduce_curl_data_part(self, lines, s, e):
        new_lines = []
        for i in range(s, e):
            new_line = lines[i]
            if '--data ' in lines[i]:
                # 判断请求的body是否完整,根据''单引号是否是两个
                char_count = lines[i].count('\'')
                if char_count == 1:
                    i += 1
                    while i < e:
                        new_line += lines[i]
                        if lines[i].count('\'') == 1:
                            break
                        i += 1
            new_lines.append(new_line)
        return new_lines

    def get_curl_line_num_scope(self, lines):
        start_num = 0
        num = 0
        curl_num = 0
        line_num_array = []
        for line in lines:
            # 拆分多个curl
            if 'curl' in line:
                curl_num += 1
                if curl_num >= 2:
                    line_num_array.append([start_num, num-1])
                    curl_num = 1
                start_num = num
            num += 1
            if num == len(lines):
                line_num_array.append([start_num, num])
        return line_num_array

    def split_curl_to_struct(self, lines, s, e, curl_filter=None) -> dict:
        req_data = {}
        header = {}
        reduced_lines = self.reduce_curl_data_part(lines=lines, s=s, e=e)
        for i in range(0, len(reduced_lines)):
            lines_i_str = str(reduced_lines[i])
            line_i_list = lines_i_str.split(' ')
            if 'curl' in lines_i_str:
                if curl_filter:
                    if curl_filter not in lines_i_str:
                        # 如果curl_filter 不存在于当前Url中,则跳过本次循环
                        continue
                for line_sub in line_i_list:
                    if line_sub.lower() in ['get', 'put', 'post', 'delete']:
                        req_data['method'] = line_sub.lower().replace('\'', '')
                    elif 'http' in line_sub:
                        req_data['original_url'] = line_sub.replace('\'', '')
                    # 兼容Postman中url没有http开头的情况
                    elif '/' in line_sub:
                        req_data['original_url'] = line_sub.replace('\'', '')
            elif '-X ' in lines_i_str:
                line_i_list = lines_i_str.split(' \'')
                req_data['method'] = line_i_list[1].lower().replace(
                    '\'', '').replace(' ', '').replace('\\\n', '')
            elif '-H \'' in lines_i_str or '--header' in lines_i_str:
                line_i_list = lines_i_str.split(' \'')
                subs = str(line_i_list[1]).split(':')
                if len(subs) > 1:
                    # TODO 空格区分有用和无用，目前cookie的value中会有包含空格的情况, 不删除
                    header[subs[0]] = subs[1].replace(
                        '\'', '').replace('\\\n', '').replace(' ', '')
                else:
                    header[subs[0]] = ''
            elif '--data-raw' in lines_i_str or '--data' in lines_i_str:
                line_i_list = lines_i_str.replace(' $',' ').split(' \'') # TODO 有$符号,split会失败,这样解决会出现被错误替换的问题
                if len(line_i_list) > 1:
                    curl_data = line_i_list[1]
                else:
                    curl_data = line_i_list[0]
                req_data['body'] = curl_data.replace(
                    '\'', '').replace(' ', '').replace('\\\n', '').replace('\n', '')

                if not req_data.get('method'):
                    req_data['method'] = 'post'

        req_data['header'] = header
        if not req_data.get('method'):
            req_data['method'] = 'get'
            
        return req_data
