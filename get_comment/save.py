from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import solution_class
from functools import lru_cache


@lru_cache(maxsize=None)
def main() -> int:
    """主函数

    测试程序的入口

    返回： 整数
    """

    path = Service(
        'xxx')  # 这里放浏览器驱动程序地址
    driver = webdriver.Chrome(service=path)
    driver.maximize_window()  # 最大化窗口
    driver.implicitly_wait(10)  # 等待时间超过10s时，抛出异常

    # 打开页面
    pro = solution_class.GetText(driver=driver)  # 实例化类
    pro.open_url(url='https://www.icourse163.org/')
    pro.search_key(pro, '操作系统')
    time.sleep(1)

    # 抓取学校名称
    school_list = []
    for i in range(0, 2):
        school_name = pro.get_school_name(pro)  # 获取学校名称
        school_list = school_list + school_name  # 存到一个列表里面
        try:
            pro.jump_next(pro)
        except Exception as e:
            print(f'End of the page: {e}')

    # 保存信息
    with open('../copyDirectory/SchoolName.txt', 'w', encoding='utf-8') as fp:
        for item in school_list:
            fp.write(item)
            fp.write('\n')
    print('学校名称下载完成。')

    # 抓取参加人数、学时安排、课程名称、课程详情、课程概述
    pro.first_handle(pro)
    number_dict = {}
    time_dict = {}
    course_dict = {}
    detail_dict = {}
    overview_dict = {}
    fine_dict = {}

    j = 0
    for i in range(0, 2):
        all_item = pro.all_course(pro)

        for item in all_item:
            pro.first_handle(pro)
            time.sleep(1)
            item.click()

            time.sleep(1)
            pro.second_handle(pro)
            time.sleep(2)
            course_name = str(j) + pro.get_course_name(pro)
            j += 1
            if course_name != str(j-1) + 'None':
                participate = pro.get_participate_num(pro)  # 获取参加人数
                number_dict[course_name] = participate

                time_course = pro.get_time(pro)  # 获取课时情况
                time_dict[course_name] = time_course

                course = pro.get_course_name(pro)  # 获取课程名称
                course_dict[course_name] = course

                detail_course = pro.get_course_detail(pro)  # 获取课程详情
                detail_course = detail_course.replace('\n', '')
                detail_dict[course_name] = detail_course

                overview_course = pro.get_course_overview(pro)  # 获取课程概述
                overview_course = overview_course.replace('\n', '')
                overview_dict[course_name] = overview_course

                fine_product = pro.if_fine_product(pro)  # 获取每一门课程是不是国家精品课程
                fine_dict[course_name] = fine_product

            time.sleep(1)
            pro.close_page(pro)
        pro.first_handle(pro)
        pro.jump_next(pro)

    # 保存信息到文件
    with open('../copyDirectory/ParticipateNumber.txt', 'w', encoding='utf-8') as fp:
        for item in number_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(number_dict[item]))
            fp.write('\n')
    print('参加人数下载完成。')

    with open('../copyDirectory/CourseTime.txt', 'w', encoding='utf-8') as fp:
        for item in time_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(time_dict[item]))
            fp.write('\n')
    print('课时信息下载完成。')

    with open('../copyDirectory/CourseName.txt', 'w', encoding='utf-8') as fp:
        for item in course_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(course_dict[item]))
            fp.write('\n')
    print('课程名称下载完成。')

    with open('../copyDirectory/CourseDetail.txt', 'w', encoding='utf-8') as fp:
        for item in detail_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(detail_dict[item]))
            fp.write('\n')
    print('课程详情下载完成。')

    with open('../copyDirectory/CourseOverview.txt', 'w', encoding='utf-8') as fp:
        for item in overview_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(overview_dict[item]))
            fp.write('\n')
    print('课程概述下载完成。')

    with open('../copyDirectory/FineProduct.txt', 'w', encoding='utf-8') as fp:
        for item in fine_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(fine_dict[item]))
            fp.write('\n')
    print('精品课程下载完成。')

    # 抓取评分
    pro.first_handle(pro)

    score_dict = {}
    for i in range(0, 2):
        all_item = pro.all_course(pro)
        j = 0
        for item in all_item:
            pro.first_handle(pro)
            time.sleep(1)
            item.click()

            time.sleep(1)
            pro.second_handle(pro)

            time.sleep(1)
            course_name = str(j) + pro.get_course_name(pro)
            j += 1
            if course_name != str(j-1) + 'None':
                score = pro.get_grade(pro)
                score_dict[course_name] = score
            time.sleep(1)
            pro.close_page(pro)
        pro.first_handle(pro)
        pro.jump_next(pro)

    with open('../copyDirectory/CourseScore.txt', 'w', encoding='utf-8') as fp:
        for item in score_dict:
            fp.write(item)
            fp.write(': ')
            fp.write(str(score_dict[item]))
            fp.write('\n')
    print('课程评分下载完成')

    # 抓取评论
    return 0


if __name__ == '__main__':
    main()

# END
