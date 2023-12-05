:y = :x
if :x >= :y [
   :y = :y + :c1
   :x = :x + :c2
]
:y = :y + :c2
:x =:x + :c1
if :x == :y [
   :y = :y + :c2
   :x = :x + :c1 ]
:y = :y + :c1
:x = :x + :c2
