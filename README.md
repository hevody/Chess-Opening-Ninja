Improve your chess.com elo with this program!  
This tool can present your most played openings to the least played openings depending on the colors you played (in other words, white or black)  

### How is Chess Opening Ninja useful?  
1. Knowing your most played openings will help you prevent pitfalls early in the game  
2. Since the opening is frequently played, there is a high chance that it will also be played in the future games which can prepare you for the attacks in advance  
3. This program can also help you discover variations of your favorite opening and take advantage of them  

### Instructions / Manual  

Note: This only works in Chess.com so far...  

1. Clone this repository first  

Either by  
```
Click Code > Download ZIP
```
or  
```
git clone https://github.com/hevody/Chess-Opening-Ninja.git
```

2. Run the code!  
```bash
python "opening ninja.py"
```
Simple as that!  

It will prompt you to enter your Chess.com username so just enter what your username is  
It will load for a moment as it calls the Chess.com API (so don't panic!)  

Once, done loading this prompt will appear:
```
Which side of your games would you like to analyze?
        (1) White
        (2) Black
        (3) Both
```
Enter 1, if you would like to view your most used opening as White  
Enter 2, if you would like to ... as Black  
Enter 3, if yoouu want to see both!  

Once you made up your mind:  
The results will appear (and will also be solved in a .txt file so you can view it whenever)  

The results will look somewhat like this:
```
The analysis for White openings by frequency:
1. Queens-Gambit-Accepted-Old-Variation - played 37 time(s)!
2. Englund-Gambit-2.dxe5-Nc6-3.Nf3-Qe7 - played 31 time(s)!
3. Queens-Gambit-Declined-Marshall-Defense - played 28 time(s)!
...
19. Pirc-Defense-Classical-Variation-4...Bg7-5.Bf4-O-O-6.Qd2 - played 1 time(s)!
19. Indian-Game-2.Bf4-d6-3.Nc3-Nbd7 - played 1 time(s)!
19. Queens-Gambit-Declined-Modern-Variation-4...c6-5.cxd5-exd5 - played 1 time(s)!

The analysis for Black openings by frequency:
1. Sicilian-Defense-Bowdler-Attack-2...Nc6 - played 55 time(s)!
2. Sicilian-Defense - played 47 time(s)!
3. Sicilian-Defense-Old-Sicilian-Variation-3.Bc4 - played 38 time(s)!
...
21. Sicilian-Defense-McDonnell-Attack-2...e6-3.Nf3 - played 1 time(s)!
21. Sicilian-Defense-Kramnik-Variation-3...Nc6-4.Nc3 - played 1 time(s)!
21. Queens-Gambit-Declined-Pseudo-Tarrasch-Defense - played 1 time(s)!
```

