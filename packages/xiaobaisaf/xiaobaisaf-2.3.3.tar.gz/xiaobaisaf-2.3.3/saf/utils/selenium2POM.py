#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/12 22:48
@File  : HTML2POM.py
'''
import re
from os import path, mkdir, remove
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException


class PageListener:
    def __init__(self, start_url: str = 'https://www.baidu.com', dirname: str = '.', rewrite: bool = True):
        '''
        基于Selenium基础操作过程中将每页内容转为POM
        :param to_str       : True将结果转为字符串返回 ,False将结果写入到脚本，自动输出到Pages包中
        '''
        if rewrite and path.exists(f'{dirname}/Pages'):
            try:
                remove(f'{dirname}/Pages')
            except PermissionError as e:
                pass
        if not path.exists(f'{dirname}/Pages'):
            mkdir('Pages')
        if not path.exists(f'{dirname}/Pages/__init__.py'):
            with open(f'{dirname}/Pages/__init__.py', 'w', encoding='UTF-8') as f:
                f.write('''#! /usr/bin/env python
                
#********************************#
#    欢迎使用自动生成POM代码工具      #
#      Auther:xiaobaiTser        #
#********************************#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
                ''')
                f.close()

        driver = webdriver.Chrome()
        driver.get(start_url)
        driver.implicitly_wait(30)
        new_title = ''.join(re.findall('\w+', driver.title))
        self.code2file(
            code=self.identify_inputs_and_buttons(driver.current_url, driver.page_source),
            filename=f'{dirname}/Pages/{"_".join(lazy_pinyin(new_title)).title()}.py')
        # 监视浏览器URL变化、标签页变化
        old_url = driver.current_url
        old_handles = driver.window_handles
        while True:
            try:
                new_url = driver.current_url
                new_handles = driver.window_handles
                if len(new_handles) > len(old_handles):
                    driver.switch_to.window(list(set(new_handles)-set(old_handles))[0])
                    new_title = ''.join(re.findall('\w+', driver.title))
                    self.code2file(
                        code=self.identify_inputs_and_buttons(driver.current_url, driver.page_source),
                        filename=f'{dirname}/Pages/{"_".join(lazy_pinyin(new_title)).title()}.py')
                    old_handles = new_handles
                elif new_url != old_url:
                    new_title = ''.join(re.findall('\w+', driver.title))
                    self.code2file(
                        code=self.identify_inputs_and_buttons(driver.current_url, driver.page_source),
                        filename=f'{dirname}/Pages/{"_".join(lazy_pinyin(new_title)).title()}.py')
            except KeyboardInterrupt as e:
                exit(-1)
            except NoSuchWindowException as e:
                exit(-2)

    @classmethod
    def code2file(cls, code: str, filename: str = None):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(code)
            f.close()
            del f

    @classmethod
    def identify_inputs_and_buttons(cls, url, html):
        '''
        1、解析HTML获取输入框与按钮并获取xpath表达式
        2、将输入框与按钮转为POM代码，一个页面单独一个脚本，一个脚本单独一个类
        :param html:
        :return:
        '''
        soup = BeautifulSoup(html, 'html.parser')
        find_all_input = soup.find_all(['input', 'textarea'])
        find_all_button = soup.find_all('button')
        find_all_button.extend(soup.find_all('a'))
        find_all_button.extend(soup.find_all('input', attrs={'type': ['button', 'submit']}))
        input_list = []
        button_list = []
        for input_tag in find_all_input:
            if input_tag not in soup.find_all('input', attrs={'type': ['button', 'submit', 'hidden']}):
                input_name = input_tag.get('name') or input_tag.name
                input_xpath = cls.get_xpath(input_tag)
                if input_name:
                    input_list.append({'tag': input_tag, 'name': input_name, 'xpath': input_xpath})
        for button_tag in find_all_button:
            button_name = button_tag.get('name') or button_tag.text.strip() or button_tag.name
            button_xpath = cls.get_xpath(button_tag)
            button_list.append({'tag': button_tag, 'name': button_name, 'xpath': button_xpath})
        title = '_'.join(lazy_pinyin(soup.select("title")[0].text)).upper()
        title = ''.join(re.findall('[0-9a-zA-Z_]+', title))
        return cls.converter(page_name=title, url=url,
                              input_list=input_list, button_list=button_list)

    @classmethod
    def get_xpath(cls, element):
        components = []
        child = element
        while child is not None:
            siblings = child.find_previous_siblings()
            index = len(siblings) + 1
            if child.name == 'html':
                components.insert(0, '/html')
                break
            if child.name == 'body':
                components.insert(0, '/body')
                break
            components.insert(0, f'/{child.name}[{index}]')
            child = child.parent
        xpath = ''.join(components)
        xpath = xpath if xpath.startswith('/html') else '/' + xpath
        return xpath

    @classmethod
    def converter(cls, page_name: str, url: str, input_list: list, button_list: list):
        function_strings = []
        function_names = []
        function_strings.append('#! /usr/bin/env python')
        function_strings.append(f'')
        function_strings.append('#********************************#')
        function_strings.append('#    欢迎使用自动生成POM代码工具      #')
        function_strings.append('#      Auther:xiaobaiTser        #')
        function_strings.append('#********************************#')
        function_strings.append(f'')
        function_strings.append('from selenium.webdriver.common.by import By')
        function_strings.append(f'')
        function_strings.append(f'class {page_name}:')
        function_strings.append('\tdef __init__(self, driver):')
        function_strings.append(f'\t\t# 当前URL: {url}')
        function_strings.append('\t\tself.driver = driver')
        function_strings.append(f'')
        for input_item in input_list:
            function_name = "_".join(lazy_pinyin(input_item['name']))
            function_name = ''.join(re.findall('[0-9a-zA-Z_]+', function_name))
            function_names.append(function_name)
            if function_names.count(function_name) > 1:
                function_name = f'{function_name}_{function_names.count(function_name)-1}'
            xpath = input_item['xpath']
            function_strings.append(f'\tdef send_{function_name}(self, data):')
            function_strings.append("\t\t'''")
            function_strings.append('\t\t当前元素：')
            input_item['tag'] = str(input_item['tag']).replace('\n', '\n\t\t')
            function_strings.append(f"\t\t{input_item['tag']}")
            function_strings.append("\t\t'''")
            function_strings.append(f'\t\tself.driver.find_element(By.XPATH, "{xpath}").send_keys(data)')
            function_strings.append(f'')
        for button_item in button_list:
            function_name = "_".join(lazy_pinyin(button_item['name']))
            function_name = ''.join(re.findall('[0-9a-zA-Z_]+', function_name))
            function_names.append(function_name)
            if function_names.count(function_name) > 1:
                function_name = f'{function_name}_{function_names.count(function_name)-1}'
            xpath = button_item['xpath']
            function_strings.append(f'\tdef click_{function_name}(self):')
            function_strings.append("\t\t'''")
            function_strings.append('\t\t当前元素：')
            button_item['tag'] = str(button_item['tag']).replace('\n', '\n\t\t')
            function_strings.append(f"\t\t{button_item['tag']}")
            function_strings.append("\t\t'''")
            function_strings.append(f'\t\tself.driver.find_element(By.XPATH, "{xpath}").click()')
            function_strings.append(f'')
        return '\n'.join(function_strings)

# if __name__ == '__main__':
#     PageListener()