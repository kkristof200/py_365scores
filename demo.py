from scores import Scores

scores = Scores(debug=True)
games = scores.get_games(only_major_games=True)
# games = Scores(debug=True).get_games()
# games = Scores(debug=True).get_games(include_cancelled=True, include_postponed=True)
# games = Scores(debug=True).get_games(include_cancelled=True, include_postponed=True, only_major_games=True)

print(len(games))

games[0].jsonprint()

scores.download_assets(games[0]).jsonprint()