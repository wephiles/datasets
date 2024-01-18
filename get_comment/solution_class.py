
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
from lxml import etree
from selenium import webdriver
"""
本文件主要进行数据的爬取 
包括评论 课程概述 课程详情 课程评分 课程所属学校 课程名称等
"""

class GetText(object):
    """获取中国大学MOOC操作系统各个课程评论数据。—— 类"""

    def __init__(self, driver=None):
        """__init__()初始化函数

        driver:浏览器对象
        """
        self.driver = driver

    def open_url(self, url: str = None) -> None:
        """打开网页。

        返回： 空
        """

        self.driver.maximize_window()  # 最大化窗口
        time.sleep(1)

        self.driver.get(url=url)  # 打开网址
        return None

    @staticmethod
    def search_key(self, key: str = None) -> None:
        """键入关键词并进行搜索。

        返回： 空
        """
        search_frame = self.driver.find_element(
            By.XPATH, '//div[@class="u-baseinputui"]/input')  # 定位元素
        time.sleep(1)
        search_frame.send_keys(key)  # 发送要搜的关键词
        time.sleep(1)
        search_frame.send_keys(Keys.ENTER)  # 直接模拟手动回车键 不用再定位搜索元素
        return None

    @staticmethod
    def refresh_page(self) -> None:
        """刷新页面。

        返回： 空
        """

        self.driver.refresh()
        return None

    @staticmethod
    def jump_next(self) -> None:
        """点击下一页，进入下一页。

        返回： 空
        """
        next_page = self.driver.find_element(By.CLASS_NAME, 'th-bk-main-gh')
        next_page.click()
        time.sleep(1)
        return None

    @staticmethod
    def all_course(self) -> list[any]:
        """所有课程： 点击每个课程的超链接可进入课程详情页。

        返回： 列表
        """
        click_element = self.driver.find_elements(
            By.CLASS_NAME, 'u-course-name')
        return click_element

    @staticmethod
    def switch_handle(self) -> None:
        """转换窗口句柄。

        并不会在转换句柄之后再关闭窗口。

        返回： 空
        """
        current_handle = self.driver.current_window_handle
        all_handle = self.driver.window_handles
        for handle in all_handle:
            if handle != current_handle:
                self.driver.switch_to.window(handle)
        return None

    @staticmethod
    def close_page(self) -> None:
        """关闭当前页面。

        返回： 空
        """
        self.driver.close()
        return None

    @staticmethod
    def get_school_name(self) -> list[any]:
        """爬取学校名称。

        返回： 列表
        """
        school_name_list = []
        time.sleep(2)
        school_list = self.driver.find_elements(By.CLASS_NAME, 't21.f-fc9')
        school_name = ''
        for school in school_list:
            school_name = school.text
            school_name_list.append(school_name)
        return school_name_list

    @staticmethod
    def get_participate_num(self) -> str:
        """爬取参加人数。

        返回：字符串
        """
        try:
            numbers_people = self.driver.find_element(
                By.CLASS_NAME, 'count')
        except Exception as e:
            print(f'CanNotFindElementError: {e}')
            return 'None'
        num = numbers_people.text
        return num

    @staticmethod
    def if_fine_product(self) -> str:
        """国家精品。

        返回： 字符串
        """
        try:
            self.driver.find_element(By.XPATH, '//*[@id="j-tag"]')
        except Exception as e:
            print(f'Not found the element! {e}')
            return '否'
        return '是'

    @staticmethod
    def get_time(self) -> str:
        """学时安排。

        返回： 字符串
        """
        try:
            time_course = self.driver.find_element(
                By.XPATH, '//*[@class="course-enroll-info_course-info_term-workload"]/span[2]')
        except Exception as e:
            print(f'NetWorkError: {e}')
            return 'None'
        return time_course.text

    @staticmethod
    def get_course_detail(self) -> str:
        """抓取课程详情

        返回： 字符串
        """
        try:
            detail_element = self.driver.find_element(
                By.XPATH, '//*[@id="j-rectxt2"]')
        except Exception as e:
            print(f'CanNotFindElementError: {e}')
            return 'None'
        detail = detail_element.text
        return detail

    @staticmethod
    def get_course_overview(self) -> str:
        """抓取课程概述

        返回： 字符串
        """
        try:
            overview_element = self.driver.find_element(
                By.XPATH, '//div[@class="f-richEditorText"]')
        except Exception as e:
            print(f'CanNotFindElementError: {e}')
            return 'None'
        overview = overview_element.text
        overview.replace('\n', '')
        return overview

    @staticmethod
    def get_course_name(self) -> str:
        """抓取课程名

        返回： 字符串
        """
        time.sleep(2)
        try:
            course_element = self.driver.find_element(
                By.CLASS_NAME, 'course-title.f-ib.f-vam')
        except Exception as e:
            print(f'NetWorkError: {e}')
            return 'None'
        course_name = course_element.text
        return course_name

    @staticmethod
    def get_course_evaluation(self) -> list[any]:
        """抓取一门课程的所有评论

        返回： 列表
        """
        # 定位到评论按钮 点击
        try:
            course_evaluation_button = self.driver.find_element(
                By.ID,
                'review-tag-button')
        except Exception as e:
            print(e)
        else:
            course_evaluation_button.click()

        time.sleep(2)
        comment_list_one_page = []

        while True:
            try:
                one_page_comment_item = self.driver.find_elements(
                    By.CLASS_NAME, 'ux-mooc-comment-course-comment_comment-list_item_body_content')  # 定位到评论元素
            except Exception as e:
                print('CanNotFoundElement!')  # 定位失败
            else:
                time.sleep(1)  # 等待元素加载出来再进行下一步，防止过快导致报错
                for item in one_page_comment_item:
                    comment_text = item.text  # 获取评论信息
                    comment_list_one_page.append(comment_text)  # 把数据添加到列表中
            time.sleep(0.5)
            if GetText.click_evaluation_next(self) == 0:  # 如果还有下一页
                continue
            else:
                return comment_list_one_page  # 函数直接返回存储信息的列表
        return comment_list_one_page  # 函数直接返回存储信息的列表

    @staticmethod
    def get_grade(self) -> str:
        """获取系统所得评分

        返回： 字符串
        """
        time.sleep(1)
        try:
            element_evaluation = self.driver.find_element(
                By.XPATH, '//*[@id="review-tag-button"]')

        except Exception as e:
            print(f'CanNotFindElementError: {e}')
            return 'None'
        element_evaluation.click()

        time.sleep(2)
        number_element = self.driver.find_element(
            By.XPATH, '//*[@id="comment-section"]/div/div[1]/div[1]/span')
        number = number_element.text
        return number

    @staticmethod
    def click_evaluation_next(self) -> int:
        """评论页面，点击下一页

        返回： 空
        """
        time.sleep(1)
        next_button_1 = self.driver.find_elements(
            By.CLASS_NAME, 'th-bk-disable-gh')
        next_button = self.driver.find_elements(
            By.CLASS_NAME, 'th-bk-main-gh')
        if next_button == [] and next_button_1 == []:
            return 1
        for next_ in next_button:
            if next_.text == '下一页':
                next_.click()
                time.sleep(1)
                return 0
            else:
                continue

        for button in next_button_1:
            if button.text == '下一页':
                return 1
        return 0

    @staticmethod
    def first_handle(self) -> None:
        """总是转换到第一个句柄

        返回： 空
        """
        all_handle = self.driver.window_handles
        self.driver.switch_to.window(all_handle[0])
        return None

    @staticmethod
    def second_handle(self) -> None:
        """总是转换到第二个句柄

        返回： 空
        """
        all_handle = self.driver.window_handles
        self.driver.switch_to.window(all_handle[1])
        return None

    @staticmethod
    def browser_quit(self) -> None:
        """退出驱动浏览器

        返回： 空
        """
        self.driver.quit()
        return None

# END
