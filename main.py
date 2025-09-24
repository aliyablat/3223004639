import sys


def read_file(file_path: str) -> str:
    """
    读取文件内容。

    Args:
        file_path: 文件路径。

    Returns:
        文件内容字符串。

    Raises:
        SystemExit: 如果文件未找到或读取出错。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: An IO error occurred while reading {file_path}: {e}")
        sys.exit(1)


def write_result(similarity: float, output_path: str):
    """
    将结果写入答案文件，精确到小数点后两位。

    Args:
        similarity: 相似度。
        output_path: 输出文件路径。

    Raises:
        SystemExit: 如果文件写入出错。
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{similarity:.2f}")
    except IOError as e:
        print(f"Error: An IO error occurred while writing to {output_path}: {e}")
        sys.exit(1)


def calculate_edit_distance_v1(s1: str, s2: str) -> int:
    """
    计算两个字符串之间的编辑距离（Levenshtein距离）。

    Args:
        s1: 第一个字符串。
        s2: 第二个字符串。

    Returns:
        编辑距离。
    """
    # 采用递归实现
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    if s1[0] == s2[0]:
        return calculate_edit_distance_v1(s1[1:], s2[1:])
    else:
        return 1 + min(
            calculate_edit_distance_v1(s1[1:], s2),  # 删除 s1 的首字符
            calculate_edit_distance_v1(s1, s2[1:]),  # 在 s1 中插入 s2 的首字符
            calculate_edit_distance_v1(s1[1:], s2[1:])  # 替换 s1 的首字符为 s2 的首字符
        )


def plagiarism_check(original_file_path: str, plagiarized_file_path: str, output_file_path: str):
    """
    论文查重核心算法函数。
    接收文件路径作为参数，计算相似度并写入结果文件。

    Args:
        original_file_path: 原文文件的绝对路径。
        plagiarized_file_path: 抄袭版论文文件的绝对路径。
        output_file_path: 输出答案文件的绝对路径。
    """
    # 读取文件
    original_text = read_file(original_file_path)
    plagiarized_text = read_file(plagiarized_file_path)

    # 计算编辑距离
    distance = calculate_edit_distance_v1(original_text, plagiarized_text)

    # 计算重复率
    max_len = max(len(original_text), len(plagiarized_text))
    if max_len == 0:
        similarity = 1.0  # 两个空字符串视为完全相同
    else:
        # 相似度 = 1 - (差异部分 / 总长度)
        similarity = 1 - (distance / max_len)

    # 写入结果
    write_result(similarity, output_file_path)

    # print(f"Similarity calculation complete. Result has been written to {output_file_path}")


def main():
    """
    程序入口。
    解析命令行参数，并调用核心算法函数。
    """
    args = sys.argv
    if len(args) != 4:
        print("Usage: python main.py <original_file_path> <plagiarized_file_path> <output_file_path>")
        sys.exit(1)

    original_path = args[1]
    plagiarized_path = args[2]
    output_path = args[3]

    plagiarism_check(original_path, plagiarized_path, output_path)


if __name__ == "__main__":
    main()