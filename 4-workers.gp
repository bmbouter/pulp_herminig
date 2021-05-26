set title "4 workers"
set xlabel "Tasks (burst)"
set ylabel "avg dispatch time (s)"
set y2label "avg time in system (s)"

set log
set xtics nomirror
unset x2tics
set ytics nomirror
set y2tics nomirror
set style data points

plot \
       '4-workers-old.data' u 1:($2*1e-9/$1) axes x1y1 title "old avg dispatch time", \
       '' u 1:5 axes x1y2 title "old avg time in system", \
       '4-workers-new.data' u 1:($2*1e-9/$1) axes x1y1 title "new avg dispatch time", \
       '' u 1:5 axes x1y2 title "new avg time in system"
