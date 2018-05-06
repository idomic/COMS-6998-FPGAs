from myhdl import *

def aes_sbox(sboxw, new_sboxw):


  # //----------------------------------------------------------------
  # // The sbox array.
  # //----------------------------------------------------------------
  sbox = [Signal(intbv()[8:]) for n in range(256)]  # wire [7 : 0] sbox [0 : 255];


  # //----------------------------------------------------------------
  # // Four parallel muxes.
  # //----------------------------------------------------------------

  new_sboxw.next[31:24] = sbox[sboxw[31:24]]  # assign new_sboxw[31 : 24] = sbox[sboxw[31 : 24]];
  new_sboxw.next[23:16] = sbox[sboxw[23:16]]  # assign new_sboxw[23 : 16] = sbox[sboxw[23 : 16]];
  new_sboxw.next[15:8] = sbox[sboxw[15:8]]  # assign new_sboxw[15 : 08] = sbox[sboxw[15 : 08]];
  new_sboxw.next[7:0] = sbox[sboxw[7:0]]  # assign new_sboxw[07 : 00] = sbox[sboxw[07 : 00]];
  

  # //----------------------------------------------------------------
  # // Creating the sbox array contents.
  # //----------------------------------------------------------------
  sbox[0x00000000] = Signal(intbv (0x00000063))
  sbox[0x00000001] = Signal(intbv (0x0000007c))
  sbox[0x00000002] = Signal(intbv (0x00000077))
  sbox[0x00000003] = Signal(intbv (0x0000007b))
  sbox[0x00000004] = Signal(intbv (0x000000f2))
  sbox[0x00000005] = Signal(intbv (0x0000006b))
  sbox[0x00000006] = Signal(intbv (0x0000006f))
  sbox[0x00000007] = Signal(intbv (0x000000c5))
  sbox[0x00000008] = Signal(intbv (0x00000030))
  sbox[0x00000009] = Signal(intbv (0x00000001))
  sbox[0x0000000a] = Signal(intbv (0x00000067))
  sbox[0x0000000b] = Signal(intbv (0x0000002b))
  sbox[0x0000000c] = Signal(intbv (0x000000fe))
  sbox[0x0000000d] = Signal(intbv (0x000000d7))
  sbox[0x0000000e] = Signal(intbv (0x000000ab))
  sbox[0x0000000f] = Signal(intbv (0x00000076))
  sbox[0x00000010] = Signal(intbv (0x000000ca))
  sbox[0x00000011] = Signal(intbv (0x00000082))
  sbox[0x00000012] = Signal(intbv (0x000000c9))
  sbox[0x00000013] = Signal(intbv (0x0000007d))
  sbox[0x00000014] = Signal(intbv (0x000000fa))
  sbox[0x00000015] = Signal(intbv (0x00000059))
  sbox[0x00000016] = Signal(intbv (0x00000047))
  sbox[0x00000017] = Signal(intbv (0x000000f0))
  sbox[0x00000018] = Signal(intbv (0x000000ad))
  sbox[0x00000019] = Signal(intbv (0x000000d4))
  sbox[0x0000001a] = Signal(intbv (0x000000a2))
  sbox[0x0000001b] = Signal(intbv (0x000000af))
  sbox[0x0000001c] = Signal(intbv (0x0000009c))
  sbox[0x0000001d] = Signal(intbv (0x000000a4))
  sbox[0x0000001e] = Signal(intbv (0x00000072))
  sbox[0x0000001f] = Signal(intbv (0x000000c0))
  sbox[0x00000020] = Signal(intbv (0x000000b7))
  sbox[0x00000021] = Signal(intbv (0x000000fd))
  sbox[0x00000022] = Signal(intbv (0x00000093))
  sbox[0x00000023] = Signal(intbv (0x00000026))
  sbox[0x00000024] = Signal(intbv (0x00000036))
  sbox[0x00000025] = Signal(intbv (0x0000003f))
  sbox[0x00000026] = Signal(intbv (0x000000f7))
  sbox[0x00000027] = Signal(intbv (0x000000cc))
  sbox[0x00000028] = Signal(intbv (0x00000034))
  sbox[0x00000029] = Signal(intbv (0x000000a5))
  sbox[0x0000002a] = Signal(intbv (0x000000e5))
  sbox[0x0000002b] = Signal(intbv (0x000000f1))
  sbox[0x0000002c] = Signal(intbv (0x00000071))
  sbox[0x0000002d] = Signal(intbv (0x000000d8))
  sbox[0x0000002e] = Signal(intbv (0x00000031))
  sbox[0x0000002f] = Signal(intbv (0x00000015))
  sbox[0x00000030] = Signal(intbv (0x00000004))
  sbox[0x00000031] = Signal(intbv (0x000000c7))
  sbox[0x00000032] = Signal(intbv (0x00000023))
  sbox[0x00000033] = Signal(intbv (0x000000c3))
  sbox[0x00000034] = Signal(intbv (0x00000018))
  sbox[0x00000035] = Signal(intbv (0x00000096))
  sbox[0x00000036] = Signal(intbv (0x00000005))
  sbox[0x00000037] = Signal(intbv (0x0000009a))
  sbox[0x00000038] = Signal(intbv (0x00000007))
  sbox[0x00000039] = Signal(intbv (0x00000012))
  sbox[0x0000003a] = Signal(intbv (0x00000080))
  sbox[0x0000003b] = Signal(intbv (0x000000e2))
  sbox[0x0000003c] = Signal(intbv (0x000000eb))
  sbox[0x0000003d] = Signal(intbv (0x00000027))
  sbox[0x0000003e] = Signal(intbv (0x000000b2))
  sbox[0x0000003f] = Signal(intbv (0x00000075))
  sbox[0x00000040] = Signal(intbv (0x00000009))
  sbox[0x00000041] = Signal(intbv (0x00000083))
  sbox[0x00000042] = Signal(intbv (0x0000002c))
  sbox[0x00000043] = Signal(intbv (0x0000001a))
  sbox[0x00000044] = Signal(intbv (0x0000001b))
  sbox[0x00000045] = Signal(intbv (0x0000006e))
  sbox[0x00000046] = Signal(intbv (0x0000005a))
  sbox[0x00000047] = Signal(intbv (0x000000a0))
  sbox[0x00000048] = Signal(intbv (0x00000052))
  sbox[0x00000049] = Signal(intbv (0x0000003b))
  sbox[0x0000004a] = Signal(intbv (0x000000d6))
  sbox[0x0000004b] = Signal(intbv (0x000000b3))
  sbox[0x0000004c] = Signal(intbv (0x00000029))
  sbox[0x0000004d] = Signal(intbv (0x000000e3))
  sbox[0x0000004e] = Signal(intbv (0x0000002f))
  sbox[0x0000004f] = Signal(intbv (0x00000084))
  sbox[0x00000050] = Signal(intbv (0x00000053))
  sbox[0x00000051] = Signal(intbv (0x000000d1))
  sbox[0x00000052] = Signal(intbv (0x00000000))
  sbox[0x00000053] = Signal(intbv (0x000000ed))
  sbox[0x00000054] = Signal(intbv (0x00000020))
  sbox[0x00000055] = Signal(intbv (0x000000fc))
  sbox[0x00000056] = Signal(intbv (0x000000b1))
  sbox[0x00000057] = Signal(intbv (0x0000005b))
  sbox[0x00000058] = Signal(intbv (0x0000006a))
  sbox[0x00000059] = Signal(intbv (0x000000cb))
  sbox[0x0000005a] = Signal(intbv (0x000000be))
  sbox[0x0000005b] = Signal(intbv (0x00000039))
  sbox[0x0000005c] = Signal(intbv (0x0000004a))
  sbox[0x0000005d] = Signal(intbv (0x0000004c))
  sbox[0x0000005e] = Signal(intbv (0x00000058))
  sbox[0x0000005f] = Signal(intbv (0x000000cf))
  sbox[0x00000060] = Signal(intbv (0x000000d0))
  sbox[0x00000061] = Signal(intbv (0x000000ef))
  sbox[0x00000062] = Signal(intbv (0x000000aa))
  sbox[0x00000063] = Signal(intbv (0x000000fb))
  sbox[0x00000064] = Signal(intbv (0x00000043))
  sbox[0x00000065] = Signal(intbv (0x0000004d))
  sbox[0x00000066] = Signal(intbv (0x00000033))
  sbox[0x00000067] = Signal(intbv (0x00000085))
  sbox[0x00000068] = Signal(intbv (0x00000045))
  sbox[0x00000069] = Signal(intbv (0x000000f9))
  sbox[0x0000006a] = Signal(intbv (0x00000002))
  sbox[0x0000006b] = Signal(intbv (0x0000007f))
  sbox[0x0000006c] = Signal(intbv (0x00000050))
  sbox[0x0000006d] = Signal(intbv (0x0000003c))
  sbox[0x0000006e] = Signal(intbv (0x0000009f))
  sbox[0x0000006f] = Signal(intbv (0x000000a8))
  sbox[0x00000070] = Signal(intbv (0x00000051))
  sbox[0x00000071] = Signal(intbv (0x000000a3))
  sbox[0x00000072] = Signal(intbv (0x00000040))
  sbox[0x00000073] = Signal(intbv (0x0000008f))
  sbox[0x00000074] = Signal(intbv (0x00000092))
  sbox[0x00000075] = Signal(intbv (0x0000009d))
  sbox[0x00000076] = Signal(intbv (0x00000038))
  sbox[0x00000077] = Signal(intbv (0x000000f5))
  sbox[0x00000078] = Signal(intbv (0x000000bc))
  sbox[0x00000079] = Signal(intbv (0x000000b6))
  sbox[0x0000007a] = Signal(intbv (0x000000da))
  sbox[0x0000007b] = Signal(intbv (0x00000021))
  sbox[0x0000007c] = Signal(intbv (0x00000010))
  sbox[0x0000007d] = Signal(intbv (0x000000ff))
  sbox[0x0000007e] = Signal(intbv (0x000000f3))
  sbox[0x0000007f] = Signal(intbv (0x000000d2))
  sbox[0x00000080] = Signal(intbv (0x000000cd))
  sbox[0x00000081] = Signal(intbv (0x0000000c))
  sbox[0x00000082] = Signal(intbv (0x00000013))
  sbox[0x00000083] = Signal(intbv (0x000000ec))
  sbox[0x00000084] = Signal(intbv (0x0000005f))
  sbox[0x00000085] = Signal(intbv (0x00000097))
  sbox[0x00000086] = Signal(intbv (0x00000044))
  sbox[0x00000087] = Signal(intbv (0x00000017))
  sbox[0x00000088] = Signal(intbv (0x000000c4))
  sbox[0x00000089] = Signal(intbv (0x000000a7))
  sbox[0x0000008a] = Signal(intbv (0x0000007e))
  sbox[0x0000008b] = Signal(intbv (0x0000003d))
  sbox[0x0000008c] = Signal(intbv (0x00000064))
  sbox[0x0000008d] = Signal(intbv (0x0000005d))
  sbox[0x0000008e] = Signal(intbv (0x00000019))
  sbox[0x0000008f] = Signal(intbv (0x00000073))
  sbox[0x00000090] = Signal(intbv (0x00000060))
  sbox[0x00000091] = Signal(intbv (0x00000081))
  sbox[0x00000092] = Signal(intbv (0x0000004f))
  sbox[0x00000093] = Signal(intbv (0x000000dc))
  sbox[0x00000094] = Signal(intbv (0x00000022))
  sbox[0x00000095] = Signal(intbv (0x0000002a))
  sbox[0x00000096] = Signal(intbv (0x00000090))
  sbox[0x00000097] = Signal(intbv (0x00000088))
  sbox[0x00000098] = Signal(intbv (0x00000046))
  sbox[0x00000099] = Signal(intbv (0x000000ee))
  sbox[0x0000009a] = Signal(intbv (0x000000b8))
  sbox[0x0000009b] = Signal(intbv (0x00000014))
  sbox[0x0000009c] = Signal(intbv (0x000000de))
  sbox[0x0000009d] = Signal(intbv (0x0000005e))
  sbox[0x0000009e] = Signal(intbv (0x0000000b))
  sbox[0x0000009f] = Signal(intbv (0x000000db))
  sbox[0x000000a0] = Signal(intbv (0x000000e0))
  sbox[0x000000a1] = Signal(intbv (0x00000032))
  sbox[0x000000a2] = Signal(intbv (0x0000003a))
  sbox[0x000000a3] = Signal(intbv (0x0000000a))
  sbox[0x000000a4] = Signal(intbv (0x00000049))
  sbox[0x000000a5] = Signal(intbv (0x00000006))
  sbox[0x000000a6] = Signal(intbv (0x00000024))
  sbox[0x000000a7] = Signal(intbv (0x0000005c))
  sbox[0x000000a8] = Signal(intbv (0x000000c2))
  sbox[0x000000a9] = Signal(intbv (0x000000d3))
  sbox[0x000000aa] = Signal(intbv (0x000000ac))
  sbox[0x000000ab] = Signal(intbv (0x00000062))
  sbox[0x000000ac] = Signal(intbv (0x00000091))
  sbox[0x000000ad] = Signal(intbv (0x00000095))
  sbox[0x000000ae] = Signal(intbv (0x000000e4))
  sbox[0x000000af] = Signal(intbv (0x00000079))
  sbox[0x000000b0] = Signal(intbv (0x000000e7))
  sbox[0x000000b1] = Signal(intbv (0x000000c8))
  sbox[0x000000b2] = Signal(intbv (0x00000037))
  sbox[0x000000b3] = Signal(intbv (0x0000006d))
  sbox[0x000000b4] = Signal(intbv (0x0000008d))
  sbox[0x000000b5] = Signal(intbv (0x000000d5))
  sbox[0x000000b6] = Signal(intbv (0x0000004e))
  sbox[0x000000b7] = Signal(intbv (0x000000a9))
  sbox[0x000000b8] = Signal(intbv (0x0000006c))
  sbox[0x000000b9] = Signal(intbv (0x00000056))
  sbox[0x000000ba] = Signal(intbv (0x000000f4))
  sbox[0x000000bb] = Signal(intbv (0x000000ea))
  sbox[0x000000bc] = Signal(intbv (0x00000065))
  sbox[0x000000bd] = Signal(intbv (0x0000007a))
  sbox[0x000000be] = Signal(intbv (0x000000ae))
  sbox[0x000000bf] = Signal(intbv (0x00000008))
  sbox[0x000000c0] = Signal(intbv (0x000000ba))
  sbox[0x000000c1] = Signal(intbv (0x00000078))
  sbox[0x000000c2] = Signal(intbv (0x00000025))
  sbox[0x000000c3] = Signal(intbv (0x0000002e))
  sbox[0x000000c4] = Signal(intbv (0x0000001c))
  sbox[0x000000c5] = Signal(intbv (0x000000a6))
  sbox[0x000000c6] = Signal(intbv (0x000000b4))
  sbox[0x000000c7] = Signal(intbv (0x000000c6))
  sbox[0x000000c8] = Signal(intbv (0x000000e8))
  sbox[0x000000c9] = Signal(intbv (0x000000dd))
  sbox[0x000000ca] = Signal(intbv (0x00000074))
  sbox[0x000000cb] = Signal(intbv (0x0000001f))
  sbox[0x000000cc] = Signal(intbv (0x0000004b))
  sbox[0x000000cd] = Signal(intbv (0x000000bd))
  sbox[0x000000ce] = Signal(intbv (0x0000008b))
  sbox[0x000000cf] = Signal(intbv (0x0000008a))
  sbox[0x000000d0] = Signal(intbv (0x00000070))
  sbox[0x000000d1] = Signal(intbv (0x0000003e))
  sbox[0x000000d2] = Signal(intbv (0x000000b5))
  sbox[0x000000d3] = Signal(intbv (0x00000066))
  sbox[0x000000d4] = Signal(intbv (0x00000048))
  sbox[0x000000d5] = Signal(intbv (0x00000003))
  sbox[0x000000d6] = Signal(intbv (0x000000f6))
  sbox[0x000000d7] = Signal(intbv (0x0000000e))
  sbox[0x000000d8] = Signal(intbv (0x00000061))
  sbox[0x000000d9] = Signal(intbv (0x00000035))
  sbox[0x000000da] = Signal(intbv (0x00000057))
  sbox[0x000000db] = Signal(intbv (0x000000b9))
  sbox[0x000000dc] = Signal(intbv (0x00000086))
  sbox[0x000000dd] = Signal(intbv (0x000000c1))
  sbox[0x000000de] = Signal(intbv (0x0000001d))
  sbox[0x000000df] = Signal(intbv (0x0000009e))
  sbox[0x000000e0] = Signal(intbv (0x000000e1))
  sbox[0x000000e1] = Signal(intbv (0x000000f8))
  sbox[0x000000e2] = Signal(intbv (0x00000098))
  sbox[0x000000e3] = Signal(intbv (0x00000011))
  sbox[0x000000e4] = Signal(intbv (0x00000069))
  sbox[0x000000e5] = Signal(intbv (0x000000d9))
  sbox[0x000000e6] = Signal(intbv (0x0000008e))
  sbox[0x000000e7] = Signal(intbv (0x00000094))
  sbox[0x000000e8] = Signal(intbv (0x0000009b))
  sbox[0x000000e9] = Signal(intbv (0x0000001e))
  sbox[0x000000ea] = Signal(intbv (0x00000087))
  sbox[0x000000eb] = Signal(intbv (0x000000e9))
  sbox[0x000000ec] = Signal(intbv (0x000000ce))
  sbox[0x000000ed] = Signal(intbv (0x00000055))
  sbox[0x000000ee] = Signal(intbv (0x00000028))
  sbox[0x000000ef] = Signal(intbv (0x000000df))
  sbox[0x000000f0] = Signal(intbv (0x0000008c))
  sbox[0x000000f1] = Signal(intbv (0x000000a1))
  sbox[0x000000f2] = Signal(intbv (0x00000089))
  sbox[0x000000f3] = Signal(intbv (0x0000000d))
  sbox[0x000000f4] = Signal(intbv (0x000000bf))
  sbox[0x000000f5] = Signal(intbv (0x000000e6))
  sbox[0x000000f6] = Signal(intbv (0x00000042))
  sbox[0x000000f7] = Signal(intbv (0x00000068))
  sbox[0x000000f8] = Signal(intbv (0x00000041))
  sbox[0x000000f9] = Signal(intbv (0x00000099))
  sbox[0x000000fa] = Signal(intbv (0x0000002d))
  sbox[0x000000fb] = Signal(intbv (0x0000000f))
  sbox[0x000000fc] = Signal(intbv (0x000000b0))
  sbox[0x000000fd] = Signal(intbv (0x00000054))
  sbox[0x000000fe] = Signal(intbv (0x000000bb))
  sbox[0x000000ff] = Signal(intbv (0x00000016))

  return sbox

# //======================================================================
# // EOF aes_sbox.v
# //======================================================================