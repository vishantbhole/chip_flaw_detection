module counter(input clk, input reset, output reg [3:0] out);
  always @(posedge clk or posedge reset)
    if (reset)
      out <= 0;
    else
      out <= out + 1;
endmodule