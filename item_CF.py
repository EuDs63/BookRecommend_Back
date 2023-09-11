import numpy as np
from models.user_rating import UserRating
import pickle


def ItemSimilarity(train):
    N = {}  # 初始化N字典,记录每个物品被反馈过的用户数
    C = {}  # 初始化C字典,记录共同喜欢两个物品的用户数
    for u, items in train.items():
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1
            for j in items:
                if i == j:
                    continue
                C.setdefault(i, {})
                C[i].setdefault(j, 0)
                C[i][j] += 1
                print("正在收集数据")
    W = {}  # 计算物品 i 和 j 的相似度矩阵
    for i, related_items in C.items():
        W.setdefault(i, {})
        for j, cij in related_items.items():
            W[i][j] = cij / np.sqrt(N[i] * N[j])
            print("正在计算")
    # 保存相似度矩阵到文件
    with open('similarity_matrix.pkl', 'wb') as file:
        pickle.dump(W, file)
    return W


# # 加载相似度矩阵
# with open('similarity_matrix.pkl', 'rb') as file:
#     W = pickle.load(file)
def Recommendation(train, user_id, W, K):
    rank_rs = {}
    u_items = train[user_id]
    for i, rui in u_items.items():
        for j, wij in sorted(W[i].items(), key=lambda x: x[1], reverse=True)[0:K]:
            if j in u_items:
                continue
            rank_rs.setdefault(j, 0)
            rank_rs[j] += rui * wij
    top_k_recommendations = dict(sorted(rank_rs.items(), key=lambda x: x[1], reverse=True)[:K])
    return top_k_recommendations  # 键为bookId,值为bookRating的字典


def getBookRating(book_id, user_id):  # 这里通过数据库得到用户对这本书的打分（1~5星），返回一个整数
    pass


def isBookCollected(book_id, user_id):  # 想读在读已读都返回1，否则返回0
    pass


def isBookHavingComments(book_id, user_id):  # 检查用户是否对这本书有评论，有返回1，没有返回0
    pass


# 这里的训练数据是一个字典，键是userId,值是相应打过分的item列表(item列表就是bookId列表)。
# 最后会生成一个字典，键是userId，值是一个字典（键是item,值是rating）
def generateBookRating(train):
    user_book_ratings = {}  # 最终的用户-图书评分数据结构
    for user_id, rated_books in train.items():
        user_rating_dict = {}  # 每个用户的评分字典
        for book_id in rated_books:
            rating_score = 0
            # 获取图书评分和其他信息
            rating = getBookRating(book_id, user_id)
            is_book_collected = isBookCollected(book_id, user_id)
            is_book_having_comments = isBookHavingComments(book_id, user_id)
            # 根据评分和其他信息计算评分分数
            if rating == 5:
                rating_score += 2
            elif rating == 4:
                rating_score += 1
            else:
                rating_score -= 1
            if is_book_collected:
                rating_score += 1
            if is_book_having_comments:
                rating_score += 2

            # 将每本书籍及其评分分数添加到用户的评分字典中
            user_rating_dict[book_id] = rating_score
        # 将用户的评分字典添加到用户-图书评分数据结构中
        user_book_ratings[user_id] = user_rating_dict
    return user_book_ratings


# 示例输入数据格式（train）：
# train = {
#    'user1': {'item1', 'item2', 'item3'},
#    'user2': {'item2', 'item4', 'item5'},
#    # 其他用户的评分过的书籍数据
# }

# 示例输出数据格式（user_book_ratings）：
# user_book_ratings = {
#     'user1': {'item1': 5, 'item2': 5, 'item3': 5},
#     'user2': {'item2': 5, 'item4': 5, 'item5': 5},
#     ...
# }

# test_train = {
#     'user1': {'item1', 'item2', 'item3'},
#     'user2': {'item2', 'item4', 'item5'},
#     # 其他用户的评分过的书籍数据
# }

user_book_ratings = generateBookRating(test_train)  # 需要从数据库给出这个
W = ItemSimilarity(user_book_ratings)
# with open('similarity_matrix.pkl', 'rb') as file:  # 算出一次W之后就用这里直接引入W
#     W = pickle.load(file)
user_id = 'user1'
K = 10
recommendations = Recommendation(user_book_ratings, user_id, W, K)
print(recommendations)
