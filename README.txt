CONNECT 4

how to run:
    install files from github
    run requirements .txt
    run Connect4.py
        python3 Connect4.py <player / ai> <player / ai>
        
        
-Question 1 : “​What heuristic did you use? Why?”
My heuristic value was based off each set of four spots in a row both horizontally, vertically, and diagonally. Each set of four spots counted how many spots were held by a particular player, and returned a value of the sum ^ 2. Thus, if a player had 2 in a row already, that section was valued at 4, with 3 in a row being valued at 9. If a player occupied a spot in the center, then that spot would be accounted for in 7 different sets of 4, with 4 being horizontal sets, 1 being vertical, and 2 being diagonal, thus giving a total score of 7 * (1^2) = 7. This would encourage the AI to pick spots that would optimize chances of getting 4 in a row. If both players occupied the same set of 4 spots, it would return a value of 0, as neither player could get 4 in a row for those particular spots. This would encourage the AI to cut the other player off to limit their score, as stopping a potential 3 in a row would reduce the opponent score by 9. Both player’s scores were calculated by : their score - opponents score, with a 4 in a row equaling +1000 or -1000 respectively.
-”Describe how your algorithm performs given different time constraints. How
much of the tree can you explore given 5 seconds per turn? 10 seconds? 3 seconds?”
My program at depth 5 could unreliably explore the entire tree (with pruning) as sometimes it reaches a time of 60-65 seconds, which is beyond the initial time constraints. For expectimax however, it was much slower, as I could not prune the tree. As such, the best depth for it was 3-4. At depth 3 (ai goes, enemy goes, ai goes, enemy goes) it could reliably perform under 10 seconds, with the time going down as the tree fills. If I was to continue working on this assignment in my own time, I would develop the ai to search in deeper depths as the game progresses, as depths are easier to traverse for my AI when the board is more filled, and as such it would be better at finding win conditions if it was allowed to traverse deeper while still staying inside the time constraints.
- “Can you beat your algorithm?”
While I have not spent enough time playing the algorithm to beat it. I believe I could. I would accomplish this by setting up a scenario where whichever spot the AI goes in, I would win. A scenario like this would be 3 in a row horizontally, with another 3 in a row above it. Thus if the AI attempts to block the first connect 4 , it allows me to stack it giving me the win condition.
However, for this to work, it would have to be in a spot where the AI could not reach for 3 turns, thus being out of the scope of its alpha beta pruning.
-“If your algorithm plays itself, does the player that goes first do better or worse in general? Share some of the results.”
While in Connect Four Game Theory, player 1 usually has the advantage, for me player 2 usually wins. This occurs very late in the game, where it comes down to filling the last row and yellow being forced to support red in it’s win condition. I have only had 2 games where yellow has one, and that was before the entire heuristic function was developed. This leads me to believe my algorithm is better at playing a more defensive style of play, better suited for player 2.
