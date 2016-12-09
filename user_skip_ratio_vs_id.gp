#set terminal pdfcairo enhanced font "Times New Roman, 20"
#set output "20_m_num_vs_vt.pdf"
#set terminal postscript eps color solid font "Times New Roman, 20"
# set terminal postscript eps color solid font ",20"
set terminal pdf
#set terminal emf color solid enhanced font "Times New Roman, 20"
set output "user_skip_ratio_vs_id.pdf"
#set terminal qt font "Times New Roman, 20"
#set xlabel "{/SimSun=20 空洞数量}"
set xlabel "User ID"
set xrange [1:50]
set xtics 10
set xtics add ("1" 1)
set mxtics 1
#set ylabel "{/SimSun=20 有效监测时间率 (%)}"
set ylabel "Skip Ratio (%)"
set yrange [0:100]
set ytics 20
set mytics 2
set format y "%.1f"
set grid
# set key box
# set key Left
unset key

#########################################################
# set style data histogram
# set style histogram cluster gap 1
# set style fill solid border -1
# set boxwidth 1
# plot "user_skip_ratio.txt" using ($2*100) ti col
#########################################################

#set key width 10
#set key spacing 10
#set key right top at 4.93, 78.2
plot "user_skip_ratio.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 #title "half"
set output
#!pdftops -pdf 20_m_num_vs_vt.pdf
