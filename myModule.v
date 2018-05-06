module myModule_tb(); 
    wire out;
    reg clock;
     
    always begin
		#1 clock =!clock;
    end
     
    initial begin
		//Initialize clock
		clock = 0;
     
		//End simulation
		#10
		$finish;
    end
     
    myModule notGate(clock, out);
endmodule

module myModule(A, B);
    input wire A;
    output wire B;
    assign B = !A;
endmodule