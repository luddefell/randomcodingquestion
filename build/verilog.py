"""Verilog problems. Each has a Python reference model (source of truth for the
expected outputs) and a reference Verilog solution (used by verify.html to
cross-check the model, the Yosys flow and the simulator)."""
from common import vlog

SEQ_NOTE = "Outputs are checked just after each rising edge of `clk`."

# ============================ Combinational: easy ============================

@vlog("gates", "Basic Gates", "easy", "input a, input b, output out_and, output out_or, output out_xor, output out_nand, output out_nor, output out_xnor",
      topic="combinational", desc="""
Drive each output with the named logic function of `a` and `b`: AND, OR, XOR, NAND, NOR and XNOR.
""", solution="""
module top_module(input logic a, b, output logic out_and, out_or, out_xor, out_nand, out_nor, out_xnor);
  assign out_and = a & b;   assign out_or  = a | b;    assign out_xor  = a ^ b;
  assign out_nand = ~(a & b); assign out_nor = ~(a | b); assign out_xnor = ~(a ^ b);
endmodule""")
def gates(i):
    a, b = i["a"], i["b"]
    return dict(out_and=a & b, out_or=a | b, out_xor=a ^ b, out_nand=1 - (a & b), out_nor=1 - (a | b), out_xnor=1 - (a ^ b))


@vlog("mux2", "2-to-1 Multiplexer", "easy", "input [7:0] a, input [7:0] b, input sel, output [7:0] out", topic="combinational", desc="""
Build an 8-bit wide 2-to-1 multiplexer: `out` is `a` when `sel` is 0 and `b` when `sel` is 1.
""", solution="""
module top_module(input logic [7:0] a, b, input logic sel, output logic [7:0] out);
  assign out = sel ? b : a;
endmodule""")
def mux2(i):
    return {"out": i["b"] if i["sel"] else i["a"]}


@vlog("mux4", "4-to-1 Multiplexer", "easy", "input [3:0] a, input [3:0] b, input [3:0] c, input [3:0] d, input [1:0] sel, output [3:0] out",
      topic="combinational", desc="""
Build a 4-bit wide 4-to-1 multiplexer: `sel` = 0, 1, 2, 3 selects `a`, `b`, `c`, `d`.
""", solution="""
module top_module(input logic [3:0] a, b, c, d, input logic [1:0] sel, output logic [3:0] out);
  always_comb case (sel)
    2'd0: out = a; 2'd1: out = b; 2'd2: out = c; default: out = d;
  endcase
endmodule""")
def mux4(i):
    return {"out": [i["a"], i["b"], i["c"], i["d"]][i["sel"]]}


@vlog("full-adder", "Full Adder", "easy", "input a, input b, input cin, output sum, output cout", topic="arithmetic", desc="""
Add three 1-bit inputs. `sum` is the low bit of `a + b + cin` and `cout` is the carry out.
""", solution="""
module top_module(input logic a, b, cin, output logic sum, cout);
  assign sum = a ^ b ^ cin;
  assign cout = (a & b) | (cin & (a ^ b));
endmodule""")
def full_adder(i):
    s = i["a"] + i["b"] + i["cin"]
    return {"sum": s & 1, "cout": s >> 1}


@vlog("adder4", "4-bit Adder", "easy", "input [3:0] a, input [3:0] b, input cin, output [3:0] sum, output cout", topic="arithmetic", desc="""
Add two 4-bit unsigned numbers and a carry in. `sum` is the 4-bit result and `cout` the carry out, i.e. `{cout, sum} = a + b + cin`.
""", solution="""
module top_module(input logic [3:0] a, b, input logic cin, output logic [3:0] sum, output logic cout);
  assign {cout, sum} = a + b + cin;
endmodule""")
def adder4(i):
    s = i["a"] + i["b"] + i["cin"]
    return {"sum": s & 15, "cout": s >> 4}


@vlog("reverse-bits", "Reverse Bit Order", "easy", "input [7:0] in, output [7:0] out", topic="vectors", desc="""
Reverse the bit order of `in`: `out[0] = in[7]`, `out[1] = in[6]`, …, `out[7] = in[0]`.
""", solution="""
module top_module(input logic [7:0] in, output logic [7:0] out);
  always_comb for (int k = 0; k < 8; k++) out[k] = in[7 - k];
endmodule""")
def reverse_bits(i):
    return {"out": int(format(i["in"], "08b")[::-1], 2)}


@vlog("popcount", "Population Count", "easy", "input [7:0] in, output [3:0] count", topic="vectors", desc="""
Output the number of `1` bits in the 8-bit input.
""", solution="""
module top_module(input logic [7:0] in, output logic [3:0] count);
  always_comb begin
    count = 0;
    for (int k = 0; k < 8; k++) count = count + in[k];
  end
endmodule""")
def popcount(i):
    return {"count": bin(i["in"]).count("1")}


@vlog("parity", "Even Parity Bit", "easy", "input [7:0] in, output parity", topic="vectors", desc="""
Compute the even parity bit for `in`: `parity` is chosen so that the 9 bits `{parity, in}` contain an even number of `1`s.
""", solution="""
module top_module(input logic [7:0] in, output logic parity);
  assign parity = ^in;
endmodule""")
def parity(i):
    return {"parity": bin(i["in"]).count("1") & 1}


@vlog("decoder3to8", "3-to-8 Decoder", "easy", "input en, input [2:0] in, output [7:0] out", topic="combinational", desc="""
When `en` is 1, set exactly one bit of `out` high: bit number `in`. When `en` is 0, `out` is all zeros.
""", solution="""
module top_module(input logic en, input logic [2:0] in, output logic [7:0] out);
  assign out = en ? 8'b1 << in : 8'b0;
endmodule""")
def decoder3to8(i):
    return {"out": (1 << i["in"]) if i["en"] else 0}


@vlog("comparator", "4-bit Comparator", "easy", "input [3:0] a, input [3:0] b, output eq, output gt, output lt", topic="arithmetic", desc="""
Compare two unsigned 4-bit numbers: `eq` is 1 when `a == b`, `gt` when `a > b`, and `lt` when `a < b`.
""", solution="""
module top_module(input logic [3:0] a, b, output logic eq, gt, lt);
  assign eq = a == b; assign gt = a > b; assign lt = a < b;
endmodule""")
def comparator(i):
    return {"eq": int(i["a"] == i["b"]), "gt": int(i["a"] > i["b"]), "lt": int(i["a"] < i["b"])}


@vlog("binary-to-gray", "Binary to Gray Code", "easy", "input [7:0] bin, output [7:0] gray", topic="vectors", desc="""
Convert an 8-bit binary number to Gray code, where consecutive values differ in exactly one bit. Each Gray bit is the XOR of a binary bit and the bit above it; the top bit stays the same.
""", solution="""
module top_module(input logic [7:0] bin, output logic [7:0] gray);
  assign gray = bin ^ (bin >> 1);
endmodule""")
def bin2gray(i):
    return {"gray": i["bin"] ^ (i["bin"] >> 1)}


@vlog("sign-extend", "Sign Extension", "easy", "input [7:0] in, output [15:0] out", topic="vectors", desc="""
Sign-extend the 8-bit two's complement number `in` to 16 bits: copy `in[7]` into the upper 8 bits.
""", solution="""
module top_module(input logic [7:0] in, output logic [15:0] out);
  assign out = {{8{in[7]}}, in};
endmodule""")
def sign_extend(i):
    return {"out": i["in"] | (0xFF00 if i["in"] & 0x80 else 0)}


@vlog("byte-swap", "Byte Swap", "easy", "input [31:0] in, output [31:0] out", topic="vectors", desc="""
Reverse the byte order of a 32-bit word (convert between little- and big-endian): byte 0 swaps with byte 3, byte 1 with byte 2. Bits inside each byte stay in order.
""", solution="""
module top_module(input logic [31:0] in, output logic [31:0] out);
  assign out = {in[7:0], in[15:8], in[23:16], in[31:24]};
endmodule""")
def byte_swap(i):
    return {"out": int.from_bytes(i["in"].to_bytes(4, "little"), "big")}


@vlog("min-of-four", "Minimum of Four", "easy", "input [7:0] a, input [7:0] b, input [7:0] c, input [7:0] d, output [7:0] min", topic="arithmetic", desc="""
Output the smallest of four unsigned 8-bit numbers.
""", solution="""
module top_module(input logic [7:0] a, b, c, d, output logic [7:0] min);
  logic [7:0] m1, m2;
  assign m1 = a < b ? a : b;
  assign m2 = c < d ? c : d;
  assign min = m1 < m2 ? m1 : m2;
endmodule""")
def min_of_four(i):
    return {"min": min(i["a"], i["b"], i["c"], i["d"])}


_SEG = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71]


@vlog("seven-segment", "Seven-Segment Decoder", "easy", "input [3:0] hex, output [6:0] seg", topic="combinational", desc="""
Drive an active-high seven-segment display showing the hex digit `hex` (0-9, A, b, C, d, E, F). `seg[0]` is segment a (top), then b, c, d, e, f, and `seg[6]` is g (middle).

The values of `seg` for 0…F are: `3F 06 5B 4F 66 6D 7D 07 7F 6F 77 7C 39 5E 79 71` (hex).
""", solution="""
module top_module(input logic [3:0] hex, output logic [6:0] seg);
  always_comb case (hex)
    4'h0: seg = 7'h3F; 4'h1: seg = 7'h06; 4'h2: seg = 7'h5B; 4'h3: seg = 7'h4F;
    4'h4: seg = 7'h66; 4'h5: seg = 7'h6D; 4'h6: seg = 7'h7D; 4'h7: seg = 7'h07;
    4'h8: seg = 7'h7F; 4'h9: seg = 7'h6F; 4'hA: seg = 7'h77; 4'hB: seg = 7'h7C;
    4'hC: seg = 7'h39; 4'hD: seg = 7'h5E; 4'hE: seg = 7'h79; default: seg = 7'h71;
  endcase
endmodule""")
def seven_segment(i):
    return {"seg": _SEG[i["hex"]]}


# ============================ Combinational: medium ============================

@vlog("gray-to-binary", "Gray Code to Binary", "medium", "input [7:0] gray, output [7:0] bin", topic="vectors", desc="""
Convert an 8-bit Gray code value back to binary. The top bit is unchanged; each lower binary bit is the XOR of the Gray bit and the binary bit above it.
""", solution="""
module top_module(input logic [7:0] gray, output logic [7:0] bin);
  always_comb begin
    bin[7] = gray[7];
    for (int k = 6; k >= 0; k--) bin[k] = bin[k + 1] ^ gray[k];
  end
endmodule""")
def gray2bin(i):
    g, b = i["gray"], 0
    while g:
        b ^= g
        g >>= 1
    return {"bin": b}


@vlog("priority-encoder", "Priority Encoder", "medium", "input [7:0] in, output [2:0] pos, output valid", topic="combinational", desc="""
Output in `pos` the index of the **highest** set bit of `in`, and set `valid` to 1. If `in` is zero, `valid` is 0 and `pos` is 0.
""", solution="""
module top_module(input logic [7:0] in, output logic [2:0] pos, output logic valid);
  always_comb begin
    pos = 0;
    for (int k = 0; k < 8; k++) if (in[k]) pos = k;
  end
  assign valid = |in;
endmodule""")
def priority_encoder(i):
    return {"pos": max(i["in"].bit_length() - 1, 0), "valid": int(i["in"] != 0)}


@vlog("alu", "8-bit ALU", "medium", "input [7:0] a, input [7:0] b, input [2:0] op, output [7:0] y, output zero", topic="arithmetic", desc="""
Build an ALU. `zero` is 1 when `y` is 0. Results wrap to 8 bits.

- `op = 0`: `a + b`
- `op = 1`: `a - b`
- `op = 2`: `a & b`
- `op = 3`: `a | b`
- `op = 4`: `a ^ b`
- `op = 5`: `a` shifted left by `b[2:0]`
- `op = 6`: `a` shifted right (logical) by `b[2:0]`
- `op = 7`: `1` if `a < b` (unsigned), else `0`
""", solution="""
module top_module(input logic [7:0] a, b, input logic [2:0] op, output logic [7:0] y, output logic zero);
  always_comb case (op)
    3'd0: y = a + b;       3'd1: y = a - b;
    3'd2: y = a & b;       3'd3: y = a | b;
    3'd4: y = a ^ b;       3'd5: y = a << b[2:0];
    3'd6: y = a >> b[2:0]; default: y = {7'b0, a < b};
  endcase
  assign zero = y == 0;
endmodule""")
def alu(i):
    a, b, op = i["a"], i["b"], i["op"]
    y = [a + b, a - b, a & b, a | b, a ^ b, a << (b & 7), a >> (b & 7), int(a < b)][op] & 0xFF
    return {"y": y, "zero": int(y == 0)}


@vlog("rotate", "Barrel Rotator", "medium", "input [7:0] in, input [2:0] amt, output [7:0] out", topic="vectors", desc="""
Rotate `in` **left** by `amt` positions: bits shifted out at the top come back in at the bottom.
""", solution="""
module top_module(input logic [7:0] in, input logic [2:0] amt, output logic [7:0] out);
  logic [15:0] doubled;
  assign doubled = {in, in} << amt;
  assign out = doubled[15:8];
endmodule""")
def rotate(i):
    x, n = i["in"], i["amt"]
    return {"out": ((x << n) | (x >> (8 - n))) & 0xFF}


@vlog("leading-zeros", "Count Leading Zeros", "medium", "input [15:0] in, output [4:0] count", topic="vectors",
      vectors=lambda rng: [{"in": 0}, {"in": 0xFFFF}] + [{"in": 1 << k} for k in range(16)] + [{"in": rng.getrandbits(16) >> rng.randrange(16)} for _ in range(100)],
      desc="""
Output the number of `0` bits above the highest `1` bit of the 16-bit input. If `in` is zero, `count` is 16.
""", solution="""
module top_module(input logic [15:0] in, output logic [4:0] count);
  always_comb begin
    count = 16;
    for (int k = 0; k < 16; k++) if (in[k]) count = 15 - k;
  end
endmodule""")
def leading_zeros(i):
    return {"count": 16 - i["in"].bit_length()}


# ============================ Sequential: easy ============================

@vlog("dff-reset", "Register with Synchronous Reset", "easy", "input clk, input reset, input [7:0] d, output [7:0] q", seq=True, topic="sequential", desc=f"""
Build an 8-bit register. On each rising edge of `clk`, `q` takes the value of `d`, unless `reset` is 1, in which case `q` becomes 0. The reset is synchronous: it only acts on a clock edge.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, input logic [7:0] d, output logic [7:0] q);
  always_ff @(posedge clk) q <= reset ? 8'd0 : d;
endmodule""")
class DffReset:
    q = 0
    def step(self, i):
        self.q = 0 if i["reset"] else i["d"]
        return {"q": self.q}


@vlog("dff-enable", "Register with Enable", "easy", "input clk, input reset, input en, input [7:0] d, output [7:0] q", seq=True, topic="sequential", desc=f"""
An 8-bit register with synchronous reset and enable. On a rising edge: if `reset`, `q` becomes 0; otherwise if `en`, `q` loads `d`; otherwise `q` keeps its value.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, en, input logic [7:0] d, output logic [7:0] q);
  always_ff @(posedge clk)
    if (reset) q <= 0;
    else if (en) q <= d;
endmodule""")
class DffEnable:
    q = 0
    def step(self, i):
        if i["reset"]:
            self.q = 0
        elif i["en"]:
            self.q = i["d"]
        return {"q": self.q}


@vlog("counter", "4-bit Counter", "easy", "input clk, input reset, output [3:0] q", seq=True, topic="counters", desc=f"""
Count up by one on every rising clock edge, from 0 to 15 and then wrap back to 0. A synchronous `reset` sets the count to 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, output logic [3:0] q);
  always_ff @(posedge clk) q <= reset ? 4'd0 : q + 4'd1;
endmodule""")
class Counter4:
    q = 0
    def step(self, i):
        self.q = 0 if i["reset"] else (self.q + 1) & 15
        return {"q": self.q}


@vlog("decade-counter", "Decade Counter", "easy", "input clk, input reset, input en, output [3:0] q", seq=True, topic="counters", desc=f"""
Count from 0 to 9 and wrap back to 0, advancing only on edges where `en` is 1. A synchronous `reset` sets the count to 0 (reset wins over `en`).

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, en, output logic [3:0] q);
  always_ff @(posedge clk)
    if (reset) q <= 0;
    else if (en) q <= (q == 9) ? 4'd0 : q + 4'd1;
endmodule""")
class Decade:
    q = 0
    def step(self, i):
        if i["reset"]:
            self.q = 0
        elif i["en"]:
            self.q = (self.q + 1) % 10
        return {"q": self.q}


@vlog("shift-register", "Shift Register", "easy", "input clk, input reset, input in, output [3:0] q", seq=True, topic="sequential", desc=f"""
Build a 4-bit shift register. On each rising edge, shift `q` left by one and put `in` into `q[0]`, so `q[3]` holds the input from 3 edges ago. A synchronous `reset` clears it.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, in, output logic [3:0] q);
  always_ff @(posedge clk) q <= reset ? 4'd0 : {q[2:0], in};
endmodule""")
class Shift4:
    q = 0
    def step(self, i):
        self.q = 0 if i["reset"] else ((self.q << 1) | i["in"]) & 15
        return {"q": self.q}


@vlog("t-flip-flop", "T Flip-Flop", "easy", "input clk, input reset, input t, output q", seq=True, topic="sequential", desc=f"""
A toggle flip-flop: on a rising edge, `q` flips if `t` is 1 and holds if `t` is 0. A synchronous `reset` sets `q` to 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, t, output logic q);
  always_ff @(posedge clk) q <= reset ? 1'b0 : q ^ t;
endmodule""")
class TFF:
    q = 0
    def step(self, i):
        self.q = 0 if i["reset"] else self.q ^ i["t"]
        return {"q": self.q}


@vlog("johnson-counter", "Johnson Counter", "easy", "input clk, input reset, output [3:0] q", seq=True, topic="counters", desc=f"""
A 4-bit Johnson (twisted ring) counter: on each rising edge, shift `q` left by one and feed the **inverse** of `q[3]` into `q[0]`. It cycles 0000 → 0001 → 0011 → 0111 → 1111 → 1110 → 1100 → 1000 → 0000. A synchronous `reset` sets `q` to 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, output logic [3:0] q);
  always_ff @(posedge clk) q <= reset ? 4'd0 : {q[2:0], ~q[3]};
endmodule""")
class Johnson:
    q = 0
    def step(self, i):
        self.q = 0 if i["reset"] else ((self.q << 1) & 15) | (1 - (self.q >> 3))
        return {"q": self.q}


@vlog("running-max", "Running Maximum", "easy", "input clk, input reset, input [7:0] in, output [7:0] max", seq=True, topic="sequential", desc=f"""
Track the largest value of `in` seen since reset. On each rising edge, `max` becomes the larger of `max` and `in`. A synchronous `reset` sets `max` to 0 (the input on a reset edge is ignored).

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, input logic [7:0] in, output logic [7:0] max);
  always_ff @(posedge clk)
    if (reset) max <= 0;
    else if (in > max) max <= in;
endmodule""")
class RunningMax:
    m = 0
    def step(self, i):
        self.m = 0 if i["reset"] else max(self.m, i["in"])
        return {"max": self.m}


@vlog("edge-detector", "Rising Edge Detector", "easy", "input clk, input reset, input in, output pulse", seq=True, topic="sequential", desc=f"""
Detect when `in` changes from 0 to 1 between two consecutive clock edges. `pulse` is a **registered** output: after the edge where `in` is sampled as 1 while it was 0 at the previous edge, `pulse` is 1 for one cycle.

A synchronous `reset` sets `pulse` to 0 and treats the previous input as 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, in, output logic pulse);
  logic prev;
  always_ff @(posedge clk)
    if (reset) begin prev <= 0; pulse <= 0; end
    else begin prev <= in; pulse <= in & ~prev; end
endmodule""")
class EdgeDetect:
    prev = 0
    def step(self, i):
        if i["reset"]:
            self.prev, out = 0, 0
        else:
            out = i["in"] & (1 - self.prev)
            self.prev = i["in"]
        return {"pulse": out}


# ============================ Sequential: medium ============================

@vlog("lfsr", "8-bit LFSR", "medium", "input clk, input reset, output [7:0] q", seq=True, cycles=60, topic="sequential", desc=f"""
Build an 8-bit Fibonacci linear-feedback shift register with polynomial x⁸ + x⁶ + x⁵ + x⁴ + 1. On each rising edge, shift `q` left by one and put `q[7] ^ q[5] ^ q[4] ^ q[3]` into `q[0]`.

A synchronous `reset` sets `q` to `8'h01` (all zeros would get stuck).

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, output logic [7:0] q);
  always_ff @(posedge clk) q <= reset ? 8'h01 : {q[6:0], q[7] ^ q[5] ^ q[4] ^ q[3]};
endmodule""")
class LFSR:
    q = 1
    def step(self, i):
        if i["reset"]:
            self.q = 1
        else:
            q = self.q
            fb = ((q >> 7) ^ (q >> 5) ^ (q >> 4) ^ (q >> 3)) & 1
            self.q = ((q << 1) | fb) & 0xFF
        return {"q": self.q}


def _seq_gen(rng, s):
    lead = [1, 0, 1, 1, 0, 1, 1, 0, 0] if s == 0 else []  # show an overlapping match early
    bits = lead + [rng.getrandbits(1) for _ in range(58 - len(lead))]
    resets = [1, 1] + [int(rng.random() < 0.04) if c > 12 else 0 for c in range(2, 60)]
    return [{"reset": r, "in": b} for r, b in zip(resets, [0, 0] + bits)]


@vlog("sequence-detector", "Sequence Detector (1011)", "medium", "input clk, input reset, input in, output detected", seq=True, gen=_seq_gen, topic="fsm", desc=f"""
`in` delivers one bit per clock edge. Set `detected` to 1 right after the edge on which the last four bits sampled were `1, 0, 1, 1` (oldest first). Overlapping matches count: `1011011` matches twice.

A synchronous `reset` forgets all previous bits (a Moore FSM works well here).

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, in, output logic detected);
  logic [3:0] hist;
  always_ff @(posedge clk) hist <= reset ? 4'd0 : {hist[2:0], in};
  assign detected = hist == 4'b1011;
endmodule""")
class Seq1011:
    h = 0
    def step(self, i):
        self.h = 0 if i["reset"] else ((self.h << 1) | i["in"]) & 15
        return {"detected": int(self.h == 0b1011)}


@vlog("gray-counter", "Gray Code Counter", "medium", "input clk, input reset, output [3:0] q", seq=True, topic="counters", desc=f"""
Count through the 16 values of 4-bit Gray code (0000, 0001, 0011, 0010, 0110, …), advancing one step per rising edge and wrapping around, so only one bit of `q` changes per clock. A synchronous `reset` sets `q` to 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, output logic [3:0] q);
  logic [3:0] bin;
  always_ff @(posedge clk) bin <= reset ? 4'd0 : bin + 4'd1;
  assign q = bin ^ (bin >> 1);
endmodule""")
class GrayCounter:
    n = 0
    def step(self, i):
        self.n = 0 if i["reset"] else (self.n + 1) & 15
        return {"q": self.n ^ (self.n >> 1)}


@vlog("bcd-counter", "Two-Digit BCD Counter", "medium", "input clk, input reset, input en, output [3:0] tens, output [3:0] ones", seq=True, cycles=150, seqs=2,
      bias={"en": 0.9}, topic="counters", desc=f"""
Count from 00 to 99 in BCD (each digit is 0-9 in its own 4 bits), then wrap to 00. The count advances on edges where `en` is 1. A synchronous `reset` sets both digits to 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, en, output logic [3:0] tens, ones);
  always_ff @(posedge clk)
    if (reset) begin tens <= 0; ones <= 0; end
    else if (en) begin
      if (ones == 9) begin
        ones <= 0;
        tens <= (tens == 9) ? 4'd0 : tens + 4'd1;
      end else ones <= ones + 4'd1;
    end
endmodule""")
class BCD:
    n = 0
    def step(self, i):
        if i["reset"]:
            self.n = 0
        elif i["en"]:
            self.n = (self.n + 1) % 100
        return {"tens": self.n // 10, "ones": self.n % 10}


@vlog("up-down-counter", "Loadable Up/Down Counter", "medium", "input clk, input reset, input load, input [7:0] d, input en, input up, output [7:0] q", seq=True,
      bias={"load": 0.15, "en": 0.8}, topic="counters", desc=f"""
An 8-bit counter. On each rising edge, in priority order:

- `reset`: `q` becomes 0
- `load`: `q` becomes `d`
- `en`: `q` counts up by 1 if `up` is 1, otherwise down by 1 (wrapping at 0 and 255)
- otherwise `q` holds.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, load, input logic [7:0] d, input logic en, up, output logic [7:0] q);
  always_ff @(posedge clk)
    if (reset) q <= 0;
    else if (load) q <= d;
    else if (en) q <= up ? q + 8'd1 : q - 8'd1;
endmodule""")
class UpDown:
    q = 0
    def step(self, i):
        if i["reset"]:
            self.q = 0
        elif i["load"]:
            self.q = i["d"]
        elif i["en"]:
            self.q = (self.q + (1 if i["up"] else -1)) & 0xFF
        return {"q": self.q}


@vlog("saturating-counter", "2-bit Branch Predictor", "medium", "input clk, input reset, input valid, input taken, output [1:0] state, output predict", seq=True,
      topic="fsm", desc=f"""
Build the classic 2-bit saturating counter used in branch predictors. `state` ranges from 0 (strongly not taken) to 3 (strongly taken).

On a rising edge with `valid` = 1: if `taken`, increment `state` (saturating at 3), otherwise decrement it (saturating at 0). When `valid` is 0, `state` holds. `predict` is 1 when `state` is 2 or 3. A synchronous `reset` sets `state` to 1 (weakly not taken).

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, valid, taken, output logic [1:0] state, output logic predict);
  always_ff @(posedge clk)
    if (reset) state <= 2'd1;
    else if (valid) begin
      if (taken && state != 3) state <= state + 2'd1;
      else if (!taken && state != 0) state <= state - 2'd1;
    end
  assign predict = state[1];
endmodule""")
class SatCounter:
    s = 1
    def step(self, i):
        if i["reset"]:
            self.s = 1
        elif i["valid"]:
            self.s = min(self.s + 1, 3) if i["taken"] else max(self.s - 1, 0)
        return {"state": self.s, "predict": self.s >> 1}


@vlog("tick-generator", "Tick Generator", "medium", "input clk, input reset, output tick", seq=True, cycles=50, topic="counters", desc=f"""
Generate a one-cycle `tick` every 5 clock cycles. Use a counter that goes 0, 1, 2, 3, 4, 0, … advancing on every rising edge; `tick` is 1 while the counter is 4. A synchronous `reset` sets the counter to 0.

So after reset is released, `tick` is high after the 4th edge, the 9th, the 14th, and so on.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, output logic tick);
  logic [2:0] cnt;
  always_ff @(posedge clk) cnt <= (reset || cnt == 4) ? 3'd0 : cnt + 3'd1;
  assign tick = cnt == 4;
endmodule""")
class Tick:
    c = 0
    def step(self, i):
        self.c = 0 if i["reset"] else (self.c + 1) % 5
        return {"tick": int(self.c == 4)}


@vlog("pwm", "PWM Generator", "medium", "input clk, input reset, input [3:0] duty, output pwm", seq=True, cycles=80, topic="counters", desc=f"""
Build a pulse-width modulator. A free-running 4-bit counter increments on every rising edge (wrapping 15 → 0); a synchronous `reset` sets it to 0. `pwm` is 1 whenever the counter is less than `duty`, so `duty` = 4 gives a signal that is high 4 out of every 16 cycles.

`pwm` is combinational from the counter and the current `duty`.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, input logic [3:0] duty, output logic pwm);
  logic [3:0] cnt;
  always_ff @(posedge clk) cnt <= reset ? 4'd0 : cnt + 4'd1;
  assign pwm = cnt < duty;
endmodule""")
class PWM:
    c = 0
    def step(self, i):
        self.c = 0 if i["reset"] else (self.c + 1) & 15
        return {"pwm": int(self.c < i["duty"])}


@vlog("moving-sum", "Moving Sum", "medium", "input clk, input reset, input [7:0] in, output [9:0] sum", seq=True, topic="sequential", desc=f"""
Output the sum of the last four values of `in` sampled on rising edges (including the one just sampled). A synchronous `reset` clears the history, so right after reset the older samples count as 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, input logic [7:0] in, output logic [9:0] sum);
  logic [7:0] h0, h1, h2, h3;
  always_ff @(posedge clk)
    if (reset) {h0, h1, h2, h3} <= 0;
    else begin h0 <= in; h1 <= h0; h2 <= h1; h3 <= h2; end
  assign sum = h0 + h1 + h2 + h3;
endmodule""")
class MovingSum:
    def __init__(self):
        self.h = [0, 0, 0, 0]
    def step(self, i):
        self.h = [0, 0, 0, 0] if i["reset"] else [i["in"]] + self.h[:3]
        return {"sum": sum(self.h)}


@vlog("sync-ram", "Synchronous RAM", "medium", "input clk, input we, input [3:0] addr, input [7:0] wdata, output [7:0] rdata", seq=True, cycles=80,
      bias={"we": 0.5}, topic="memory", desc=f"""
Build a 16 x 8-bit RAM with a synchronous read port. On each rising edge:

- if `we` is 1, write `wdata` to address `addr`
- `rdata` is loaded with the value stored at `addr` **before** this edge's write (read-first behavior).

The memory starts out all zeros in this simulator. There is no reset.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, we, input logic [3:0] addr, input logic [7:0] wdata, output logic [7:0] rdata);
  logic [7:0] mem [0:15];
  always_ff @(posedge clk) begin
    if (we) mem[addr] <= wdata;
    rdata <= mem[addr];
  end
endmodule""")
class SyncRAM:
    def __init__(self):
        self.mem, self.r = [0] * 16, 0
    def step(self, i):
        self.r = self.mem[i["addr"]]
        if i["we"]:
            self.mem[i["addr"]] = i["wdata"]
        return {"rdata": self.r}


# ============================ Sequential: hard ============================

@vlog("round-robin-arbiter", "Round-Robin Arbiter", "hard", "input clk, input reset, input [3:0] req, output [3:0] grant", seq=True, cycles=60, topic="fsm", desc=f"""
Four clients request a shared resource on `req`. On each rising edge, the arbiter registers a one-hot `grant` for one requesting client, or `grant = 0` if nobody requests.

Priority rotates: search starts at the client just after the one granted most recently and wraps around (…, 3, 0, 1, …). After a synchronous `reset`, `grant` is 0 and the search starts at client 0.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, input logic [3:0] req, output logic [3:0] grant);
  logic [1:0] last, idx, pick;
  logic found;
  always_comb begin
    found = 0; pick = 0;
    for (int k = 1; k <= 4; k++) begin
      idx = last + k[1:0];
      if (!found && req[idx]) begin found = 1; pick = idx; end
    end
  end
  always_ff @(posedge clk)
    if (reset) begin grant <= 0; last <= 2'd3; end
    else if (found) begin grant <= 4'b1 << pick; last <= pick; end
    else grant <= 0;
endmodule""")
class Arbiter:
    last, g = 3, 0
    def step(self, i):
        if i["reset"]:
            self.last, self.g = 3, 0
        else:
            self.g = 0
            for k in range(1, 5):
                idx = (self.last + k) % 4
                if i["req"] >> idx & 1:
                    self.g, self.last = 1 << idx, idx
                    break
        return {"grant": self.g}


def _fifo_gen(rng, s):
    cycles, p_push = [], [0.7, 0.3, 0.5][s % 3]
    for c in range(80):
        cycles.append({"reset": 1 if c < 2 else int(rng.random() < 0.02), "push": int(rng.random() < p_push),
                       "pop": int(rng.random() < 1 - p_push), "din": rng.getrandbits(8)})
    return cycles


@vlog("fifo", "FIFO Queue", "hard", "input clk, input reset, input push, input pop, input [7:0] din, output [7:0] dout, output empty, output full",
      seq=True, gen=_fifo_gen, topic="memory", desc=f"""
Build a 4-entry, 8-bit first-in first-out queue. On each rising edge, based on the state **before** the edge:

- if `pop` is 1 and the FIFO is not empty, remove the oldest entry
- if `push` is 1 and the FIFO is not full, append `din`
- both can happen on the same edge; a push to a full FIFO or a pop from an empty one is ignored.

`empty` and `full` reflect the current count. `dout` always shows the oldest entry (show-ahead); its value doesn't matter while the FIFO is empty. A synchronous `reset` empties the FIFO.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, push, pop, input logic [7:0] din,
                  output logic [7:0] dout, output logic empty, full);
  logic [7:0] mem [0:3];
  logic [1:0] rd, wr;
  logic [2:0] count;
  logic do_push, do_pop;
  assign empty = count == 0;
  assign full = count == 4;
  assign do_pop = pop && !empty;
  assign do_push = push && !full;
  assign dout = mem[rd];
  always_ff @(posedge clk)
    if (reset) begin rd <= 0; wr <= 0; count <= 0; end
    else begin
      if (do_push) begin mem[wr] <= din; wr <= wr + 2'd1; end
      if (do_pop) rd <= rd + 2'd1;
      count <= count + do_push - do_pop;
    end
endmodule""")
class FIFO:
    def __init__(self):
        self.q = []
    def step(self, i):
        if i["reset"]:
            self.q = []
        else:
            do_pop = i["pop"] and len(self.q) > 0
            do_push = i["push"] and len(self.q) < 4
            if do_pop:
                self.q.pop(0)
            if do_push:
                self.q.append(i["din"])
        return {"dout": self.q[0] if self.q else None, "empty": int(not self.q), "full": int(len(self.q) == 4)}


def _uart_gen(rng, s):
    return [{"reset": 1 if c < 2 else 0, "start": int(rng.random() < 0.25), "data": rng.getrandbits(8)} for c in range(70)]


@vlog("uart-tx", "UART Transmitter", "hard", "input clk, input reset, input start, input [7:0] data, output tx, output busy",
      seq=True, gen=_uart_gen, topic="fsm", desc=f"""
Build a UART transmitter that sends one bit per clock cycle. While idle, `tx` is 1 and `busy` is 0.

On a rising edge where the transmitter is idle and `start` is 1, it captures `data` and begins a 10-bit frame: a start bit (`0`), the 8 data bits **LSB first**, then a stop bit (`1`). Each bit appears on `tx` for one cycle, beginning right after that edge. `busy` is 1 for all 10 bits. `start` is ignored while busy; after the stop bit the transmitter is idle again and can accept a new `start` on the next edge.

A synchronous `reset` returns it to idle.

{SEQ_NOTE}
""", solution="""
module top_module(input logic clk, reset, start, input logic [7:0] data, output logic tx, busy);
  logic [3:0] idx;   // 0 = start bit, 1..8 = data, 9 = stop bit
  logic [7:0] shreg;
  always_ff @(posedge clk)
    if (reset) busy <= 0;
    else if (!busy) begin
      if (start) begin busy <= 1; idx <= 0; shreg <= data; end
    end else if (idx == 9) busy <= 0;
    else idx <= idx + 4'd1;
  always_comb
    if (!busy) tx = 1;
    else if (idx == 0) tx = 0;
    else if (idx == 9) tx = 1;
    else tx = shreg[idx - 1];
endmodule""")
class UartTx:
    idx, data = None, 0
    def step(self, i):
        if i["reset"]:
            self.idx = None
        elif self.idx is None:
            if i["start"]:
                self.idx, self.data = 0, i["data"]
        elif self.idx == 9:
            self.idx = None
        else:
            self.idx += 1
        if self.idx is None:
            return {"tx": 1, "busy": 0}
        tx = 0 if self.idx == 0 else 1 if self.idx == 9 else (self.data >> (self.idx - 1)) & 1
        return {"tx": tx, "busy": 1}
