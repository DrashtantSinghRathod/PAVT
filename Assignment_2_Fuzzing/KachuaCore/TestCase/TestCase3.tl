pendown
left 90
:move = 90
if(:x>:y)[
    if(:y>:z)[
        right 45
        forward :move
    ]else[
        left 45
        backward :move]]
else[
    if(:x>:z)[
       left 45 
       forward :move]
    else[
        right 45
        backward :move]]
