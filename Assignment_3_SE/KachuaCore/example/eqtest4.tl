:y = 0
if(:y > :x)[
   :y = :y + 90
   forward :x
   right :y
]else[
   :y =:y +90
   forward :x
   left :y
]
