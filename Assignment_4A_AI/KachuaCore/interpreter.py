
from kast import kachuaAST
import turtle

Release="Kachua v5.3"

def addContext(s):
    return str(s).strip().replace(":", "self.prg.")

class Interpreter:
    # Turtle program should not contain variable with names "ir", "pc", "t_screen"
    ir = None
    pc = None
    t_screen = None
    trtl = None

    def __init__(self, ir):
        self.ir = ir
        self.pc = 0
        self.t_screen = turtle.getscreen()
        self.trtl = turtle.Turtle()
        self.trtl.shape("turtle")
        self.trtl.color("brown")
        self.trtl.fillcolor("green")
        self.trtl.speed(1) # TODO: Make it user friendly
        turtle.title(Release)
        turtle.hideturtle()

    def initProgramContext(self, params):
        for key,val in params.items():
            var = key.replace(":","")
            exec("setattr(self.prg,\"%s\",%s)" % (var, val))

    def handleAssignment(self, stmt,tgt):
        raise NotImplementedError('Assignments are not handled!')

    def handleCondition(self, stmt, tgt):
        raise NotImplementedError('Conditions are not handled!')

    def handleMove(self, stmt, tgt):
        raise NotImplementedError('Moves are not handled!')

    def handlePen(self, stmt, tgt):
        raise NotImplementedError('Pens are not handled!')

    def handleGotoCommand(self, stmt, tgt):
        raise NotImplementedError('Gotos are not handled!')

    def handleNoOpCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def handlePauseCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def sanityCheck(self, irInstr):
        stmt, tgt = irInstr
        # if not a condition command, rel. jump can't be anything but 1
        if not isinstance(stmt, kachuaAST.ConditionCommand):
            if tgt != 1:
                raise ValueError("Improper relative jump for non-conditional instruction", str(stmt), tgt)

    def interpret(self):
        if self.pc >= len(self.ir):
            return True # program terminated

        print("Program counter : ", self.pc)
        stmt, tgt = self.ir[self.pc]
        print(stmt, stmt.__class__.__name__, tgt)

        self.sanityCheck(self.ir[self.pc])

        if isinstance(stmt, kachuaAST.AssignmentCommand):
            ntgt = self.handleAssignment(stmt, tgt)
        elif isinstance(stmt, kachuaAST.ConditionCommand):
            ntgt = self.handleCondition(stmt, tgt)
        elif isinstance(stmt, kachuaAST.MoveCommand):
            ntgt = self.handleMove(stmt, tgt)
        elif isinstance(stmt, kachuaAST.PenCommand):
            ntgt = self.handlePen(stmt, tgt)
        elif isinstance(stmt, kachuaAST.GotoCommand):
            ntgt = self.handleGotoCommand(stmt, tgt)
        elif isinstance(stmt, kachuaAST.NoOpCommand):
            ntgt = self.handleNoOpCommand(stmt, tgt)
        else:
            raise NotImplementedError("Unknown instruction: %s, %s."%(type(stmt), stmt))

        # TODO: handle statement
        self.pc += ntgt

        # FIXME : Fuzzer returns a value pass the #ir in the coverage.
        return True if self.pc >= len(self.ir) else False # TODO: return termination status

class ProgramContext:
    pass

# TODO: move to a different file
class ConcreteInterpreter(Interpreter):
    # Ref: https://realpython.com/beginners-guide-python-turtle
    cond_eval = None # used as a temporary variable within the embedded program interpreter
    prg = None

    def __init__(self, ir):
        super().__init__(ir)
        self.prg = ProgramContext()

    def handleAssignment(self, stmt, tgt):
        print("  Assignment Statement")
        lhs = str(stmt.lvar).replace(":","")
        rhs = addContext(stmt.rexpr)
        exec("setattr(self.prg,\"%s\",%s)" % (lhs,rhs))
        return 1

    def handleCondition(self, stmt, tgt):
        print("  Branch Instruction")
        condstr = addContext(stmt)
        exec("self.cond_eval = %s" % (condstr))
        return 1 if self.cond_eval else tgt

    def handleMove(self, stmt, tgt):
        print("  MoveCommand")
        exec("self.trtl.%s(%s)" % (stmt.direction,addContext(stmt.expr)))
        return 1

    def handleNoOpCommand(self, stmt, tgt):
        print("  No-Op Command")
        return 1

    def handlePen(self, stmt, tgt):
        print("  PenCommand")
        exec("self.trtl.%s()"%(stmt.status))
        return 1

    def handleGotoCommand(self, stmt, tgt):
        print(" GotoCommand")
        xcor = addContext(stmt.xcor)
        ycor = addContext(stmt.ycor)
        exec("self.trtl.goto(%s, %s)" % (xcor, ycor))
        return 1
