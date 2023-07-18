def dict_generator(user_count, watchlist_count):
    watchlist_user_review = {}
    # user_count = 10
    # watchlist_count = 11
    for i in range(user_count):
        for j in range(watchlist_count):
            watchlist_user_review[i+1] = j+1
    return print(watchlist_user_review)

dict_generator(10, 11)
        