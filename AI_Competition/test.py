import unittest
from BeautifulReport import BeautifulReport
import Move

class TestFunction(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("开始测试")

    @classmethod
    def tearDown(self):
        print("测试结束")

    def test_1(self):
        print('初始状态有解，交换步骤在解之后')
        print('初始序列: %s, 空白格: %s, 在第%d步交换, 交换%d, %d' % ('123459786', '9', 20, 1, 2))
        path, Myswap = Move.main('123459786', '9', 20, [1,2])
        print('最优解路径: ', path)
        print('自由交换位置: ',Myswap)
    
    def test_2(self):
        print('初始状态有解，交换步骤在解之前')
        print('初始序列: %s, 空白格: %s, 在第%d步交换, 交换%d, %d' % ('278641539', '9', 5, 5, 9))
        path, Myswap = Move.main('278641539', '9', 5, [5,9])
        print('最优解路径: ', path)
        print('自由交换位置: ',Myswap)

    def test_3(self):
        print('初始状态无解')
        print('初始序列: %s, 空白格: %s, 在第%d步交换, 交换%d, %d' % ('728641539', '9', 5, 3, 7))
        path, Myswap = Move.main('728641539', '9', 5, [3,7])
        print('最优解路径: ', path)
        print('自由交换位置: ',Myswap)

    def test_4(self):
        print('随机')
        print('初始序列: %s, 空白格: %s, 在第%d步交换, 交换%d, %d' % ('123456789', '5', 0, 1, 9))
        path, Myswap = Move.main('123456789', '5', 0, [1,9])
        print('最优解路径: ', path)
        print('自由交换位置: ',Myswap)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    tests = [
        TestFunction('test_1'),
        TestFunction('test_2'),
        TestFunction('test_3'),
        TestFunction('test_4'),
    ]
    suite.addTests(tests)
    BeautifulReport(suite).report(filename='AI_Competition/TestReport.html',
                                  description='测试报告',
                                  log_path='.')