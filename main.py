import itertools
import function as F
import time

start_time = time.time()

hang_2list = [[3,2], [4,4], [2,1,4], [2], [6], [9], [11,1], [1,8], [4,3], [1,7,1], [1,10,1], [1,4,1],
              [1,1,8],[9],[9]]

lie_2list = [[1, 3], [2], [2,4,2], [2,3,2,1], [3,4,2,2], [1,4,2,2], [3, 2, 2], [3,2,3], [4,2,3],
             [2,4,2,3], [3,3,3,3], [2,3,3,3], [6,3,2], [3, 1],[1,4]]


def search_solution(depth, current_solution):
    """
    depth: 当前递归的层数，即当前构建到的行数
    current_solution: 已生成的部分解（前 depth 行的组合）
    """
    global cnt, right_answer
    # print(depth)
    # 如果已经生成了全部行的组合，进入列判断
    if depth == len(hang_2list):
        # 转置得到列组合
        transferred_2list = F.transpose(current_solution)

        # 检查列是否满足条件
        judge_result = True
        for col_index, col in enumerate(transferred_2list):
            if not F.if_match(a_list=col, match_list=lie_2list[col_index]):
                judge_result = False
                break

        # 若满足所有列条件，记录答案并退出递归
        if judge_result:
            right_answer = current_solution[:]
            cnt += 1
        return

    # 遍历当前行的可能组合
    for candidate in all_hang_possible_3list[depth]:
        # 将当前行组合加入到部分解
        current_solution.append(candidate)

        # 剪枝判断
        if not pruning_function(current_solution, depth):
            # 移除最后添加的行，进行下一次迭代
            current_solution.pop()
            continue

        # 递归处理下一行
        search_solution(depth + 1, current_solution)

        # 回溯：移除当前行，尝试下一个组合
        current_solution.pop()


# 剪枝函数，定义剪枝逻辑
def pruning_function(partial_solution, depth):
    rest_num = len(lie_2list) - depth - 1
    transposed_partial_solution = F.transpose(partial_solution)
    for transposed_partial_solution_lie_index, transposed_partial_solution_lie in enumerate(
            transposed_partial_solution):
        rest_fill_num = sum(lie_2list[transposed_partial_solution_lie_index]) - sum(transposed_partial_solution_lie)
        if rest_fill_num < 0:
            return False
        if sum(lie_2list[transposed_partial_solution_lie_index]) > sum(lie_2list[transposed_partial_solution_lie_index]):
            return False
        all_possible_rest_lie = F.get_combinations(list_len=rest_num, num=rest_fill_num)
        if_possible_match = False
        for every_possible_rest_lie in all_possible_rest_lie:
            if F.if_match(a_list=transposed_partial_solution_lie + every_possible_rest_lie,
                          match_list=lie_2list[transposed_partial_solution_lie_index]):
                if_possible_match = True
                break
        if not if_possible_match:
            return False
    return True





if __name__ == "__main__":
    init_possible_to_check = 1
    all_hang_possible_3list = []

    for hang_condition in hang_2list:
        hang_possible_2list = F.get_possible_match(list_len=len(hang_2list), match_list=hang_condition)
        init_possible_to_check *= len(hang_possible_2list)
        all_hang_possible_3list.append(hang_possible_2list)

    print(f"仅仅从行来说，需要验证的有{init_possible_to_check}")

    right_answer = []
    cnt = 0
    search_solution(0, [])
    print("正确答案是：")
    F.display_2list(right_answer)
    print("正确答案有：", cnt, '个。')
    end_time = time.time()
    print(f"程序运行了{end_time - start_time}秒")

