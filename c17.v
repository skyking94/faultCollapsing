module c17 (N1,N2,N3,N6,N7,N22,N23);
input N1,N2,N3,N6,N7;
output N22,N23;
wire N10,N11,N16,N19,N3fo0,N3fo1,N11fo0,N11fo1,N16fo0,N16fo1;
NAND2X1 uut0 (.Y(N10),.A(N1),.B(N3fo0));
NAND2X1 uut1 (.Y(N11),.A(N3fo1),.B(N6));
NAND2X1 uut2 (.Y(N16),.A(N2),.B(N11fo0));
NAND2X1 uut3 (.Y(N19),.A(N11fo1),.B(N7));
NAND2X1 uut4 (.Y(N22),.A(N10),.B(N16fo0));
NAND2X1 uut5 (.Y(N23),.A(N16fo1),.B(N19));
fanout2 uut_fo2 (.A(N3),.Y1(N3fo0),.Y2(N3fo1));
fanout2 uut_fo_w0 (.A(N16),.Y1(N16fo0),.Y2(N16fo1));
fanout2 uut_fo_w2 (.A(N11),.Y1(N11fo0),.Y2(N11fo1));
endmodule
