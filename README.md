# Most-Profitable-March-Madness-Bracket
This was inspired by a March Madness game predictor I made last year.
In many March Madness fan competitions, picking not what is the MOST LIKELY result, but the MOST PROFITABLE result is critical.
This accounts for the fact that higher seeds earn more points than lower seeds, while not just having the higher seed win every game (this scenario is actually a TERRIBLE strategy, yielding an overall net expected return of around -213 points).
To run this, you need to copy and paste the source code for Kenpom to your machine. Then, copy the path and paste it in the "Paste Kenpom .html file here: " space.
After that, it asks how many tournaments to simulate. For reference, it takes about 8 seconds to simulate 100 tournaments on my Mac M1.
The result will include a list of the winners of each game, as well as what its overall expected return is (this will choose whichever simulation yielded the most expected points).
IMPORTANT: This simulator makes the assumption that your competition multiplies the base number of points (equal to 2 ^ whichever round you're in, with 0 being the first) by the seed (i.e. in round 2, a 16 seed winning would be 2^1 * 16 = 32 points).
Enjoy and best of luck with your bracket!
