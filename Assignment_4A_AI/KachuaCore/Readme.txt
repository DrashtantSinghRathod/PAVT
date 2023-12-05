CS 639: Program Analysis, Verification And Testing
Assignment #4A: Abstract Interpretation

Problem Statement:

In this assignment, we will try to track for safe movements of Kachua. Kachua would move in accordance to the program instructions, and eventually rests at the final position reached at the end of the program. If Kachua rests into an area in a magarmach's (crocodile's) region, the magarmach can eat it. Such a dangerous region is usually rectangular in shape and can be described by x-coordinate interval and y-coordinate interval e.g, ([x1, x2], [y1, y2]). Given a Turtle program, students need to verify that the Kachua never rests in the magarmach's region. You need to verify this using abstract interpretation with the interval domain.

TestCases:-

The test cases are enclosed inside the directory:
Kachua-Framework\KachuaCore\example
example1.tl
example2.tl
example3.tl
example4.tl
example5.tl
	

Running Abstract Interpretation:- 
python3.8 kachua.py -ai example/example1.tl





	
