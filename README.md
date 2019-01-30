# 2-Mighty AI

Developing AI for 2-Mighty card game.

## Game rule

2-Mighty is a variation of Mighty, which is a card game generally played by
5 or 6 players. 2-Mighty is played by only 2 players, which makes it easier
to design AI for the game.

The game mainly has 3 phases.

### Card selection phase

In the first phase, each player takes cards from the shuffled deck.
The player can see a card just for oneself, and decides whether to pick the card or discard it.
If the card is picked, the next card in the deck is buried without being seen by anyone.
If the player decides to discard it, it is buried and the next card goes straight into the player's hand.
Each player takes turns, so in each turn for a player, 1 card is buried and 1 card goes to a player's hand.
After total 13 turns, each player has 13 cards and 26 buried, and 1 card is left on the floor.

### Election phase

In the next phase, each player proposes manifesto of the game.
Manifesto consists of the Kiruda, which is the shape that will be the strongest shape in the game,
and the number of cards the proponent should get to win.
The minimum number of cards is 7 in the 2-Mighty game, and players should propose a manifesto with a higher number.
When a player gives up the proposal, the manifesto of the game is set, and the player who set that becomes 'the lord', and the other becomes 'the opposition party'.
The lord takes the card which was left on the floor, and bury 1 card from his hand (the buried card can be the one taken from the floor).

### Main phase

Starting from the lord, players take turns to hand out a card in each round.
The player who handed out the stronger card wins that round.
The strenght order of cards is as follows:

  1. Mighty
    - Mighty is the strongest card in the game of Mighty, which is by default Ace of spades.
    When the Kiruda is spade, however, it is Ace of diamonds.
  2. Jocker
    - Jocker is second-strongest card in general.
    - An exception is that when it was pulled out by the 'Jocker call' card.
    The Jocker call card is by default clover 3, or heart 3 when the Kiruda is clover.
    When the first player in a round hands out the Jocker call, the player who has the Jocker in his hand must hand it out, and it becomes the weakest card in that round.
    If the player does not have the Jocker in hand, it is considered as a normal clover (or heart) card.
    You can avoid the Jocker call by handing out the Mighty card even if you have the Jocker.
    - Another exception is that when it is handed out in the first or the last round.
    In these rounds, the Jocker is again the most weakest card.
  3. Kiruda
    - If both cards have same shape, the order is determined by the number: A, K, Q, J, 10, ..., 2
  4. Shape of the card which was handed out by the first player in that round
    - As same as 3, the order between the same shape is determined by the number

When the first player of a round hands out a card and you have that shape, you must hand out a card among that shape.
If you don't have that shape, you can hand out the card with any shape, including the Kiruda.
The Mighty or the Jocker can be handed out any time.
