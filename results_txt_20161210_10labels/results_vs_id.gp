#set terminal pdfcairo enhanced font "Times New Roman, 20"
#set output "20_m_num_vs_vt.pdf"
#set terminal postscript eps color solid font "Times New Roman, 20"
# set terminal postscript eps color solid font ",20"
set terminal pdf color solid
#set terminal emf color solid enhanced font "Times New Roman, 20"
set output "1st_accuracy_vs_id.pdf"
#set terminal qt font "Times New Roman, 20"
#set xlabel "{/SimSun=20 空洞数量}"
set xlabel "User ID"
set xrange [1:50]
set xtics 10
set xtics add ("1" 1)
set mxtics 1
# set auto x
# set xtics 10
# set xtic rotate by -90 scale 0

#set ylabel "{/SimSun=20 有效监测时间率 (%)}"
set ylabel "Accuracy of 1st Predictor (%)"
set yrange [0:100]
set ytics 20
set mytics 2
set format y "%.1f"
set grid
# set key box
# set key Left
unset key

# set style data histogram
# set style histogram cluster gap 1
# set style fill solid border -1
# set boxwidth 1
# plot "accuracy.txt" using ($2*100):xticlabels(1) ti col
# plot "accuracy.txt" using ($2*100) ti col
plot "accuracy1.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output
#!pdftops -eps 10_m_num_vs_vt.pdf

set output "1st_precision_vs_id.pdf"
set ylabel "Precision of 1st Predictor (%)"
# plot "precision.txt" using ($2*100) ti col
plot "precision.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output

set output "1st_recall_vs_id.pdf"
set ylabel "Recall of 1st Predictor (%)"
# plot "recall.txt" using ($2*100) ti col
plot "recall.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output

set output "1st_f1_vs_id.pdf"
set ylabel "F-measure of 1st Predictor (%)"
# plot "f1.txt" using ($2*100) ti col
plot "f1.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output

set output "2nd_accuracy_vs_id.pdf"
set ylabel "Accuracy of 2nd Predictor (%)"
# plot "f1.txt" using ($2*100) ti col
plot "accuracy2.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output

set output "user_exp_vs_id.pdf"
set ylabel "Percent of Stalling (%)"
# plot "user_exp.txt" using 2 ti col
plot "user_exp.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output

set output "overall_accuracy_vs_id.pdf"
set ylabel "Overall Accuracy (%)"
# plot "skip_accuracy.txt" using 2 ti col
plot "overall_accuracy.txt" using 1:($2*100) w lp lt 1 lw 2 pt 5 ps 1 title ""
set output
