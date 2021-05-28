clear

set title "Tasking system benchmark (Burst 256 tasks)"
set xlabel "# Workers"
set ylabel "avg dispatch time (s)"
set y2label "avg time in system (s)"

set log
set yrange [0.01 : 1]
set y2range [0.01 : 100]
set xtics nomirror scale 1, 0 2
unset x2tics
set ytics nomirror
set y2tics nomirror
set style data points

f1(x) = a1 + b1 * x
g1(x) = c1 + d1 * x
f2(x) = a2 + b2 * x
g2(x) = c2 + d2 * x

plot \
  'workers-old.data' u ($1==256?$6:NaN):($2*1e-9/$1) axes x1y1 title "old avg dispatch time", \
  '' u ($1==256?$6:NaN):5 axes x1y2 title "old avg time in system", \
  'workers-new.data' u ($1==256?$6:NaN):($2*1e-9/$1) axes x1y1 title "new avg dispatch time", \
  '' u ($1==256?$6:NaN):5 axes x1y2 title "new avg time in system", \
