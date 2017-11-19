Udacity AI Nanodegree   
****

&nbsp;

# Isolation Game Player Agent  
_Bertrand Louargant_

&nbsp;
&nbsp;

## 1. Introduction   
<p>
The goal of this project is to create an AI agent for the Isolation game.
<p> 
In the Isolation game, each player move their pawm in a L-shaped step alternately.
Each box on the grid can be visited only once so that the number of possible moves decrease at each turn.
The player that doesn't have any remaining move available loose the game.

## 2. Heuristics analysis   
In addition to the AlphaBeta Pruning strategy we have been tasked to develop 
three different heuristics and compare their ability to win.   
As the game is lost by the player that cannot move anymore, then the overall strategy is to try to restrain the opponent's movements.   
In this context, for each functions we return the score of the player minus three times the score of it's opponent.   
The three heuristics are:  

* Center first (custom_score):   
For this approach we introduce a new function, weighted_move, that return a weight equal to square of the distance from the center of the
board to a given position.    
The function add up all the weighted potentials moves of the player and compare it the sum of the weighted moves of it's opponent. 
* Plan ahead (custom_score_2):   

* A mix of both previous function (custom_score_3):

## 3. Results  


|               |   AB_Improved  |   AB_Custom   |   AB_Custom_2 |   AB_Custom_3  |
| ------------- | :------------: | :-----------: | :-----------: | :-----------:  |
| **Opponent**  | **Won / Lost** | **Won / Lost**| **Won / Lost**| **Won / Lost** |
| Random        | **`8`** / `2`  | **`10`** / `0`| **`10`** / `0`| **`7`** / `3`  |
| MM_Open       | `5`   /   `5`  | **`6`** / `4` | **`6`** / `4` | **`8`** / `2`  |
| MM_Center     | **`7`** / `3`  | **`8`** / `2` | **`7`** / `3` | **`8`** / `2`  |
| MM_Improved   | **`7`** / `3`  | **`6`** / `4` | **`8`** / `2` | **`8`** / `2`  |
| AB_Open       | `5`    /  `5`  | **`7`** / `3` | `5`  /   `5`  | `4`  / **`6`** |
| AB_Center     | `3`  / **`7`** | **`6`** / `4` | **`6`** / `4` | **`6`** / `4`  |
| AB_Improved   | **`6`** / `4`  | `5`  /   `5`  | `5`  /   `5`  | **`7`** / `3`  |
| **Win Rate:** |<font color="Blue">58.6%</font>|<font color="Blue">68.6%</font>|<font color="Blue">67.1%</font>|<font color="Blue">68.6%</font>|

                              