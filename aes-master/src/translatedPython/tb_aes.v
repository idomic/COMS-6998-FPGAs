module tb_aes;

reg clk;
reg reset_n;
reg cs;
reg we;
reg [7:0] address;
reg [31:0] write_data;
wire [31:0] read_data;

initial begin
    $from_myhdl(
        clk,
        reset_n,
        cs,
        we,
        address,
        write_data
    );
    $to_myhdl(
        read_data
    );
end

aes dut(
    clk,
    reset_n,
    cs,
    we,
    address,
    write_data,
    read_data
);

endmodule
