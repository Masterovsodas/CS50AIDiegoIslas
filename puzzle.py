from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # facts
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    # connections
    Implication(AKnave, Not(And(AKnight, AKnave))),
    Implication(AKnight, And(AKnave,AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement = And(AKnave, BKnave)
knowledge1 = And(
   #facts
   Not(And(AKnight, AKnave)),
   Or(AKnight, AKnave),
   Not(And(BKnight, BKnave)),
   Or(BKnight,BKnave),

   # connections
   Implication(AKnight, statement),
   Implication(AKnave, Not(statement))
)

# Puzzle 2
# A says "We are the same kind."
sentence0 = Or(And(AKnight, BKnight), And(AKnave,BKnave))
# B says "We are of different kinds."
sentence1 = Or(And(AKnight,BKnave), And(AKnave, BKnight))

knowledge2 = And(
    #facts
   Not(And(AKnight, AKnave)),
   Or(AKnight, AKnave),
   Not(And(BKnight, BKnave)),
   Or(BKnight,BKnave),

   # connections
   # sentences are contradictory
   Implication(sentence0, Not(sentence1)),
   Implication(sentence1, Not(sentence0)),

   Implication(AKnight, Not(sentence1)),
   Implication(BKnight, Not(sentence0)),
   Implication(AKnave, sentence1),
   Implication(BKnave, sentence0)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. Knight
idea0 = Or(AKnight, AKnave)
# B says "A said 'I am a knave'." Knave
sentence1 = AKnave
# B says "C is a knave." Knave
sentence2 = CKnave
# C says "A is a knight." Knight
sentence3 = AKnight

# NOTHING CAN EVER SAY "I AM A KNAVE"; BECAUSE THEN IT CANT BE A KNIGHT CAUSE THEY ALWAYS TELL TRUTH AND A KNAVE WOULD BE LYING
knowledge3 = And(
   # facts
   Not(And(AKnight, AKnave)),
   Or(AKnight, AKnave),
   Not(And(BKnight, BKnave)),
   Or(BKnight, BKnave),
   Not(And(CKnight, CKnave)),
   Or(CKnight, CKnave),

    # connections
    Implication(sentence1, Not(idea0)),
    Implication(sentence2, Not(sentence3)),
    Implication(sentence3, And(Not(sentence2), Not(sentence1))),
    Implication(BKnight, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
