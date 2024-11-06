import itertools
import time
import tkinter as tk
from tkinter import messagebox


start_time = time.time()

#hang_2list = [[3, 2], [4, 4], [2, 1, 4], [2], [6], [9], [11, 1], [1, 8], [4, 3], [1, 7, 1], [1, 10, 1], [1, 4, 1],
#              [1, 1, 8], [9], [9]]

#lie_2list = [[1, 3], [2], [2, 4, 2], [2, 3, 2, 1], [3, 4, 2, 2], [1, 4, 2, 2], [3, 2, 2], [3, 2, 3], [4, 2, 3],
#             [2, 4, 2, 3], [3, 3, 3, 3], [2, 3, 3, 3], [6, 3, 2], [3, 1], [1, 4]]

right_answer = None


def near_list(a_list):
    result = []
    i = 0
    while i < len(a_list):
        if a_list[i] == 1:
            count = 1  # 计数当前的1
            # 计算右边连续的1
            j = i + 1
            while j < len(a_list) and a_list[j] == 1:
                count += 1
                j += 1
            result.append(count)
            i = j  # 跳过已经计数的1
        else:
            i += 1
    return result


def if_match(a_list, match_list):
    if near_list(a_list) == match_list:
        ret = True
    else:
        ret = False
    return ret


def if_match_num(a_list, num):
    cnt = 0
    ret = False
    for item in a_list:
        if item:
            cnt += 1
    if cnt == num:
        ret = True
    return ret


def get_init_list(num):
    ret_list = []
    for i in range(num):
        ret_list.append(0)
    return ret_list


def get_combinations(list_len, num):
    # 初始化列表
    result = []
    # 生成所有可能的m个位置放1的组合
    for positions in itertools.combinations(range(list_len), num):
        # 创建一个长度为n的列表，初始化为0
        combination = [0] * list_len
        # 在指定的位置放1
        for pos in positions:
            combination[pos] = 1
        # 将该组合加入结果列表
        result.append(combination)
    return result


def get_possible_match(list_len, match_list):
    ret_list = []
    all_match_num_2list = get_combinations(list_len=list_len, num=sum(match_list))
    for all_match_num_list in all_match_num_2list:
        if if_match(all_match_num_list, match_list):
            ret_list.append(all_match_num_list)
    return ret_list




def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def display_2list(a_2list):
    for line in a_2list:
        print(line)

def search_solution(depth, current_solution, hang_2list, lie_2list):
    """
    depth: 当前递归的层数，即当前构建到的行数
    current_solution: 已生成的部分解（前 depth 行的组合）
    """
    global right_answer
    # print(depth)
    # 如果已经生成了全部行的组合，进入列判断
    right_answer = []
    if depth == len(hang_2list):
        # 转置得到列组合
        transferred_2list = transpose(current_solution)

        # 检查列是否满足条件
        judge_result = True
        for col_index, col in enumerate(transferred_2list):
            if not if_match(a_list=col, match_list=lie_2list[col_index]):
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
    transposed_partial_solution = transpose(partial_solution)
    for transposed_partial_solution_lie_index, transposed_partial_solution_lie in enumerate(
            transposed_partial_solution):
        rest_fill_num = sum(lie_2list[transposed_partial_solution_lie_index]) - sum(transposed_partial_solution_lie)
        if rest_fill_num < 0:
            return False
        if sum(lie_2list[transposed_partial_solution_lie_index]) > sum(
                lie_2list[transposed_partial_solution_lie_index]):
            return False
        all_possible_rest_lie = get_combinations(list_len=rest_num, num=rest_fill_num)
        if_possible_match = False
        for every_possible_rest_lie in all_possible_rest_lie:
            if if_match(a_list=transposed_partial_solution_lie + every_possible_rest_lie,
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
        hang_possible_2list = get_possible_match(list_len=len(hang_2list), match_list=hang_condition)
        all_hang_possible_3list.append(hang_possible_2list)

    search_solution(0, [], hang_2list=hang_2list, lie_2list=lie_2list)
    print("正确答案是：")
    # display_2list(right_answer)
    end_time = time.time()
    print(f"程序运行了{end_time - start_time}秒。")
    return right_answer



root = tk.Tk()
root.title("树织问题求解器")

# 行约束和列约束输入框
entries_hang = {}
entries_lie = {}
for i in range(15):
    tk.Label(root, text=f"行{i + 1}约束:").grid(row=i, column=0)
    entry_hang = tk.Entry(root, width=10)
    #entry_hang.insert(tk.END, ','.join(map(str, hang_2list[i])))
    entry_hang.grid(row=i, column=1)
    entries_hang[f'hang{i}'] = entry_hang

    tk.Label(root, text=f"列{i + 1}约束:").grid(row=i, column=2)
    entry_lie = tk.Entry(root, width=10)
    #entry_lie.insert(tk.END, ','.join(map(str, lie_2list[i])))
    entry_lie.grid(row=i, column=3)
    entries_lie[f'lie{i}'] = entry_lie

# 显示解的结果矩阵
result_canvas = tk.Canvas(root, width=400, height=400)
result_canvas.grid(row=4, column=15, rowspan=15, columnspan=15)


# 求解按钮的点击事件
def on_run_clicked():
    try:
        global hang_2list
        global lie_2list
        global right_answer
        hang_2list = [list(map(int, entries_hang[f'hang{i}'].get().split(','))) if entries_hang[f'hang{i}'].get() else [] for i in range(15)]
        lie_2list = [list(map(int, entries_lie[f'lie{i}'].get().split(','))) if entries_lie[f'lie{i}'].get() else [] for i in range(15)]
        solve(hang_2list, lie_2list)
        right_answer_tk = right_answer[:]
        if right_answer_tk:
            print(right_answer_tk)
            display_result(right_answer_tk)
        else:
            messagebox.showerror("无解！","无解！")
    except ValueError:
        right_answer = []
        messagebox.showerror("错误", "请输入有效的数字")


# 在 Canvas 上显示结果矩阵
def display_result(right_answer_tk):
    cell_size = 20
    result_canvas.delete("all")
    for i, row in enumerate(right_answer_tk):
        for j, val in enumerate(row):
            color = "black" if val == 1 else "white"
            result_canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size,
                                           fill=color)


# 创建并布局运行按钮
button_run = tk.Button(root, text="运行", command=on_run_clicked)
button_run.grid(row=18, column=0, columnspan=4)

# 运行主窗口
root.mainloop()
