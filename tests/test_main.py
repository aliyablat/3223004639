# tests/test_main.py

import unittest
import os
import sys
import tempfile


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from main import (
    read_file,
    write_result,
    calculate_edit_distance_v2,
    plagiarism_check
)


class TestPlagiarismChecker(unittest.TestCase):

    def setUp(self):
        """在每个测试用例运行前设置临时文件和目录"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.orig_file_path = os.path.join(self.temp_dir.name, "orig.txt")
        self.plag_file_path = os.path.join(self.temp_dir.name, "plag.txt")
        self.output_file_path = os.path.join(self.temp_dir.name, "ans.txt")

    def tearDown(self):
        """在每个测试用例运行后清理临时文件和目录"""
        self.temp_dir.cleanup()

    # --- 测试 calculate_edit_distance_v2 ---
    def test_1_identical_strings(self):
        """测试两个完全相同的字符串"""
        s1 = "hello world"
        s2 = "hello world"
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 0)

    def test_2_completely_different_strings(self):
        """测试两个完全不同的字符串"""
        s1 = "abc"
        s2 = "xyz"
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 3)  # 需要3次替换

    def test_3_insertion(self):
        """测试插入操作"""
        s1 = "cat"
        s2 = "cast"
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 1)

    def test_4_deletion(self):
        """测试删除操作"""
        s1 = "apple"
        s2 = "aple"
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 1)

    def test_5_substitution(self):
        """测试替换操作"""
        s1 = "book"
        s2 = "back"
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 2)

    def test_6_empty_strings(self):
        """测试两个空字符串"""
        s1 = ""
        s2 = ""
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 0)

    def test_7_one_empty_string(self):
        """测试其中一个字符串为空"""
        s1 = "test"
        s2 = ""
        self.assertEqual(calculate_edit_distance_v2(s1, s2), 4)

    # --- 测试文件读写 ---
    def test_8_read_and_write_file(self):
        """测试文件的基本读写功能"""
        # 测试写入
        test_content = "This is a test."
        with open(self.orig_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)

        # 测试读取
        read_content = read_file(self.orig_file_path)
        self.assertEqual(test_content, read_content)

        # 测试写入结果
        write_result(0.88, self.output_file_path)
        with open(self.output_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "0.88")


    # --- 测试核心查重逻辑 ---
    def test_9_plagiarism_check_identical(self):
        """集成测试：测试两个内容相同的文件"""
        content = "完全相同的内容"
        with open(self.orig_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(self.plag_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        plagiarism_check(self.orig_file_path, self.plag_file_path, self.output_file_path)

        with open(self.output_file_path, 'r', encoding='utf-8') as f:
            similarity = float(f.read())
        self.assertAlmostEqual(similarity, 1.00)

    def test_10_plagiarism_check_half_similar(self):
        """集成测试：测试有一定差异的文件"""
        original_content = "abcdefgh"
        plagiarized_content = "abcdwxyz"
        with open(self.orig_file_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        with open(self.plag_file_path, 'w', encoding='utf-8') as f:
            f.write(plagiarized_content)

        # 编辑距离为4 (4次替换), 最大长度为8
        # 相似度 = 1 - (4 / 8) = 0.5
        plagiarism_check(self.orig_file_path, self.plag_file_path, self.output_file_path)

        with open(self.output_file_path, 'r', encoding='utf-8') as f:
            similarity = float(f.read())
        self.assertAlmostEqual(similarity, 0.50)

    def test_11_plagiarism_check_empty_files(self):
        """集成测试：测试两个空文件"""
        open(self.orig_file_path, 'w').close()
        open(self.plag_file_path, 'w').close()

        plagiarism_check(self.orig_file_path, self.plag_file_path, self.output_file_path)
        with open(self.output_file_path, 'r', encoding='utf-8') as f:
            similarity = float(f.read())
        self.assertAlmostEqual(similarity, 1.00)


if __name__ == '__main__':
    unittest.main()