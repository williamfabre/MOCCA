// Generated by Cadence Encounter(R) RTL Compiler RC13.12 - v13.10-s021_1
tclmode
set env(RC_VERSION) "RC13.12 - v13.10-s021_1"
vpxmode
set dofile abort exit
usage -auto -elapse
set log file fv/MIPS_32_1P_MUL_DIV/rtl_to_g1.log -replace
tclmode
set ver [lindex [split [lindex [get_version_info] 0] "-"] 0]
vpxmode
tclmode
set env(CDN_SYNTH_ROOT) /users/soft/opus/Linux/RC-13.12-000/tools.lnx86
set CDN_SYNTH_ROOT /users/soft/opus/Linux/RC-13.12-000/tools.lnx86
vpxmode
tclmode
if {$ver >= 08.10} {
  vpx set naming style rc
}
vpxmode
set naming rule "%s[%d]" -instance_array
set naming rule "%s_reg" -register -golden
set naming rule "%L.%s" "%L[%d].%s" "%s" -instance
set naming rule "%L.%s" "%L[%d].%s" "%s" -variable
set undefined cell black_box -noascend -both
set undriven signal Z -golden

add search path -library . /users/soft/opus/Linux/RC-13.12-000/tools.lnx86/lib/tech
read library -statetable -liberty -both  \
	/users/enseig/tuna/ue_vlsi2/techno/cmos_120/cmos_120nm_core_Worst.lib

add search path -design .
read design -rangeconstraint -configuration  -enumconstraint -golden -lastmod -noelab \
	-vhdl 93 \
		/users/enseig/fabre/work/MOCCA/ProjetMOCCA/src/mips_with_reset.vhd

elaborate design -golden -root MIPS_32_1P_MUL_DIV -rootonly \

tclmode
if {$ver < 13.10} {
vpx read design -verilog -revised -lastmod -noelab \
	-unzip fv/MIPS_32_1P_MUL_DIV/g1.v.gz
} else {
vpx read design -verilog95 -revised -lastmod -noelab \
	-unzip fv/MIPS_32_1P_MUL_DIV/g1.v.gz
}
vpxmode

elaborate design -revised -root MIPS_32_1P_MUL_DIV

tclmode
set ver [lindex [split [lindex [get_version_info] 0] "-"] 0]
if {$ver < 13.10} {
vpx substitute blackbox model -golden
}
vpxmode
report design data
report black box

uniquify -all -nolib
set flatten model -seq_constant -seq_constant_x_to 0
set flatten model -nodff_to_dlat_zero -nodff_to_dlat_feedback
// set parallel option -threads 4 -license xl -norelease_license
// set compare options -threads 0
set analyze option -auto

set system mode lec
analyze datapath -module -verbose
usage
analyze datapath -verbose
// report mapped points
report unmapped points -summary
report unmapped points -extra -unreachable -notmapped
add compared points -all
// report compared points
compare
usage
// report compare data
report compare data -class nonequivalent -class abort -class notcompared
report verification -verbose
report statistics
tclmode
puts "No of compare points = [get_compare_points -count]"
puts "No of diff points    = [get_compare_points -diff -count]"
puts "No of abort points   = [get_compare_points -abort -count]"
puts "No of unknown points = [get_compare_points -unknown -count]"
if {[get_compare_points -count] == 0} {
    puts "---------------------------------"
    puts "ERROR: No compare points detected"
    puts "---------------------------------"
}
if {[get_compare_points -diff -count] > 0} {
    puts "------------------------------------"
    puts "ERROR: Different Key Points detected"
    puts "------------------------------------"
#     foreach i [get_compare_points -diff] {
#         vpx report test vector [get_keypoint $i]
#         puts "     ----------------------------"
#     }
}
if {[get_compare_points -abort -count] > 0} {
    puts "-----------------------------"
    puts "ERROR: Abort Points detected "
    puts "-----------------------------"
}
if {[get_compare_points -unknown -count] > 0} {
    puts "----------------------------------"
    puts "ERROR: Unknown Key Points detected"
    puts "----------------------------------"
}
vpxmode
exit -force