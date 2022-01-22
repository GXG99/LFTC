bits 32
global start
extern exit, printf, scanf
import exit msvcrt.dll
import printf msvcrt.dll
import scanf msvcrt.dll

segment data use32 class=data
	format db "%d", 10, 0
	A dw 0
	B dw 0
	C dw 0

segment  code use32 class=code
	start:
	;Multiply
		mov AX, 3
		mov BX, 4
		mul BX
		push DX
		push AX
		pop EAX
		mov [A], EAX
	;Reading variable
		push dword C
		push dword format
		call [scanf]
		add esp, 4 * 2
	;Adding
		mov AX, [C]
		mov BX, 4
		add AX, BX
		mov [B], AX
	;Printing variable
		mov eax, [B]
		push dword eax
		push dword format
		call [printf]
		add esp, 4 * 2

		push dword 0
		call [exit]