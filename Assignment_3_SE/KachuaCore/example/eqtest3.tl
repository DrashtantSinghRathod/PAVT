:y=0
if(:y > :x)[
   forward :x
   :y = :y+:c1
   right :y

]else[
   forward :x
   :y = :y+:c2
   left :y
]
