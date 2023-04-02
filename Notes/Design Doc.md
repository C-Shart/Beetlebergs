GAME DESIGN DOC - LEGALLY DISTINCT BEETLEBERGS
==============================================

CORE CONCEPT
============
Two teams of beetles. Each round, they fight, and the player guesses which one will win. If the player guesses right, the loser gains an evolution and +1 beetle. The player then predicts a winner for the next round.


MAIN FEATURES
=============
+ Basic mode: 2 teams of beetles fight
+ more types of bug (with their own basic stats & evolutions?) - this would be for after we get the beetles down maybe
+ VS mode: Save your favorite bug teams in basic mode to fight them against each other
+ VS mode: Create a custom team of beetles with 2-3 evolutions each, selected by the player, to test (cannot save these teams)
+ Tournaments - subset of VS mode? Pit beetle teams vs each other in brackets? For fun?


DEVELOPMENT MILESTONES
======================
+ First basic beetle coded (minimum: movement/turning, attack cycle)
+ First evolution created & implemented (basic beetle can take in evo, evo changes beetle behavior accordingly)
+ Special beetles implemented (Queen, Elite, ??)
+ First successful 1v1 battle round from start to finish, & first successful many-v-many battle round from start to finish
+ Special behaviors implemented: larvae spawning, cannibal feeding, teleporting(?), anything that isn't basic movement/turning & attack cycle)
+ First successful alpha-complete(?) game from round 1 to round n: evolutions, determination of win/loss, etc.
+ Creation of player profile/data (to store/track unlocks, metrics, and progress)
+ 


PLAYER EXPERIENCE AND GAME POV
==============================
+ Top-down omniscient perspective
+ Player is mostly hands off, but I would like to include a way for the player to actually engage and influence. This may interact strongly with the core idea of switching which team you vote for/control, or may not make a difference. Perhaps player interactions or orders can be a consumable resource, e.g. player has 3 Move Heres at the beginning of a match.
	++ Ideas:
	++ A special beetle type, or Queen subtype, that allows the player limited control over the beetles. e.g.: Basic beetles generally stay within X radius of Controllable Queen subtype, CQ goes roughly where player clicks (accuracy & speed modifiable?) and meanders around that general spot, basics follow. Player disadvantage: have to manually spawn larvae when available.
	++ UI that grants player some high-level controls over general bug posture rather than specific actions, e.g. Aggressive/Hold/Defensive, Focus Fire, Use Special Abilities
+ Perhaps at the end of the game, when your chosen team has lost, you can choose whether to keep the team (save team for VS mode (maybe breeding??)), or to let the team be devoured by the winners? Some kind of risk/reward for each.
	++ FLAVOR: haha maybe the PLAYER can devour their losing team!!



CORE LOOPS
==========
Action: 
	+ Basic: Teams of beetles fight a number of rounds until the player guesses wrong (or other game-over condition)
	+ VS: like basic, but you can pick from pre-selected teams (either winning/losing teams from basic mode, or maybe you can create a custom low-level team to experiment with mutation combinations)

Rewards: 
	+ Evolution points? Could be used to unlock new evolutions, beetle types, or features

Expansion: 
	+ Unlock special beetle types (elites, queens, ?)
	+ ability to increase/decrease # of evolutions both teams start with
	+ ability to pick 1 free additional evolution in the beginning and grant it to team of your choice
	+ Increase available # of slots for custom teams in VS mode
	+ (depending on player involvement implementation) Unlock special player-directed actions, e.g. Focus Fire, Move Here

Example:
	1. Player starts a game
	2. Two beetle teams created with a starting evolution each.
	3. Player predicts Team 2 will win.
	4. Team 2 wins.
	5. Losing team (Team 1) gains an evolution and +1 basic beetle
	6. Player predicts Team 1 will win.
	7. Team 2 wins somehow.
	8. Because it only lasted one round, player receives low amount of evo points, and is given the choice to keep the team or have it devoured. Player chooses to devour their team.
	9. Player given choices: Start New Match, Game Stats(?), Main Menu
