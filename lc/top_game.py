lines = [
    "1500000000,user1,1001,join",
    "1500000010,user1,1002,join",
    "1500000015,user1,1002,quit",
    "1500000020,user1,1003,quit",
]


def process(event_list):
    """
    if only join: = min(next_join, avg_time)
    if only quit: = min(previous_quit, avg_time)

    current_event:
    1. join
      1. next is same quit
      2. next is other, use that as quit time
    2. quit
      1. previous event as join

    prepare a temporary list to process lastly
    """
    total_score = 0
    total_game = 0
    corruped_games = []
    i = 0
    while i < len(event_list):
        current_event = event_list[i]
        if current_event[2] == "join":
            if i + 1 >= len(event_list):
                break
            next_event = event_list[i+1]
            if next_event[1] == current_event[1] and next_event[2] == "quit":  # same game
                print(current_event[1], next_event[0] - current_event[0])
                i += 2
                continue
            corruped_games.append((current_event[1], next_event[0] - current_event[0]))
            i += 1
        else:  # is quit
            if i - 1 >= 0:  # has previous
                previous_event = event_list[i - 1]
                corruped_games.append((current_event[1], current_event[0] - previous_event[0]))
            else:  # no previous, discard
                pass
            i += 1
    print(corruped_games)


def find_top_game(lines):
    # key is game
    game_score = {}
    # key is user, value is list
    user_event = {}
    for line in lines:
        ts, user_id, game_id, action = line.split(",")
        ts = int(ts)
        if user_id in user_event:
            user_event[user_id].append((ts, game_id, action))
        else:
            user_event[user_id] = [(ts, game_id, action)]

    for user_id, event_list in user_event.items():
        process(event_list)
    print(user_event)


find_top_game(lines)
