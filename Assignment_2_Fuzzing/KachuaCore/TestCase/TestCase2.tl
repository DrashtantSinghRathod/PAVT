left 90
if(:x>:y)[
	if(:x>:z)[
            if(:v>:u)[
              right 145
			  forward 66]
			else[
				right 145
				backward 66]]
	else[
		if(:u>:v)[
           left 45
		   backward 66]
		else[
           left 145
		   forward 66]]]
else[
	if(:y>:z)[
		if(:v > :u)[
           left 45
		   backward 66]
		else[
           left 145
		   forward 66]]
	else[
            if(:u>:v)[
              right 90
			  forward 90]
			else[
				right 145
				backward 90]]]
