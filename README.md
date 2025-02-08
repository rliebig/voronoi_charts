# Voronoi Diagrams

Voronoi Diagrams are very interesting, and have been implemented a lot already. This repository
just documents my efforts to implement Fortune Algorithm in a somewhat stable fashion. I initially
toyed a lot around with just using the generated beachline to generate the voronoi edges,
but I have dropped this effort because it has some drawbacks. I still believe that it is possible
to generate the voronoi chart, just by a slightly modified beachline structure and searching
the beachline for local minima / critical points where are direction changes, but I have not been
able to implement this.

Therefore, we have a simply pygame implementation.  
