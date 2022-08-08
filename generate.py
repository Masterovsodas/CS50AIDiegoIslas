import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # check domains of all variables
        for var in self.crossword.variables:
            # cause of "Set changed size during iteration" error, a temp array will be used
            toRemove = []

            for val in self.domains[var]:
                # POSSIBLE SYNTAX ISSSSSSUUUUUUUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
                if len(val) != var.length:
                    toRemove.append(val)
            # now truncate
            for i in toRemove:
                self.domains[var].remove(i)
        return None

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # can assume a valid arc has been passed in???
        revised = False
        constraint = self.crossword.overlaps[x, y]
        # x char position = constraint[0]
        # y char position = constraint[1]
       
        # temp array to prevent removal issues
        xdoms = self.domains[x].copy()
        # for every value left in X domain 
        for valx in xdoms:
            # all x vals need one compatible Y at least
            worksOnce = False
            # for every value left in Y domain 
            for valy in self.domains[y]:
                # check if they have the same letter at the constraint indexes; and are long enough to have that constraint index
                if (len(valx) > constraint[0] and len(valy) > constraint[1]) and valx[constraint[0]] == valy[constraint[1]]:
                    # if they do, note that this X has a potential partner
                    worksOnce = True

            # if this X works with NO Y's, KILL IT!!
            if worksOnce == False:
                revised = True
                self.domains[x].remove(valx)
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            # get all arcs
            arcs = []
            for key in self.crossword.overlaps:
                # NOTE: KEY MAY NOT ACTUALLY BE IN THE TUPLE FORM WE WANT TO SPLIT FOR THE ARGS OF REVISE; POTENTIAL EXPLOSION SPOT HERE
                arcs.append(key)

        while len(arcs) != 0:
            # dequeue
            arc = arcs.pop(0)
            if self.crossword.overlaps[arc] == None:
                continue

            if self.revise(arc[0], arc[1]):
                # if less than zero, current model is not solvable
                if len(self.domains[arc[0]]) <= 0:
                    return False
                # get neighbors of arc[0]
                for neighbor in self.crossword.neighbors(arc[0]):
                    if neighbor == arc[1]:
                        continue
                    arcs.append((neighbor, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for key in assignment:
            # if any vars not assigned, return false
            if assignment[key] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # node conistency (length issue) already adressed
        # run AC3 to check for conflicts
        if not self.ac3():
            return False
        
        # check uniqueness
        for i in assignment:
            for j in assignment:
                if i == j:
                    continue
                if assignment[i] == assignment[j] and assignment[i] != None:
                    # if not same var and same value that isnt none, we have dupes, oops
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # dict of scores where values are keys
        scores = {}
        # rule out based on duplicity, and neighbor overlap conditions
        for value in self.domains[var]:
            # initialize score
            scores[value] = 0

            # check for duplicity NOT ASSIGNED VARS
            for nvar in self.crossword.variables:
                # if any domain not belonging to var has assignment, add one
                if assignment[nvar] == None and value in self.domains[nvar] and nvar != var:
                    scores[value] += 1

            # check for conflictive ruling out, (ie: given assignment of this value, will the overlap indexes still be fulfilled)
            for neighbor in self.crossword.neighbors(var):
                # get overlap
                constraint = self.crossword.overlaps[var, neighbor]

                # based on overlap see what gets ruled out given the theoretical assignment
                for neighValu in self.domains[neighbor]:
                    if value[constraint[0]] != neighValu[constraint[1]]:
                        scores[value] += 1

        # sort by least constraining, key = values
        finalOrder = []
        clowest = None
        # do over and over until scores is clear and final order has everything
        while len(finalOrder) < len(self.domains[var]):
            newApp = None
            for key in scores:
                # initial
                if clowest == None:
                    clowest = scores[key]
                    newApp = key
                    continue
                
                if scores[key] < clowest:
                    newApp = key
            finalOrder.append(newApp)
            # remove dict value
            scores.pop(newApp, None)
        return finalOrder

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        clowestValue = None
        withValue = []
        for var in assignment:
            # if an assignment is present on this var don't select it
            if assignment[var] != None:
                continue
            # initially set lowest domain count to first var
            if clowestValue == None:
                clowestValue = len(self.domains[var])
                withValue.append(var)
                continue

            # check if new var has less values in domain
            if len(self.domains[var]) < clowestValue:
                clowestValue = len(self.domains[var])
                # clear withValue
                withValue = []
                withValue.append(var)

            # check if new var has equal values in domain
            if len(self.domains[var]) == clowestValue:
                withValue.append(var)

        # if empty due to full assignment
        if withValue == []:
            return None

        # do degree check
        if len(withValue) > 1:
            mostNeighbors = {}
            currHigh = 0
            for var in withValue:
                mostNeighbors[var] = len(self.crossword.neighbors(var))

                if len(self.crossword.neighbors(var)) > currHigh:
                    currHigh = len(self.crossword.neighbors(var))

            # clear withValue and reappend vars tied for neighbor counts
            withValue = []
            for key in mostNeighbors:
                if mostNeighbors[key] == currHigh:
                    withValue.append(key)

        # if a still tie exists and more than one variable is under this array, this is technically an arbitrary choice. If only one winner exists in the array, it will be at this index  no doy
        return withValue[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # initially fill the empty dict with JUST KEYS
        if assignment == {}:
            for var in self.crossword.variables:
                # initialize new key and empty val
                assignment[var] = None

        if self.assignment_complete(assignment):
            return assignment

        # get random var
        var = self.select_unassigned_variable(assignment)
        # cycle over whole domain, to see if any assignment is fit
        # make temp in case of domain restriction issues
        currDom = self.order_domain_values(var, assignment)
        for value in currDom:
            # try out this assignment, also restrict domain becasue of possible assignment
            assignment[var] = value
            self.domains[var] = []
            self.domains[var].append(value)

            if self.consistent(assignment):
                result = self.backtrack(assignment)

                # if result isnt none, we will have the result of the assignment complete condition from the top, keep spitting it up
                if result != None:
                    return result
            # RESET
            assignment[var] = None
            self.domains[var] = currDom
        # no working assignment was found, unfortunate
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()
    
    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
           creator.save(assignment, output)


if __name__ == "__main__":
    main()
    
    

