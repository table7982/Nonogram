import itertools
import function as F
import time

start_time = time.time()

hang_2list_model = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

lie_2list_model = [[15], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

right_answer = None


def search_solution(depth, current_solution, hang_2list, lie_2list):
    """
    depth: 当前递归的层数，即当前构建到的行数
    current_solution: 已生成的部分解（前 depth 行的组合）
    """
    global right_answer
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
            print("有解")
            print(right_answer)
        return

    # 遍历当前行的可能组合
    for candidate in all_hang_possible_3list[depth]:
        # 将当前行组合加入到部分解
        current_solution.append(candidate)

        # 剪枝判断
        if not pruning_function(current_solution, depth, lie_2list):
            # 移除最后添加的行，进行下一次迭代
            current_solution.pop()
            continue

        # 递归处理下一行
        search_solution(depth + 1, current_solution, hang_2list=hang_2list, lie_2list=lie_2list)

        # 回溯：移除当前行，尝试下一个组合
        current_solution.pop()


# 剪枝函数，定义剪枝逻辑
def pruning_function(partial_solution, depth, lie_2list):
    rest_num = len(lie_2list) - depth - 1
    transposed_partial_solution = F.transpose(partial_solution)
    for transposed_partial_solution_lie_index, transposed_partial_solution_lie in enumerate(
            transposed_partial_solution):
        rest_fill_num = sum(lie_2list[transposed_partial_solution_lie_index]) - sum(transposed_partial_solution_lie)
        if rest_fill_num < 0:
            return False
        if sum(lie_2list[transposed_partial_solution_lie_index]) > sum(
                lie_2list[transposed_partial_solution_lie_index]):
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


'''
if __name__ == "__main__":
    init_possible_to_check = 1
    all_hang_possible_3list = []

    for hang_condition in hang_2list:
        hang_possible_2list = F.get_possible_match(list_len=len(hang_2list), match_list=hang_condition)
        init_possible_to_check *= len(hang_possible_2list)
        all_hang_possible_3list.append(hang_possible_2list)

    print(f"仅仅从行来说，需要验证的有{init_possible_to_check}")
    for all_combine in itertools.product(*all_hang_possible_3list):
        print(len(all_combine))
        break
    right_answer = []
    cnt = 0
    search_solution(0, [])
    print("正确答案是：")
    F.display_2list(right_answer)
    print("正确答案有：", cnt, '个。')
    end_time = time.time()
    print(f"程序运行了{end_time - start_time}")
'''


def solve(hang_2list, lie_2list):
    global all_hang_possible_3list
    all_hang_possible_3list = []
    for hang_condition in hang_2list:
        hang_possible_2list = F.get_possible_match(list_len=len(hang_2list), match_list=hang_condition)
        all_hang_possible_3list.append(hang_possible_2list)

    search_solution(0, [], hang_2list=hang_2list, lie_2list=lie_2list)
    print("正确答案是：")
    F.display_2list(right_answer)
    end_time = time.time()
    print(f"程序运行了{end_time - start_time}秒。")
    return right_answer


solve(hang_2list_model, lie_2list_model)
