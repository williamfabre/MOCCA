logic=cordic_cor
ifndef logic
		$(error logic must be set)
endif

all : $(logic).v 

$(logic).v : $(logic).vhd
	vasy -I vhd -V -o -v $< $(logic)

clean:
	rm -f *.al *.vbe *.vst *.v *.blif *.rep *.o core *~ vivado.* *.xsc *.ap
