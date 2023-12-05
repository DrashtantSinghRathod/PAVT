if :x <:y 
[
    right 45
    forward 50 
    if :y >50 
    [
        right 45
        forward 50 
        if :z <= 60
        [
            right 45
            forward 50
            left 90
             if :y >750 
   [
        right 45
        forward 50 
        if :z <= 60
        [
            right 45
            forward 50 
        ]
        
    ]
            backward 80
            right45
            forward 47 
        ]
        if :y <=750 
        [
             backward 80
            right45
            forward 47 
        ]
        
    ]
]
if :x >= 70 
[
    right 45
    forward 50 
    if :y <50 
    [
        right 45
        forward 50 
        if :z > 60
        [
            right 45
            forward 50 
        ]
        
    ]
]
