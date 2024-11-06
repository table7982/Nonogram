import itertools
import time



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


if __name__ == "__main__":

    start_time = time.time()  # 记录开始时间
    every_lun_time = 4.364426513910383e-6
    hang_2list = [
        [1],
        [4, 2],
        [7, 1],
        [4, 1],
        [2, 3],
        [9],
        [1, 6],
        [8],
        [1, 1, 1],
        [2, 5],

    ]

    lie_2list = [
        [1, 3],
        [2, 1, 3],
        [8, 1],
        [7],
        [3, 3],
        [2, 5],
        [2, 3, 1],
        [1, 6],
        [3, 1],
        [1, 1, 1],

    ]

    all_hang_possible_3list = []
    all_possible_3list = []
    all_possible_list = []
    for index, hang_match_list in enumerate(hang_2list):
        every_possible_2list = get_possible_match(len(hang_2list), hang_match_list)
        all_hang_possible_3list.append(every_possible_2list)

    num_to_check = 1
    for all_hang_possible_3list_index in range(len(all_hang_possible_3list)):
        num_to_check *= len(all_hang_possible_3list[all_hang_possible_3list_index])
    print(num_to_check)

    print(f"预计需要{round(num_to_check * every_lun_time, 2)}秒")
    right_answer = []
    cnt = 0
    for a in all_hang_possible_3list[0]:
        for b in all_hang_possible_3list[1]:
            for c in all_hang_possible_3list[2]:
                for d in all_hang_possible_3list[3]:
                    for e in all_hang_possible_3list[4]:
                        for f in all_hang_possible_3list[5]:
                            for g in all_hang_possible_3list[6]:
                                for h in all_hang_possible_3list[7]:
                                    for i in all_hang_possible_3list[8]:
                                        for j in all_hang_possible_3list[9]:

                                            all_possible_list.append(a)
                                            all_possible_list.append(b)
                                            all_possible_list.append(c)
                                            all_possible_list.append(d)
                                            all_possible_list.append(e)
                                            all_possible_list.append(f)
                                            all_possible_list.append(g)
                                            all_possible_list.append(h)
                                            all_possible_list.append(i)
                                            all_possible_list.append(j)

                                            transferred_2list = transpose(all_possible_list)
                                            judge_result = True
                                            # display_2list(transferred_2list)
                                            for every_lie_list_index, every_lie_list in enumerate(transferred_2list):
                                                result = if_match(a_list=every_lie_list,
                                                                  match_list=lie_2list[every_lie_list_index])
                                                if not result:
                                                    judge_result = False
                                                if not judge_result:
                                                    break

                                            if judge_result:
                                                # print("正确答案是：\n")
                                                #display_2list(all_possible_list)
                                                right_answer = all_possible_list
                                                break
                                            if cnt % 1000000 == 1:
                                                print("---------------")
                                                print(f'预计还剩下{round((num_to_check-cnt)*every_lun_time,2)}秒')
                                                print(f'现在进行到{cnt}轮，共{num_to_check}轮,进度{round(cnt / num_to_check * 100,5)}%')
                                            cnt += 1
                                            all_possible_list = []
                                            if right_answer:
                                                break
                                        if right_answer:
                                            break
                                    if right_answer:
                                        break
                                if right_answer:
                                    break
                            if right_answer:
                                break
                        if right_answer:
                            break
                    if right_answer:
                        break
                if right_answer:
                    break
            if right_answer:
                break
        if right_answer:
            break

    end_time = time.time()  # 记录结束时间
    print(f"运行了{cnt}次，运行了{round(end_time-start_time,2)}秒,找到了答案。")
    print(f"你在{round(cnt/num_to_check*100,2)}%就找到了答案")
    display_2list(transpose(right_answer))
